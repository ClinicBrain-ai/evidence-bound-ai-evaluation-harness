import pytest

from evidence_bound_ai_evaluation_harness.event_text import parse_event


@pytest.mark.parametrize(
    ("text", "event", "status"),
    [
        ("預計下次回診拍攝 36 根尖片。", "pa:36", "planned"),
        ("下回安排拍攝 36 根尖片。", "pa:36", "planned"),
        ("已拍攝 36 根尖片。", "pa:36", "completed"),
        ("尚未拍攝 36 根尖片。", "pa:36", "not_done"),
        ("36 根尖片完成與否未記載。", "pa:36", "unknown"),
        ("已拍攝４６根尖片。", "pa:46", "completed"),
        ("  １１　根尖片完成與否未記載．", "pa:11", "unknown"),
        ("A periapical radiograph for tooth 36 was planned for the next visit.", "pa:36", "planned"),
        ("A periapical radiograph for tooth 36 was taken.", "pa:36", "completed"),
        ("A periapical radiograph for tooth 36 was not taken.", "pa:36", "not_done"),
        ("Completion of the periapical radiograph for tooth 36 was not documented.", "pa:36", "unknown"),
        ("Ａ PERIAPICAL radiograph for tooth　４８ was\ttaken", "pa:48", "completed"),
    ],
)
def test_supported_sentences(text, event, status):
    assert parse_event(text) == (event, status)


@pytest.mark.parametrize(
    "text",
    [
        "",
        "已拍攝 36 根尖片？",
        "是否已拍攝 36 根尖片。",
        "並非尚未拍攝 36 根尖片。",
        "已拍攝 36 及 46 根尖片。",
        "已拍攝 36 根尖片。尚未拍攝 46 根尖片。",
        "已拍攝 36 根尖片，未見異常。",
        "已拍攝 36 根尖片機。",
        "已拍攝 36 咬翼片。",
        "已拍攝 39 根尖片。",
        "已拍攝 51 根尖片。",
        "已拍攝 ３⁶ 根尖片。",
        "A periapical radiograph for tooth 36 was not not taken.",
        "A periapical radiograph for tooth 36 was taken?",
        "A periapical radiograph for tooth 36 was taken if necessary.",
        "A periapical radiograph for tooth 36 was taken and reviewed.",
        "A periapical radiograph for tooth 36\nwas taken.",
        "A periapical radiograph for tooth 36 was taken. No findings.",
        "A periapical radiograph for tooth 360 was taken.",
        "A periapical radiograph device for tooth 36 was taken.",
    ],
)
def test_out_of_grammar_sentences_abstain(text):
    assert parse_event(text) is None
