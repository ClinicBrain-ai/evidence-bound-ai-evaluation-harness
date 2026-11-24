import json
import subprocess
import sys
from pathlib import Path

import pytest

from evidence_bound_ai_evaluation_harness.fidelity import check_packet


FIXTURE_DIR = Path(__file__).resolve().parents[1] / "benchmarks" / "temporal_fidelity"
PACKET = json.loads((FIXTURE_DIR / "packet.json").read_text(encoding="utf-8"))
EXPECTED = json.loads((FIXTURE_DIR / "expected.json").read_text(encoding="utf-8"))


def test_fixture_ids_and_citations() -> None:
    source_ids = {source["id"] for source in PACKET["sources"]}
    claim_ids = {claim["id"] for claim in PACKET["claims"]}
    assert len(source_ids) == len(PACKET["sources"])
    assert len(claim_ids) == len(PACKET["claims"])
    assert claim_ids == set(EXPECTED)
    for claim in PACKET["claims"]:
        reason = EXPECTED[claim["id"]]
        citations = claim["citations"]
        assert (not citations) == (reason == "no_citation")
        assert bool(set(citations) - source_ids) == (reason == "unknown_citation")


def test_temporal_benchmark_matches_expected_labels() -> None:
    results = check_packet(PACKET)["results"]
    assert len(results) == len(EXPECTED)
    assert {result["claim_id"]: result["reason"] for result in results} == EXPECTED
    for result in results:
        expected_match = EXPECTED[result["claim_id"]] == "status_match"
        assert result["status"] == ("matched" if expected_match else "needs_review")


@pytest.mark.parametrize(
    "claim",
    [claim for claim in PACKET["claims"] if len(claim["citations"]) > 1],
    ids=lambda claim: claim["id"],
)
def test_order_of_citations_preserves_result(claim: dict) -> None:
    reordered = {**claim, "citations": list(reversed(claim["citations"]))}
    packet = {"sources": PACKET["sources"], "claims": [reordered]}
    result, = check_packet(packet)["results"]
    assert result["reason"] == EXPECTED[claim["id"]]


def test_scoring_command_reports_both_methods() -> None:
    run = subprocess.run(
        [sys.executable, "-m", "benchmarks.temporal_fidelity.score"],
        cwd=FIXTURE_DIR.parents[1],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "Citation IDs only | 8/18 | 10 | 0" in run.stdout
    assert "Temporal fidelity checker | 18/18 | 0 | 0" in run.stdout
    assert "Exact checker reason agreement 18/18" in run.stdout
