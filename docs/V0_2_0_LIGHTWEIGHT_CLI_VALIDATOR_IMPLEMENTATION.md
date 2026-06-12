# v0.2.0 Lightweight CLI Validator Implementation

## Purpose

The CLI validates a single evaluation report JSON against the project schema for local structure and reviewability checking.

It is a local convenience tool for confirming that an `evaluation_report.json` file follows the expected report shape. It does not evaluate clinical correctness.

## Commands

```bash
python -m evidence_bound_ai_evaluation_harness validate path/to/evaluation_report.json
```

```bash
evidence-bound-eval validate path/to/evaluation_report.json
```

## Output Behavior

For a valid report:

```text
PASS: evaluation report conforms to schema.
Scope: structure and reviewability only; not clinical correctness.
```

For a schema validation failure:

```text
FAIL: evaluation report does not conform to schema.
Error: <schema validation error>
Scope: structure and reviewability only; not clinical correctness.
```

For a missing file:

```text
ERROR: file not found: <path>
```

For invalid JSON:

```text
ERROR: invalid JSON: <path>
Error: <JSON parsing error>
```

For a missing schema:

```text
ERROR: schema file not found: <path>
```

## Exit Codes

- `0`: valid evaluation report.
- `1`: schema validation failure.
- `2`: usage error, missing file, invalid JSON, or missing schema.

## What It Validates

- The report file can be loaded as JSON.
- The project schema can be loaded.
- Required top-level fields are present.
- Required nested fields are present.
- Enum values match the schema.
- Claim evaluation entries follow the schema shape.
- Human-review routing fields follow the schema shape.
- Safety-boundary metadata is present.

## What It Does Not Validate

- Clinical correctness.
- Diagnosis.
- Treatment recommendation.
- Medical safety.
- HIPAA compliance.
- Production readiness.
- Medical-device functionality.
- Patient-facing advice.
- Clinician replacement.
- Real patient data handling.

## Safety Boundary

This is a local structure and reviewability validator only. It validates evaluation report shape against the JSON Schema and does not assess clinical correctness, diagnosis, treatment, medical safety, patient-facing advice, HIPAA compliance, production readiness, medical-device functionality, clinician replacement, or real patient data handling.

## Test Coverage

The CLI tests cover:

- Valid example report returns exit code `0`.
- Valid example output includes `PASS` and scope language.
- Invalid support status returns exit code `1`.
- Missing required field returns exit code `1`.
- Missing file returns exit code `2`.
- Invalid JSON returns exit code `2`.
- Missing schema returns exit code `2`.
- CLI validation does not modify the input file.
- `python -m evidence_bound_ai_evaluation_harness validate ...` works through subprocess.
- The console script entry point is defined.

The tests do not test clinical correctness, diagnosis, treatment, or medical safety validation.
