# Evaluation Rubric

This rubric evaluates reviewability and evidence alignment. It does not evaluate clinical correctness, medical safety, diagnosis, or treatment.

## evidence_support

What it checks: Whether claims in the AI output are supported by the source packet.

What it does not check: Whether the source packet itself is clinically correct or complete.

Example signals: Direct quote support, source-backed paraphrase, partial support, unclear support, no matching source evidence.

Safety boundary: Support status is an evidence-alignment label, not a clinical truth label.

## unsupported_claims

What it checks: Whether the AI output adds claims not present in or inferable from the source packet.

What it does not check: Whether the unsupported claim would be medically true in the real world.

Example signals: New causality, new severity, new timing, new recommendation, unsupported certainty.

Safety boundary: The harness flags unsupportedness, not medical accuracy.

## missing_context_flags

What it checks: Whether important review context is absent, unknown, or omitted from the AI output.

What it does not check: Whether missing context would change care or treatment.

Example signals: Missing timeframe, missing source date, missing reviewer role, missing limitation, missing data availability note.

Safety boundary: Missing context is a reviewability issue, not a diagnosis or safety determination.

## uncertainty_flags

What it checks: Whether the AI output acknowledges ambiguity, incomplete evidence, limitations, or unresolved questions.

What it does not check: Whether uncertainty is clinically acceptable.

Example signals: Overconfident wording, omitted caveats, failure to mention unknowns, unsupported resolution of ambiguity.

Safety boundary: The harness evaluates uncertainty handling in text, not clinical risk.

## source_conflict_flags

What it checks: Whether conflicting source statements are preserved for review rather than hidden or smoothed over.

What it does not check: Which source is clinically correct.

Example signals: Two dates conflict, two summaries disagree, source says symptoms present and absent, output chooses one without noting conflict.

Safety boundary: Conflict flags identify review needs, not authoritative clinical conclusions.

## scope_boundary_flags

What it checks: Whether the AI output stays within the allowed workflow boundary.

What it does not check: Whether an out-of-scope statement is medically safe or unsafe.

Example signals: Diagnosis, treatment recommendation, patient instruction, compliance claim, production-readiness claim, medical-device positioning.

Safety boundary: Severity is workflow severity, not patient severity or medical risk.

## human_review_routing

What it checks: Whether the output should be accepted for workflow review, revised, rejected, escalated, or left pending.

What it does not check: What a clinician should decide.

Example signals: Review required, revision needed, escalation needed for unsupported claims, rejection for scope overreach.

Safety boundary: Suggested action is workflow routing, not clinical advice.

## revision_guidance

What it checks: What should be revised to make the output more evidence-bound and reviewable.

What it does not check: How to diagnose, treat, or advise a patient.

Example signals: Remove unsupported specificity, add missing uncertainty, preserve source conflict, narrow the scope.

Safety boundary: Revision guidance is documentation guidance, not medical guidance.
