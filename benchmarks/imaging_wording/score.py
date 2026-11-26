"""Measure routing and parsed-event coverage against frozen semantic labels."""
import json
from pathlib import Path

from evidence_bound_ai_evaluation_harness.fidelity import check_packet


def score(packet, labels):
    rows = check_packet(packet)["results"]
    if set(labels) != {row["claim_id"] for row in rows}:
        raise ValueError("The packet and labels must have identical claim IDs.")
    counts = {}
    for row in rows:
        label = labels[row["claim_id"]]
        group = label["group"]
        if group not in {"control", "challenge"} or type(label["supported"]) is not bool:
            raise ValueError(f"Invalid label for {row['claim_id']}")
        tally = counts.setdefault(group, dict(total=0, supported=0, false_pass=0,
                                              extra_review=0, covered=0))
        good = label["supported"]
        passed = row["status"] == "matched"
        evidence = row["evidence"]
        covered = bool(evidence) and row["event"] is not None and all(
            item.get("event") is not None for item in evidence
        )
        tally["total"] += 1
        tally["supported"] += good
        tally["false_pass"] += passed and not good
        tally["extra_review"] += good and not passed
        tally["covered"] += covered
    return counts


def main():
    folder = Path(__file__).parent
    packet = json.loads((folder / "packet.json").read_text(encoding="utf-8"))
    labels = json.loads((folder / "labels.json").read_text(encoding="utf-8"))
    for group, t in score(packet, labels).items():
        total, supported = t["total"], t["supported"]
        print(f"{group}: false passes {t['false_pass']}/{total - supported}, "
              f"extra reviews {t['extra_review']}/{supported}, "
              f"parsed coverage {t['covered']}/{total}")


if __name__ == "__main__":
    main()
