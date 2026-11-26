import json
from pathlib import Path

import pytest

from benchmarks.imaging_wording.score import score


def test_coverage_includes_recognized_mismatch_and_excludes_abstention():
    source = {"id": "s", "visit": "v", "text": "已拍攝 36 根尖片。"}
    claims = [
        {"id": str(i), "visit": "v", "text": text, "citations": ["s"]}
        for i, text in enumerate(["尚未拍攝 36 根尖片。", "A PA of 36 was taken."])
    ]
    packet = {"sources": [source], "claims": claims}
    labels = {str(i): {"group": "challenge", "supported": bool(i)} for i in range(2)}
    assert score(packet, labels)["challenge"] == {
        "total": 2, "supported": 1, "false_pass": 0, "extra_review": 1, "covered": 1
    }
    with pytest.raises(ValueError, match="claim IDs"):
        score(packet, {})


def test_frozen_challenge_has_balanced_pairs_and_separate_controls():
    root = Path(__file__).resolve().parents[1] / "benchmarks" / "imaging_wording"
    packet, labels = [json.loads((root / f"{name}.json").read_text(encoding="utf-8"))
                      for name in ("packet", "labels")]
    counts = score(packet, labels)
    assert counts["challenge"]["total"] == 12
    assert counts["control"]["total"] == 2
    for source in packet["sources"]:
        pair = [labels[c["id"]]["supported"] for c in packet["claims"]
                if c["citations"] == [source["id"]]]
        assert sorted(pair) == [False, True]
