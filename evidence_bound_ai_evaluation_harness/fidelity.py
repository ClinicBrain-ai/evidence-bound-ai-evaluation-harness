"""Compare cited documentation with claims in the bounded imaging-status task."""

from typing import Optional

from jsonschema import Draft202012Validator

from .event_text import parse_event

_ID = {"type": "string", "minLength": 1, "not": {"pattern": r"[\s\ud800-\udfff]"}}
_TEXT = {"type": "string", "pattern": r"\S", "not": {"pattern": r"[\ud800-\udfff]"}}
_RECORD_FIELDS = {
    "id": _ID,
    "visit": _ID,
    "text": _TEXT,
}


def _records(fields: dict) -> dict:
    return {
        "type": "array",
        "items": {
            "type": "object",
            "additionalProperties": False,
            "required": list(fields),
            "properties": fields,
        },
    }


_PACKET = Draft202012Validator({
    "type": "object",
    "required": ["sources", "claims"],
    "additionalProperties": False,
    "properties": {
        "sources": _records(_RECORD_FIELDS),
        "claims": {
            **_records({
                **_RECORD_FIELDS,
                "citations": {"type": "array", "items": _ID, "uniqueItems": True},
            }),
            "minItems": 1,
        },
    },
})


def _validate_packet(packet: dict) -> None:
    error = next(_PACKET.iter_errors(packet), None)
    if error is not None:
        raise ValueError(f"{error.json_path}: {error.message}")
    for group in ("sources", "claims"):
        seen = set()
        for record in packet[group]:
            if record["id"] in seen:
                raise ValueError(f"Duplicate ID in {group}: {record['id']}")
            seen.add(record["id"])


def _event(text: str) -> Optional[dict]:
    parsed = parse_event(text)
    if parsed is None:
        return None
    event_key, state = parsed
    return {"key": event_key, "state": state}


def _reason(claim: dict, evidence: list) -> str:
    if not evidence:
        return "no_citation"
    if any(not item["found"] for item in evidence):
        return "unknown_citation"
    if claim["event"] is None:
        return "unrecognized_claim"
    if any(item["event"] is None for item in evidence):
        return "unrecognized_source"
    if any(item["visit"] != claim["visit"] for item in evidence):
        return "visit_mismatch"
    if any(item["event"]["key"] != claim["event"]["key"] for item in evidence):
        return "event_mismatch"
    states = {item["event"]["state"] for item in evidence}
    if len(states) > 1:
        return "conflicting_sources"
    if claim["event"]["state"] not in states:
        return "status_mismatch"
    return "status_match"


def check_packet(packet: dict) -> dict:
    """Check every claim against every cited source. Raise ValueError for bad input."""
    _validate_packet(packet)
    sources = {
        item["id"]: {**item, "found": True, "event": _event(item["text"])}
        for item in packet["sources"]
    }
    results = []
    for item in packet["claims"]:
        claim = {**item, "event": _event(item["text"])}
        evidence = [
            sources.get(ref, {"id": ref, "found": False}) for ref in claim["citations"]
        ]
        reason = _reason(claim, evidence)
        results.append({
            "claim_id": claim["id"],
            "visit": claim["visit"],
            "text": claim["text"],
            "event": claim["event"],
            "evidence": evidence,
            "reason": reason,
            "status": "matched" if reason == "status_match" else "needs_review",
        })
    matched = sum(item["status"] == "matched" for item in results)
    return {
        "task": "cited_imaging_status_v1",
        "summary": {"total": len(results), "matched": matched, "needs_review": len(results) - matched},
        "results": results,
    }
