"""Score the frozen synthetic packet from a checkout with Python's -m option."""

import json
import sys
from pathlib import Path

from evidence_bound_ai_evaluation_harness.fidelity import check_packet


FIXTURE_DIR = Path(__file__).resolve().parent


def print_decisions(name: str, decisions: dict, expected: dict) -> None:
    false_passes = 0
    unnecessary_reviews = 0
    for claim_id, status in decisions.items():
        expected_match = expected[claim_id] == "status_match"
        if status == "matched" and not expected_match:
            false_passes += 1
        elif status == "needs_review" and expected_match:
            unnecessary_reviews += 1
    total = len(expected)
    correct = total - false_passes - unnecessary_reviews
    print(f"{name} | {correct}/{total} | {false_passes} | {unnecessary_reviews}")


def main() -> int:
    packet = json.loads((FIXTURE_DIR / "packet.json").read_text(encoding="utf-8"))
    expected = json.loads((FIXTURE_DIR / "expected.json").read_text(encoding="utf-8"))
    claims = packet["claims"]
    if len(claims) != len(expected) or {c["id"] for c in claims} != set(expected):
        print("Claim IDs and expected label IDs must agree one to one.", file=sys.stderr)
        return 1

    results = check_packet(packet)["results"]
    if len(results) != len(expected) or {r["claim_id"] for r in results} != set(expected):
        print("Checker result IDs and expected label IDs must agree one to one.", file=sys.stderr)
        return 1
    if any(r["status"] not in {"matched", "needs_review"} for r in results):
        print("The checker returned an unrecognized decision.", file=sys.stderr)
        return 1

    source_ids = {source["id"] for source in packet["sources"]}
    baseline = {}
    for claim in claims:
        citations = claim["citations"]
        ids_exist = bool(citations) and source_ids.issuperset(citations)
        baseline[claim["id"]] = "matched" if ids_exist else "needs_review"
    predicted = {r["claim_id"]: r["status"] for r in results}
    print("Synthetic temporal fidelity fixture")
    print("Method | Correct decisions | False passes | Unnecessary reviews")
    print_decisions("Citation IDs only", baseline, expected)
    print_decisions("Temporal fidelity checker", predicted, expected)

    reason_matches = 0
    errors = False
    for result in results:
        claim_id = result["claim_id"]
        label = expected[claim_id]
        expected_status = "matched" if label == "status_match" else "needs_review"
        if result["reason"] == label:
            reason_matches += 1
        if result["reason"] != label or result["status"] != expected_status:
            errors = True
            print(
                f"{claim_id} expected {expected_status}/{label}, "
                f"received {result['status']}/{result['reason']}.",
                file=sys.stderr,
            )
    print(f"Exact checker reason agreement {reason_matches}/{len(expected)}")
    return int(errors)


if __name__ == "__main__":
    raise SystemExit(main())
