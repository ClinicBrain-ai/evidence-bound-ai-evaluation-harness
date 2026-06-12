# Walkthrough Index

Use these walkthroughs to see the harness from a reviewer, hiring manager, or product team perspective.

Each case follows the same pattern:

1. Read the synthetic source packet.
2. Read the AI-generated output.
3. Inspect the evaluation report.
4. Use the walkthrough to understand what the harness flags and what it does not decide.

## Synthetic Cases

| Case | Pattern | Start Here |
| --- | --- | --- |
| Case 001 | Missing context | [Walkthrough](../examples/case_001_missing_context/WALKTHROUGH.md) |
| Case 002 | Unsupported specificity | [Walkthrough](../examples/case_002_unsupported_specificity/WALKTHROUGH.md) |
| Case 003 | Source conflict smoothed over | [Walkthrough](../examples/case_003_source_conflict/WALKTHROUGH.md) |

## What The Reviewer Sees

Before the harness, the reviewer sees an AI output that may sound complete but does not clearly show which statements are supported, unsupported, uncertain, missing context, or affected by source conflict.

After the harness, the reviewer sees a structured evaluation report with claim-level support labels, missing-context flags, uncertainty flags, source-conflict flags, scope-boundary flags, human-review routing, and revision guidance.

## What These Walkthroughs Do Not Decide

These walkthroughs do not diagnose, recommend treatment, validate clinical correctness, assess medical safety, provide patient-facing advice, claim HIPAA compliance, claim production readiness, or function as medical-device documentation.
