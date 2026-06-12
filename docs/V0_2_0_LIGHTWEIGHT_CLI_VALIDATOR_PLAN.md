# v0.2.0 Lightweight CLI Validator Plan

Implementation status: Implemented in v0.2.0 as a local single-report schema validator.

## Purpose

The planned CLI is intended to help locally validate whether an `evaluation_report.json` file conforms to the project's JSON Schema and contains the expected reviewability fields.

The CLI is for local portfolio, developer, and reviewer workflow support only. It is a convenience layer for checking report structure, not a clinical validation tool.

## Planned Command Shape

Possible future command shape:

```bash
python -m evidence_bound_ai_evaluation_harness validate path/to/evaluation_report.json
```

Optional future packaged entry point:

```bash
evidence-bound-eval validate path/to/evaluation_report.json
```

At the time this plan was written, these commands were not implemented yet. The commands are now implemented in v0.2.0 as a local single-report schema validator.

## What The CLI Should Validate

- JSON file can be loaded.
- JSON Schema can be loaded.
- Report conforms to `schemas/evaluation_report.schema.json`.
- Required top-level fields are present.
- Allowed enum values are respected.
- `claim_evaluations` entries follow schema shape.
- `human_review_routing` contains required workflow routing fields.
- Safety boundary field is present.
- Output is structurally reviewable.

## What The CLI Must Not Validate

- Clinical correctness.
- Diagnosis.
- Treatment recommendation.
- Patient safety.
- Medical safety.
- Real-world clinical appropriateness.
- HIPAA compliance.
- Production readiness.
- Medical-device functionality.
- Whether a reviewer's decision is medically correct.
- Whether an AI output is safe for clinical use.
- Real patient data.

## Proposed Output Behavior

For valid report:

```text
PASS: evaluation report conforms to schema.
Scope: structure and reviewability only; not clinical correctness.
```

For invalid report:

```text
FAIL: evaluation report does not conform to schema.
Error: <jsonschema validation error>
Scope: structure and reviewability only; not clinical correctness.
```

For missing file:

```text
ERROR: file not found: <path>
```

For invalid JSON:

```text
ERROR: invalid JSON: <path>
```

For missing schema:

```text
ERROR: schema file not found: schemas/evaluation_report.schema.json
```

## Exit Code Plan

Proposed exit codes for future implementation:

- `0`: valid evaluation report.
- `1`: schema validation failure.
- `2`: usage error, missing file, invalid JSON, or missing schema.

These are proposed codes for a future implementation gate.

## Proposed Implementation Boundaries

The future implementation should be minimal and local-only.

It should probably use:

- Python standard library:
  - `argparse`
  - `json`
  - `pathlib`
  - `sys`
- Existing dev dependency:
  - `jsonschema`

It should not require network access.
It should not call external APIs.
It should not process real patient data.
It should not introduce clinical logic.
It should not add scoring logic in v0.2.0 unless separately planned.
It should not modify input files.

## Proposed File Structure For Future Implementation

Possible future structure:

```text
evidence_bound_ai_evaluation_harness/
├── __init__.py
├── __main__.py
└── cli.py
```

This structure was not created during the planning gate. It was created later during the v0.2.0 implementation gate.

Tests could later be added under:

```text
tests/test_cli_validator.py
```

## Planned Tests For Future Implementation

- Valid example report returns exit code `0`.
- Invalid support status returns exit code `1`.
- Missing required field returns exit code `1`.
- Missing file returns exit code `2`.
- Invalid JSON returns exit code `2`.
- CLI output includes "not clinical correctness".
- CLI does not modify input files.
- All existing schema tests continue to pass.

These tests were documentation-only in the planning gate. They were added later during the v0.2.0 implementation gate.

## Safety Boundary For CLI

The future CLI must remain a structure and reviewability validator only.

It must not be described as:

- Clinical AI.
- Diagnostic software.
- Treatment recommendation software.
- Medical safety validation.
- Clinical correctness validation.
- HIPAA compliance tooling.
- Production monitoring.
- Medical-device functionality.
- Patient-facing advice.
- Clinician replacement.

## v0.2.0 Acceptance Criteria

- CLI validates a single evaluation report JSON against the existing schema.
- CLI prints explicit scope language.
- CLI returns documented exit codes.
- CLI handles invalid JSON and missing files cleanly.
- CLI has tests for valid, invalid, missing, and invalid JSON cases.
- Existing schema tests continue to pass.
- README documents the CLI without clinical overclaiming.
- CHANGELOG records runtime behavior addition clearly.
- Safety boundary remains explicit.

## Intentionally Deferred

- Batch directory validation.
- Scoring.
- Reviewer UI.
- Web app.
- API service.
- GitHub Action.
- Automatic report generation.
- Clinical correctness evaluation.
- Medical safety evaluation.
- Real patient data handling.
- EHR integration.
- HIPAA or compliance features.
- Production deployment.

## Recommended Next Gate

Recommended next gate after implementation: `v0.2.0 CLI Release Readiness Gate`

The implementation gate began after reviewing this plan and is now complete in v0.2.0.
