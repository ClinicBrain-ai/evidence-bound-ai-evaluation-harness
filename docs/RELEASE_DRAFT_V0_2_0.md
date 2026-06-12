# v0.2.0 - Lightweight CLI Validator

## Summary

This release adds a lightweight local CLI validator for checking whether a single `evaluation_report.json` file conforms to the project's JSON Schema.

The CLI is intended for local structure and reviewability validation only.

It does not validate clinical correctness.

## What Changed

- Added package module `evidence_bound_ai_evaluation_harness`.
- Added module command:

```bash
python -m evidence_bound_ai_evaluation_harness validate path/to/evaluation_report.json
```

- Added console script:

```bash
evidence-bound-eval validate path/to/evaluation_report.json
```

- Added local single-report JSON Schema validation.
- Added CLI output with explicit scope language.
- Added documented exit codes.
- Added CLI tests.
- Added implementation documentation.
- Preserved existing schema validation tests.
- Preserved existing synthetic examples.

## Example Usage

```bash
python -m evidence_bound_ai_evaluation_harness validate examples/case_001_missing_context/evaluation_report.json
```

Expected output:

```text
PASS: evaluation report conforms to schema.
Scope: structure and reviewability only; not clinical correctness.
```

Optional console script usage:

```bash
evidence-bound-eval validate examples/case_001_missing_context/evaluation_report.json
```

## Exit Codes

- `0`: valid evaluation report.
- `1`: schema validation failure.
- `2`: usage error, missing file, invalid JSON, or missing schema.

## Validation

Test command:

```bash
python -m pytest
```

Test result:

```text
16 passed
```

Manual CLI checks:

```bash
python -m evidence_bound_ai_evaluation_harness validate examples/case_001_missing_context/evaluation_report.json
evidence-bound-eval validate examples/case_001_missing_context/evaluation_report.json
```

Both passed.

## Safety Boundary

This release validates structure and reviewability fields only.

It does not validate clinical correctness.
It does not diagnose.
It does not recommend treatment.
It does not assess medical safety.
It does not provide patient-facing advice.
It does not replace clinicians or licensed reviewers.
It does not claim HIPAA compliance.
It does not claim production readiness.
It does not function as a medical device.
It does not use real patient data.

## Not Included

- No clinical correctness validation.
- No diagnosis.
- No treatment recommendation.
- No medical safety validation.
- No HIPAA compliance tooling.
- No production deployment.
- No medical-device functionality.
- No patient-facing workflow.
- No real patient data.
- No scoring.
- No batch validation.
- No report generation.
- No external APIs.
- No network behavior.
- No web app.
- No GitHub Action.

## Recommended Next Step

Recommended next gate: `v0.2.0 GitHub Release Gate`

The next gate should create the tag and GitHub release using this draft, without adding features.
