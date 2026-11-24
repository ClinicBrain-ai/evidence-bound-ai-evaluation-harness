"""Exercise source fidelity through the public module entry point."""

import json
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "examples" / "case_001_missing_context" / "evaluation_report.json"
PLAN = "預計下次回診拍攝 36 根尖片。"
COMPLETE = "A periapical radiograph for tooth 36 was taken."


def run_cli(*args):
    return subprocess.run(
        [sys.executable, "-m", "evidence_bound_ai_evaluation_harness", *args],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=False,
    )


def packet():
    return {
        "sources": [{"id": "note-1", "visit": "V1", "text": PLAN}],
        "claims": [{"id": "c1", "visit": "V1", "text": PLAN, "citations": ["note-1"]}],
    }


@pytest.mark.parametrize(
    ("claim_text", "code", "status", "reason"),
    [(PLAN, 0, "matched", "status_match"), (COMPLETE, 1, "needs_review", "status_mismatch")],
)
def test_json_result_preserves_claim_and_cited_text(tmp_path, claim_text, code, status, reason):
    value = packet()
    value["claims"][0]["text"] = claim_text
    path = tmp_path / "packet.json"
    original = json.dumps(value, ensure_ascii=False, indent=4).encode("utf-8")
    path.write_bytes(original)

    result = run_cli("check", path, "--json")

    assert result.returncode == code, result.stderr
    assert result.stderr == ""
    report = json.loads(result.stdout)
    assert report["summary"] == {
        "total": 1, "matched": int(status == "matched"), "needs_review": int(status == "needs_review"),
    }
    row, = report["results"]
    assert (row["claim_id"], row["text"], row["status"], row["reason"]) == ("c1", claim_text, status, reason)
    source, = row["evidence"]
    assert (source["id"], source["visit"], source["text"]) == ("note-1", "V1", PLAN)
    assert source["found"] is True
    assert source["event"] == {"key": "pa:36", "state": "planned"}
    assert path.read_bytes() == original


def test_mixed_claims_route_for_review_without_changing_run_order(tmp_path):
    value = packet()
    value["claims"].append({**value["claims"][0], "id": "c2", "citations": ["unlisted"]})
    path = tmp_path / "packet.json"
    path.write_text(json.dumps(value), encoding="utf-8")

    result = run_cli("check", path, "--json")

    assert result.returncode == 1, result.stderr
    report = json.loads(result.stdout)
    assert report["summary"] == {"total": 2, "matched": 1, "needs_review": 1}
    first, second = report["results"]
    assert (first["claim_id"], second["claim_id"]) == ("c1", "c2")
    assert second["reason"] == "unknown_citation"
    assert second["evidence"] == [{"id": "unlisted", "found": False}]


@pytest.mark.parametrize("group", ["claims", "sources", "citations"])
def test_rejects_duplicate_identifiers(tmp_path, group):
    value = packet()
    entries = value["claims"][0]["citations"] if group == "citations" else value[group]
    entries.append(entries[0])
    path = tmp_path / "packet.json"
    original = json.dumps(value).encode("utf-8")
    path.write_bytes(original)

    result = run_cli("check", path, "--json")

    assert result.returncode == 2
    assert result.stdout == ""
    assert "ERROR" in result.stderr
    assert "Traceback" not in result.stderr
    assert path.read_bytes() == original


@pytest.mark.parametrize("bad_input", [b"{", b"null", b'{"sources":[],"claims":[]}', b"\xff", None])
def test_malformed_or_missing_packet_has_input_error_exit_code(tmp_path, bad_input):
    path = tmp_path / "packet.json"
    if bad_input is not None:
        path.write_bytes(bad_input)

    result = run_cli("check", path, "--json")

    assert result.returncode == 2
    assert result.stdout == ""
    assert "ERROR" in result.stderr
    assert "Traceback" not in result.stderr


def test_ambiguous_duplicate_json_member_is_an_input_error(tmp_path):
    value = json.dumps(packet())
    ambiguous = value.replace('"citations": ["note-1"]', '"citations": [], "citations": ["note-1"]')
    assert ambiguous != value
    path = tmp_path / "packet.json"
    path.write_text(ambiguous, encoding="utf-8")

    result = run_cli("check", path, "--json")

    assert result.returncode == 2
    assert "ERROR" in result.stderr
    assert result.stdout == ""


@pytest.mark.parametrize(
    ("field", "invalid"),
    [("id", "c1\n"), ("visit", "V1\n"), ("text", "\ud800")],
)
def test_invalid_identifiers_and_lone_surrogates_are_input_errors(tmp_path, field, invalid):
    value = packet()
    value["claims"][0][field] = invalid
    path = tmp_path / "packet.json"
    path.write_text(json.dumps(value), encoding="utf-8")

    result = run_cli("check", path, "--json")

    assert result.returncode == 2
    assert result.stdout == ""
    assert "ERROR" in result.stderr
    assert "Traceback" not in result.stderr


def test_schema_command_preserves_its_previous_evidence_scope(tmp_path):
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    report["claim_evaluations"][0].update(
        claim_text=COMPLETE, supporting_evidence=[PLAN], support_status="supported",
    )
    path = tmp_path / "report.json"
    path.write_text(json.dumps(report), encoding="utf-8")

    schema_result = run_cli("validate", path)
    fidelity_result = run_cli("check", path, "--json")

    assert schema_result.returncode == 0
    assert "PASS: evaluation report conforms to schema." in schema_result.stdout
    assert fidelity_result.returncode == 2
    assert "ERROR" in fidelity_result.stderr
