# Portfolio Publication Record

## Project

- Project name: Evidence-Bound AI Evaluation Harness
- Repository URL: https://github.com/ClinicBrain-ai/evidence-bound-ai-evaluation-harness
- Release URL: https://github.com/ClinicBrain-ai/evidence-bound-ai-evaluation-harness/releases/tag/v0.1.4
- Release version: v0.1.4
- Release date: 2026-06-12
- Release commit: f326cfc
- Repository owner / organization: ClinicBrain-ai

## Portfolio Positioning

Evidence-Bound AI Evaluation Harness is a portfolio-grade prototype for evaluating AI-generated healthcare-adjacent outputs against source evidence, missing context, uncertainty handling, source conflicts, scope boundaries, and human-review routing.

It focuses on reviewability and evidence alignment. It does not validate clinical correctness. It is a portfolio/research artifact, not a clinical tool.

## Why This Project Exists

AI-generated healthcare-adjacent outputs can sound fluent and confident even when they are unsupported, incomplete, uncertain, conflicting, or outside the intended workflow boundary.

This project demonstrates a structured way to inspect the relationship between AI output, source evidence, missing context, uncertainty, source conflicts, scope boundaries, and human-review needs.

## What Was Published

- README landing page with 60-second view.
- Hiring signal.
- Reviewer journey.
- Relationship to Clinical Review Packet Toolkit.
- Design-source summary.
- Evaluation workflow docs.
- Evaluation rubric.
- Failure taxonomy.
- Safety boundary.
- Non-claims.
- Version scope.
- Three synthetic examples.
- Walkthrough index.
- JSON Schema for evaluation reports.
- Positive and negative schema validation tests.
- Release draft / release readiness documentation.

## Validation Record

- Test command: `python3 -m pytest`
- Test result: `6 passed`
- What tests validate: schema structure and synthetic evaluation report conformance.
- What tests do not validate: clinical correctness, diagnosis, treatment, medical safety, HIPAA compliance, production readiness, or medical-device functionality.

## Safety Boundary

This project is not for clinical use.

It does not diagnose.
It does not recommend treatment.
It does not validate clinical correctness.
It does not assess medical safety.
It does not provide patient-facing advice.
It does not replace clinicians or licensed reviewers.
It does not claim HIPAA compliance.
It does not claim production readiness.
It does not function as a medical device.
It does not use real patient data.

## Relationship to Other Portfolio Repositories

```text
AI-generated output
  -> Evidence-Bound AI Evaluation Harness
  -> evaluation report
  -> Evidence-Bound Clinical Review Toolkit
  -> Clinical Review Packet
  -> human review decision + audit trail
  -> Evidence-Bound AI Workflows portfolio index
```

The Clinical Review Packet Toolkit focuses on converting AI-generated healthcare-adjacent outputs into evidence-linked, human-reviewable packets.

This Evaluation Harness sits one step before that, identifying unsupported claims, missing context, uncertainty gaps, source conflicts, scope-boundary issues, and review needs.

- Evaluation Harness: https://github.com/ClinicBrain-ai/evidence-bound-ai-evaluation-harness
- Clinical Review Toolkit: https://github.com/ClinicBrain-ai/evidence-bound-clinical-review-toolkit
- Portfolio Index: https://github.com/ClinicBrain-ai/evidence-bound-ai-workflows

## LinkedIn Featured Copy

Title:

Evidence-Bound AI Evaluation Harness

Description:

Portfolio project for evaluating AI-generated healthcare-adjacent outputs against source evidence, missing context, uncertainty, source conflicts, scope boundaries, and human-review needs. Uses synthetic examples only and does not validate clinical correctness.

## LinkedIn Announcement Copy

I published a new portfolio repo: Evidence-Bound AI Evaluation Harness.

It is a small, safety-bounded prototype for evaluating AI-generated healthcare-adjacent outputs against source evidence, missing context, uncertainty handling, source conflicts, scope boundaries, and human-review routing.

The goal is not to validate clinical correctness. It is to make the relationship between an AI output and its source material easier for a human reviewer to inspect.

This sits one step before my Clinical Review Packet Toolkit:

AI-generated output -> evaluation report -> Clinical Review Packet -> human review decision + audit trail

Built with synthetic examples, JSON Schema validation, and explicit non-claims around clinical use, diagnosis, treatment, HIPAA compliance, production readiness, and medical-device functionality.

Repo: https://github.com/ClinicBrain-ai/evidence-bound-ai-evaluation-harness

## Resume / Interview Use

- Designed a safety-bounded evaluation harness for reviewing AI-generated healthcare-adjacent outputs against source evidence, missing context, uncertainty, source conflicts, scope boundaries, and human-review routing.
- Built synthetic examples, JSON Schema validation, and positive / negative tests to demonstrate reviewability and evidence-alignment workflow design.
- Maintained explicit safety boundaries: not clinical use, not diagnosis, not treatment recommendation, not clinical correctness validation, not HIPAA compliance, not production-ready, and not medical-device functionality.

## Publication Status

- Public repo: yes
- GitHub release: yes
- LinkedIn Featured copy prepared: yes
- LinkedIn announcement copy prepared: yes
- Tests passing at publication: yes
- Safety boundary reviewed: yes
- Runtime behavior added: no
- CLI added: no
- Clinical claims added: no
- Real patient data used: no

## Next Safe Gate

Recommended next gate: `v0.2.0 Lightweight CLI Validator Planning Gate`

The next gate should plan CLI behavior before implementation and preserve the boundary that this project validates report structure and reviewability, not clinical correctness.
