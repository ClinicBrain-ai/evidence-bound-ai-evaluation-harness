import copy
import json
from pathlib import Path

import jsonschema
import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = PROJECT_ROOT / "schemas" / "evaluation_report.schema.json"
BASE_REPORT_PATH = (
    PROJECT_ROOT
    / "examples"
    / "case_001_missing_context"
    / "evaluation_report.json"
)


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


@pytest.fixture()
def schema() -> dict:
    return load_json(SCHEMA_PATH)


@pytest.fixture()
def valid_report() -> dict:
    return load_json(BASE_REPORT_PATH)


def assert_invalid(report: dict, schema: dict) -> None:
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=report, schema=schema)


def test_missing_report_id_is_invalid(valid_report: dict, schema: dict) -> None:
    report = copy.deepcopy(valid_report)
    del report["report_id"]

    assert_invalid(report, schema)


def test_invalid_claim_support_status_is_invalid(valid_report: dict, schema: dict) -> None:
    report = copy.deepcopy(valid_report)
    report["claim_evaluations"][0]["support_status"] = "clinically_correct"

    assert_invalid(report, schema)


def test_missing_human_review_required_is_invalid(valid_report: dict, schema: dict) -> None:
    report = copy.deepcopy(valid_report)
    del report["human_review_routing"]["review_required"]

    assert_invalid(report, schema)


def test_invalid_human_review_suggested_action_is_invalid(
    valid_report: dict, schema: dict
) -> None:
    report = copy.deepcopy(valid_report)
    report["human_review_routing"]["suggested_action"] = "recommend_treatment"

    assert_invalid(report, schema)


def test_invalid_scope_boundary_severity_is_invalid(
    valid_report: dict, schema: dict
) -> None:
    report = copy.deepcopy(valid_report)
    report["scope_boundary_flags"][0]["severity"] = "clinical_risk"

    assert_invalid(report, schema)
