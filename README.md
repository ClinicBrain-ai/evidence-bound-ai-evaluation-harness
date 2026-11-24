# Evidence-Bound AI Evaluation Harness

Evidence-Bound AI Evaluation Harness is a portfolio-grade prototype for evaluating AI-generated healthcare-adjacent outputs against source evidence, missing context, uncertainty handling, scope boundaries, and human-review needs.

## 60-Second View

- Reviews AI outputs against bounded source packets.
- Flags unsupported claims, missing context, omitted uncertainty, source conflicts, and scope-boundary issues.
- Produces schema-validated evaluation reports for human-review routing.
- Uses only synthetic examples.
- Evaluates reviewability and evidence alignment, not clinical correctness.

## Try the cited imaging-status check (v0.3.0)

A synthetic note says **預計下次回診拍攝 36 根尖片。** (planned for the next visit).
A summary cites that exact note and says **已拍攝 36 根尖片。** (already taken).
The source ID exists. The wording changes the documented status of the event.
The `check` command reads the two sentences and routes that claim to review.

From the repository root, with Python 3.9 or later:

```bash
python -m pip install -e .
python -m evidence_bound_ai_evaluation_harness check benchmarks/temporal_fidelity/packet.json --json
```

The example intentionally exits with **1** because 12 of its 18 claims need review.
Each result includes the claim, its visit, its normalized event and state, every cited excerpt,
and the reason for the decision. Omit `--json` for a short per-claim summary.
Exit **0** means all claims matched on the checked dimensions; **2** means the input could not be read or validated.

### What a packet contains

```json
{
  "sources": [{"id": "S1", "visit": "V1", "text": "預計下次回診拍攝 36 根尖片。"}],
  "claims": [{"id": "C1", "visit": "V1", "text": "已拍攝 36 根尖片。", "citations": ["S1"]}]
}
```

This returns `needs_review / status_mismatch`: the claim is `completed`; source S1 is `planned`.
Replace the claim text with `下回安排拍攝 36 根尖片。` and the result becomes `matched / status_match`.
Visit IDs refer to the encounter whose documentation is being summarized. A note from V2
cannot prove that an event was already complete as documented at V1. The caller supplies
these IDs and the citations. Multiple cited notes must agree on visit, tooth and status.
Uncited notes are outside the check, even when their wording would support the claim.

### Run the contrast set

```bash
python -m benchmarks.temporal_fidelity.score
```

| Check on the 18 synthetic claims | Incorrectly passed | Unnecessarily sent to review | Decisions agreeing with the fixture labels |
| --- | ---: | ---: | ---: |
| Nonempty citations, all IDs exist | 10 | 0 | 8/18 |
| Cited imaging-status check | 0 | 0 | 18/18 |

The ID-only rule is a comparison baseline. The original `validate` command checks a different artifact: a reviewer-authored report against its schema. Expected labels live in [expected.json](benchmarks/temporal_fidelity/expected.json), separate from the [input packet](benchmarks/temporal_fidelity/packet.json). The set includes planned/completed, not done/documentation unknown, a later visit, a different tooth, conflicts, and unsupported wording.

This is a deterministic, local check for a closed set of English and Traditional Chinese
sentences about permanent-tooth periapical imaging. It compares four documentation
states: `planned`, `completed`, `not_done`, and `unknown`. The [recognizer](evidence_bound_ai_evaluation_harness/event_text.py)
lists all nine sentence templates. Unrecognized wording routes to human review. A match
applies only to the cited event, visit and status. These fixture results do not estimate
performance on free-text clinical notes or establish that the event occurred.

## Hiring Signal

This project demonstrates practical AI evaluation judgment for healthcare-adjacent workflows: claim-level review, evidence alignment, uncertainty handling, failure taxonomy design, human-review routing, and safety-boundary discipline.

## Reviewer Journey

A hiring manager, reviewer, or product team can read this repo as a small workflow story:

1. Start with a bounded synthetic source packet.
2. Compare it with a plausible AI-generated output.
3. Inspect the evaluation report to see which claims are supported, unsupported, missing context, uncertainty-sensitive, conflict-sensitive, or outside workflow scope.
4. Use human-review routing to decide whether the output should be revised, rejected, escalated, accepted for workflow review, or left pending.

Before the harness, a reviewer sees fluent text and has to manually infer what is grounded, missing, uncertain, or out of scope.

After the harness, a reviewer sees a structured report that separates source-supported claims from review issues and keeps workflow routing visible.

## Why This Exists

AI-generated healthcare-adjacent text can sound fluent and confident even when it is only partly grounded in source material. This project creates a structured, safety-bounded way to review whether an output is evidence-aligned, appropriately uncertain, scoped to the workflow, and ready for human review.

This project evaluates reviewability and evidence alignment. It does not validate clinical correctness.

## Before / After

Before:
AI-generated healthcare-adjacent text may sound fluent and confident, but reviewers may not know which claims are supported, what context is missing, whether uncertainty was handled properly, or whether the output exceeds the workflow boundary.

After:
The same output is evaluated through a structured report that records supported claims, unsupported claims, missing context, uncertainty flags, source conflicts, scope-boundary issues, and human-review routing.

## Core Workflow

Source packet -> AI-generated output -> Claim/evidence review -> Missing context review -> Uncertainty review -> Source conflict review -> Scope-boundary review -> Human-review routing -> Evaluation report

## What This Project Evaluates

- Evidence support for claims made in an AI output
- Unsupported or over-specific claims
- Missing context that affects reviewability
- Omitted uncertainty or overstated confidence
- Source conflicts that were ignored or smoothed over
- Scope-boundary issues
- Human-review routing needs
- Revision focus for workflow review

## What This Project Does Not Evaluate

- Clinical correctness
- Medical safety
- Diagnosis
- Treatment recommendations
- Patient-facing advice
- HIPAA compliance
- Production readiness
- Medical-device functionality

## Synthetic Examples

- `case_001_missing_context`: plausible output with important context absent.
- `case_002_unsupported_specificity`: output becomes more specific than the source supports.
- `case_003_source_conflict`: source conflict is smoothed over by the AI output.

See [docs/WALKTHROUGH_INDEX.md](docs/WALKTHROUGH_INDEX.md) for a simple guide to the three case walkthroughs.

All examples are synthetic, de-identified, and healthcare-adjacent or dental-adjacent. They are not clinical cases and do not use real patient data.

## Why Schema Validation Matters

Schema validation makes the evaluation report reviewable as a consistent artifact. It checks that each synthetic report includes the expected workflow fields, allowed labels, routing values, and safety-boundary metadata.

The schema does not validate clinical correctness, diagnosis, treatment, medical safety, compliance, production readiness, or medical-device functionality.

- [v0.2.0 Lightweight CLI Validator Plan](docs/V0_2_0_LIGHTWEIGHT_CLI_VALIDATOR_PLAN.md) - planning document for the local schema validator CLI.
- [v0.2.0 Lightweight CLI Validator Implementation](docs/V0_2_0_LIGHTWEIGHT_CLI_VALIDATOR_IMPLEMENTATION.md) - implementation notes and command behavior.
- [v0.2.0 Release Draft](docs/RELEASE_DRAFT_V0_2_0.md) - release notes for the lightweight local CLI validator.

## CLI Validator

Validate a single evaluation report JSON against the project schema:

```bash
python -m evidence_bound_ai_evaluation_harness validate examples/case_001_missing_context/evaluation_report.json
```

Expected output:

```text
PASS: evaluation report conforms to schema.
Scope: structure and reviewability only; not clinical correctness.
```

After editable install, the packaged command is also available:

```bash
evidence-bound-eval validate examples/case_001_missing_context/evaluation_report.json
```

The CLI validates JSON report structure and reviewability fields against the schema. It does not validate clinical correctness, diagnosis, treatment, medical safety, HIPAA compliance, production readiness, or medical-device functionality.

## Release Readiness

See [docs/RELEASE_DRAFT_V0_1_X.md](docs/RELEASE_DRAFT_V0_1_X.md) for a GitHub release-note draft and release safety boundary for the v0.1.x foundation.

- [Portfolio Publication Record](docs/PORTFOLIO_PUBLICATION_RECORD.md) - release, validation, LinkedIn, and portfolio-use record for v0.1.4.

## Relationship To Clinical Review Packet Toolkit

The companion [Evidence-Bound Clinical Review Toolkit](https://github.com/ClinicBrain-ai/evidence-bound-clinical-review-toolkit) focuses on converting AI-generated healthcare-adjacent outputs into evidence-linked, human-reviewable Clinical Review Packets.

This project focuses on the layer before that: evaluating the AI output to identify unsupported claims, missing context, uncertainty gaps, source conflicts, scope-boundary issues, and review needs.

```text
AI-generated output
  -> Evidence-Bound AI Evaluation Harness
  -> evaluation report: unsupported claims / missing context / source conflicts / scope flags
  -> Clinical Review Packet
  -> human review decision + audit trail
```

In short: this repository evaluates whether an AI output is ready to become a review packet; the toolkit turns bounded material into the packet reviewers inspect. Both repositories stay within reviewability, evidence alignment, and human-review workflow boundaries.

## Test Instructions

```bash
python3 -m pip install -r requirements-dev.txt
python3 -m pytest
```

The tests exercise report validation, sentence recognition, the CLI and synthetic citation comparisons. To reproduce the labeled contrast set separately, run the scoring command above.

## Safety Boundary

This is not a clinical decision tool. It is not for clinical use, diagnosis, treatment recommendation, medical safety assessment, patient-facing advice, clinician replacement, HIPAA compliance, production deployment, medical-device use, or real patient data.
