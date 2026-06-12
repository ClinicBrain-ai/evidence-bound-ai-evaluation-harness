import json
from pathlib import Path

import jsonschema


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = PROJECT_ROOT / "schemas" / "evaluation_report.schema.json"
EXAMPLES_ROOT = PROJECT_ROOT / "examples"


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def test_all_example_reports_validate_against_schema() -> None:
    schema = load_json(SCHEMA_PATH)
    report_paths = sorted(EXAMPLES_ROOT.glob("**/evaluation_report.json"))

    assert report_paths, "Expected at least one example evaluation report."

    for report_path in report_paths:
        report = load_json(report_path)
        jsonschema.validate(instance=report, schema=schema)
