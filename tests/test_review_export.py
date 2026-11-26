import json
import os
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

import pytest

from evidence_bound_ai_evaluation_harness.fidelity import check_packet
from evidence_bound_ai_evaluation_harness.review_html import render_review


ROOT = Path(__file__).resolve().parents[1]
PACKET_PATH = ROOT / "benchmarks" / "temporal_fidelity" / "packet.json"
EXAMPLE_PATH = ROOT / "docs" / "review-example.html"


class Document(HTMLParser):
    def __init__(self, html: str):
        super().__init__()
        self.elements = []
        self.body_text = []
        self.in_body = False
        self.feed(html)
        self.close()

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))
        if tag == "body":
            self.in_body = True

    def handle_endtag(self, tag):
        if tag == "body":
            self.in_body = False

    def handle_data(self, data):
        if self.in_body:
            self.body_text.append(data)


def export(path: Path, *options) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "evidence_bound_ai_evaluation_harness", "review", path, *options],
        cwd=ROOT,
        capture_output=True,
    )


def test_cli_exports_exact_reproducible_example_with_review_flags() -> None:
    packet = json.loads(PACKET_PATH.read_text(encoding="utf-8"))
    result = check_packet(packet)
    assert result["summary"]["needs_review"] > 0
    run = export(PACKET_PATH)
    assert run.returncode == 0
    assert run.stderr == b""
    assert run.stdout == render_review(result).encode("utf-8") == EXAMPLE_PATH.read_bytes()


def test_review_page_is_standalone_and_declares_a_mobile_viewport() -> None:
    html = EXAMPLE_PATH.read_text(encoding="utf-8")
    assert html.lstrip().lower().startswith("<!doctype html>")
    page = Document(html)
    assert any(
        tag == "meta"
        and attrs.get("name", "").lower() == "viewport"
        and "width=device-width" in attrs.get("content", "").replace(" ", "").lower()
        for tag, attrs in page.elements
    )
    for tag, attrs in page.elements:
        assert tag not in {"script", "iframe", "object", "embed", "base"}
        assert not any(name.startswith("on") for name in attrs)
        if tag == "link":
            assert attrs.get("href", "").startswith("data:")
        for attr in {"src", "srcset", "poster"} & attrs.keys():
            assert attrs[attr].startswith("data:")
    css_targets = re.findall(r"""(?:url\(\s*|@import\s+)["']?([^"')\s;]+)""", html, re.I)
    assert all(target.startswith(("data:", "#")) for target in css_targets)


def test_all_cited_evidence_and_missing_reference_are_visible_as_text() -> None:
    sources = [
        {"id": "source-1<review-marker>", "visit": "visit-A", "text": "已拍攝 36 根尖片。"},
        {
            "id": "source-2",
            "visit": 'visit-B"<review-marker>',
            "text": 'A <review-marker> described as "left & right".',
        },
    ]
    claim = {
        "id": 'claim-"<review-marker>',
        "visit": "visit-C",
        "text": "影像註記：<review-marker> & 待查。",
        "citations": [sources[0]["id"], sources[1]["id"], "source-X"],
    }
    html = render_review(check_packet({"sources": sources, "claims": [claim]}))
    page = Document(html)
    visible = " ".join(page.body_text)
    for record in [claim, *sources]:
        for key in ("id", "visit", "text"):
            assert record[key] in visible
    assert "source-X" in visible
    assert "source not found" in visible.lower() or "找不到此來源" in visible
    assert "review-marker" not in {tag for tag, _ in page.elements}


@pytest.mark.parametrize(
    "bad_input", ["missing", "malformed", "wrong_shape", "duplicate_id", "duplicate_field"]
)
def test_invalid_input_has_only_stderr_and_exit_two(tmp_path: Path, bad_input: str) -> None:
    path = tmp_path / "packet.json"
    packet = json.loads(PACKET_PATH.read_text(encoding="utf-8"))
    if bad_input == "malformed":
        path.write_text("{", encoding="utf-8")
    elif bad_input == "wrong_shape":
        path.write_text("{}", encoding="utf-8")
    elif bad_input == "duplicate_id":
        packet["sources"].append(packet["sources"][0])
        path.write_text(json.dumps(packet), encoding="utf-8")
    elif bad_input == "duplicate_field":
        duplicated = '{"sources": [], ' + json.dumps(packet)[1:]
        path.write_text(duplicated, encoding="utf-8")
    run = export(path)
    assert run.returncode == 2
    assert run.stdout == b""
    assert run.stderr.strip()


def test_output_option_replaces_report_and_preserves_packet(tmp_path: Path) -> None:
    packet = tmp_path / "packet.json"
    original = PACKET_PATH.read_bytes()
    packet.write_bytes(original)
    output = tmp_path / "review.html"
    output.write_bytes(b"previous report")
    previous = tmp_path / "previous.html"
    os.link(output, previous)
    run = export(packet, "-o", output)
    assert run.returncode == 0
    assert output.read_bytes() == export(packet).stdout
    assert previous.read_bytes() == b"previous report"
    assert packet.read_bytes() == original


def test_bad_packet_preserves_existing_output(tmp_path: Path) -> None:
    packet = tmp_path / "packet.json"
    packet.write_bytes(b"{")
    output = tmp_path / "review.html"
    output.write_bytes(b"previous report")
    run = export(packet, "--output", output)
    assert run.returncode == 2
    assert run.stderr.strip()
    assert output.read_bytes() == b"previous report"
    assert packet.read_bytes() == b"{"


def test_input_as_output_is_rejected_without_changing_packet(tmp_path: Path) -> None:
    packet = tmp_path / "packet.json"
    original = PACKET_PATH.read_bytes()
    packet.write_bytes(original)
    run = export(packet, "--output", packet)
    assert run.returncode == 2
    assert run.stderr.strip()
    assert packet.read_bytes() == original
