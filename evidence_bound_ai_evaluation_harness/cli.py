import argparse
import json
import sys
from pathlib import Path
from typing import List, Optional, Tuple

import jsonschema

from .fidelity import check_packet


SCOPE_MESSAGE = "Scope: structure and reviewability only; not clinical correctness."
SCHEMA_FILE = Path("schemas", "evaluation_report.schema.json")
PACKAGE_DIR = Path(__file__).resolve().parent
# A built wheel installs the repository's schemas directory inside the package.
DEFAULT_SCHEMA_PATH = PACKAGE_DIR / SCHEMA_FILE
if not DEFAULT_SCHEMA_PATH.is_file():
    DEFAULT_SCHEMA_PATH = PACKAGE_DIR.parent / SCHEMA_FILE


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _unique_fields(pairs: list) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON field: {key!r}")
        result[key] = value
    return result


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
            "Validate a review report or compare imaging-status claims with cited notes."
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

    check_parser = subparsers.add_parser(
        "check", help="Compare bilingual imaging-status claims with their cited notes."
    )
    check_parser.add_argument("packet_path", type=Path, help="Path to a fidelity packet JSON.")
    check_parser.add_argument("--json", action="store_true", help="Write the complete result as JSON.")

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "validate":
        exit_code, output = validate_report(args.report_path)
        print(output)
        return exit_code

    if args.command == "check":
        try:
            with args.packet_path.open(encoding="utf-8") as handle:
                packet = json.load(handle, object_pairs_hook=_unique_fields)
            result = check_packet(packet)
        except (OSError, ValueError) as error:
            print(f"ERROR: {error}", file=sys.stderr)
            return 2

        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            for row in result["results"]:
                print(f"{row['claim_id']}: {row['status']} ({row['reason']})")
            counts = result["summary"]
            print(f"{counts['matched']} matched; {counts['needs_review']} need review.")
            print("Scope: cited documentation of imaging status only.")
        return 1 if result["summary"]["needs_review"] else 0

    parser.print_help(sys.stderr)
    return 2
