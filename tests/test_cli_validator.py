import copy
import json
import shutil
import subprocess
import sys
from pathlib import Path

from evidence_bound_ai_evaluation_harness.cli import SCOPE_MESSAGE, validate_report


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BASE_REPORT_PATH = (
    PROJECT_ROOT
    / "examples"
    / "case_001_missing_context"
    / "evaluation_report.json"
)
PYPROJECT_PATH = PROJECT_ROOT / "pyproject.toml"


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: dict) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(value, handle)


def test_valid_example_report_returns_exit_code_zero() -> None:
    exit_code, output = validate_report(BASE_REPORT_PATH)

    assert exit_code == 0
    assert "PASS: evaluation report conforms to schema." in output
    assert "not clinical correctness" in output


def test_invalid_support_status_returns_exit_code_one(tmp_path: Path) -> None:
    report = copy.deepcopy(load_json(BASE_REPORT_PATH))
    report["claim_evaluations"][0]["support_status"] = "clinically_correct"
    report_path = tmp_path / "evaluation_report.json"
    write_json(report_path, report)

    exit_code, output = validate_report(report_path)

    assert exit_code == 1
    assert "FAIL: evaluation report does not conform to schema." in output
    assert "Error:" in output
    assert SCOPE_MESSAGE in output


def test_missing_required_field_returns_exit_code_one(tmp_path: Path) -> None:
    report = copy.deepcopy(load_json(BASE_REPORT_PATH))
    del report["report_id"]
    report_path = tmp_path / "evaluation_report.json"
    write_json(report_path, report)

    exit_code, output = validate_report(report_path)

    assert exit_code == 1
    assert "FAIL: evaluation report does not conform to schema." in output
    assert "Error:" in output


def test_missing_file_returns_exit_code_two(tmp_path: Path) -> None:
    report_path = tmp_path / "missing_report.json"

    exit_code, output = validate_report(report_path)

    assert exit_code == 2
    assert f"ERROR: file not found: {report_path}" in output


def test_invalid_json_returns_exit_code_two(tmp_path: Path) -> None:
    report_path = tmp_path / "evaluation_report.json"
    report_path.write_text("{invalid json", encoding="utf-8")

    exit_code, output = validate_report(report_path)

    assert exit_code == 2
    assert f"ERROR: invalid JSON: {report_path}" in output


def test_missing_schema_returns_exit_code_two(tmp_path: Path) -> None:
    schema_path = tmp_path / "missing.schema.json"

    exit_code, output = validate_report(BASE_REPORT_PATH, schema_path=schema_path)

    assert exit_code == 2
    assert f"ERROR: schema file not found: {schema_path}" in output


def test_cli_does_not_modify_input_file(tmp_path: Path) -> None:
    report_path = tmp_path / "evaluation_report.json"
    original_bytes = BASE_REPORT_PATH.read_bytes()
    report_path.write_bytes(original_bytes)

    exit_code, _ = validate_report(report_path)

    assert exit_code == 0
    assert report_path.read_bytes() == original_bytes


def test_python_module_validate_command_works_through_subprocess() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "evidence_bound_ai_evaluation_harness",
            "validate",
            str(BASE_REPORT_PATH),
        ],
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "PASS: evaluation report conforms to schema." in result.stdout
    assert "not clinical correctness" in result.stdout


def test_console_script_entry_point_is_defined() -> None:
    pyproject = PYPROJECT_PATH.read_text(encoding="utf-8")

    assert "[project.scripts]" in pyproject
    assert (
        'evidence-bound-eval = "evidence_bound_ai_evaluation_harness.cli:main"'
        in pyproject
    )


def test_console_script_works_when_installed() -> None:
    command_path = shutil.which("evidence-bound-eval")
    if command_path is None:
        return

    result = subprocess.run(
        [
            command_path,
            "validate",
            str(BASE_REPORT_PATH),
        ],
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "PASS: evaluation report conforms to schema." in result.stdout
    assert "not clinical correctness" in result.stdout
