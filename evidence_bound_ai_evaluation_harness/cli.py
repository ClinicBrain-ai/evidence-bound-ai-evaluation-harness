import argparse
import json
import sys
from pathlib import Path
from typing import List, Optional, Tuple

import jsonschema


SCOPE_MESSAGE = "Scope: structure and reviewability only; not clinical correctness."
DEFAULT_SCHEMA_PATH = (
    Path(__file__).resolve().parents[1] / "schemas" / "evaluation_report.schema.json"
)


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_schema(schema_path: Path) -> dict:
    return load_json(schema_path)


def validate_report(
    report_path: Path, schema_path: Optional[Path] = None
) -> Tuple[int, str]:
    selected_schema_path = schema_path or DEFAULT_SCHEMA_PATH

    if not report_path.exists():
        return 2, f"ERROR: file not found: {report_path}"

    if not selected_schema_path.exists():
        return 2, f"ERROR: schema file not found: {selected_schema_path}"

    try:
        report = load_json(report_path)
    except json.JSONDecodeError as error:
        return 2, f"ERROR: invalid JSON: {report_path}\nError: {error}"

    schema = load_schema(selected_schema_path)
    validator = jsonschema.Draft202012Validator(schema)

    try:
        validator.validate(report)
    except jsonschema.ValidationError as error:
        return (
            1,
            "FAIL: evaluation report does not conform to schema.\n"
            f"Error: {error.message}\n"
            f"{SCOPE_MESSAGE}",
        )

    return (
        0,
        "PASS: evaluation report conforms to schema.\n"
        f"{SCOPE_MESSAGE}",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="evidence-bound-eval",
        description=(
            "Validate an evaluation report JSON against the local project schema."
        ),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate a single evaluation_report.json file.",
    )
    validate_parser.add_argument(
        "report_path",
        type=Path,
        help="Path to the evaluation_report.json file to validate.",
    )

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "validate":
        exit_code, output = validate_report(args.report_path)
        print(output)
        return exit_code

    parser.print_help(sys.stderr)
    return 2
