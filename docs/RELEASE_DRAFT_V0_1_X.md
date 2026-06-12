# Release Draft: v0.1.x Foundation

## Summary

Evidence-Bound AI Evaluation Harness v0.1.x is a portfolio-grade documentation, schema, and example foundation for evaluating AI-generated healthcare-adjacent outputs against source evidence, missing context, uncertainty handling, source conflicts, scope boundaries, and human-review routing.

This release series focuses on reviewability and evidence alignment. It does not add runtime behavior or a CLI.

## Included

- README landing page with a 60-second view, hiring signal, reviewer journey, safety boundary, and relationship to the Clinical Review Packet Toolkit.
- Design-source summary preserving the conceptual foundation from the original Clinical AI Review Harness artifact.
- Evaluation workflow, rubric, failure taxonomy, safety-boundary, non-claims, and version-scope docs.
- Three synthetic example cases:
  - missing context
  - unsupported specificity
  - source conflict smoothed over
- Walkthrough index linking the three synthetic examples.
- JSON Schema for evaluation reports.
- Positive and negative schema validation tests.

## Validation

Expected validation command:

```bash
python3 -m pip install -r requirements-dev.txt
python3 -m pytest
```

The tests validate schema structure and example report conformance only. They do not validate clinical correctness.

## Release Safety Boundary

This release is not for clinical use. It does not diagnose, recommend treatment, validate clinical correctness, assess medical safety, provide patient-facing advice, replace clinicians or licensed reviewers, claim HIPAA compliance, claim production readiness, function as a medical device, or use real patient data.

The release should be described as a portfolio-grade prototype for reviewability, evidence alignment, and human-review workflow.

## Not Included

- Runtime behavior.
- CLI.
- Real patient data.
- Clinical deployment.
- HIPAA or compliance claims.
- Production-readiness claims.
- Medical-device functionality.

## Suggested GitHub Release Text

Evidence-Bound AI Evaluation Harness v0.1.x establishes a documentation, schema, and synthetic-example foundation for reviewing AI-generated healthcare-adjacent outputs against bounded source material.

The release includes a reviewer journey, walkthrough index, three synthetic cases, a JSON Schema for evaluation reports, and tests that validate example report structure.

This is a portfolio/research artifact for reviewability and evidence alignment only. It is not for clinical use and does not validate clinical correctness.
