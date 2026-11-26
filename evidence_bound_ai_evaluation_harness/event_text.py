"""Recognize the whole-sentence templates in the synthetic imaging benchmark."""

import re
from typing import Optional, Tuple


# Fold only the printable ASCII width variants and the ideographic space.
# Broader Unicode normalization could turn a superscript into a tooth digit.
_WIDTH_MAP = {value: value - 0xFEE0 for value in range(0xFF01, 0xFF5F)}
_WIDTH_MAP[0x3000] = ord(" ")

_TOOTH = r"(?P<tooth>[1-4][1-8])"
_ZH_IMAGE = rf" *{_TOOTH} *根尖片"
_EN_IMAGE = rf"a periapical radiograph for tooth {_TOOTH}"
_TEMPLATES = (
    ("planned", rf"預計下次回診拍攝{_ZH_IMAGE}"),
    ("planned", rf"下回安排拍攝{_ZH_IMAGE}"),
    ("completed", rf"已拍攝{_ZH_IMAGE}"),
    ("not_done", rf"尚未拍攝{_ZH_IMAGE}"),
    ("unknown", rf"{_TOOTH} *根尖片完成與否未記載"),
    ("planned", rf"{_EN_IMAGE} was planned for the next visit"),
    ("completed", rf"{_EN_IMAGE} was taken"),
    ("not_done", rf"{_EN_IMAGE} was not taken"),
    ("unknown", rf"completion of the periapical radiograph for tooth {_TOOTH} was not documented"),
)
_PATTERNS = tuple(
    (status, re.compile(template + r"[.。]?", re.IGNORECASE | re.ASCII))
    for status, template in _TEMPLATES
)


def parse_event(text: str) -> Optional[Tuple[str, str]]:
    """Return (event key, documented status), or None outside the grammar."""
    normalized = text.translate(_WIDTH_MAP).strip(" \t")
    normalized = re.sub(r"[ \t]+", " ", normalized)
    for status, pattern in _PATTERNS:
        match = pattern.fullmatch(normalized)
        if match is not None:
            return f"pa:{match.group('tooth')}", status
    return None
