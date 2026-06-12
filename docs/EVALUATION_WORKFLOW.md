# Evaluation Workflow

This workflow reviews AI-generated healthcare-adjacent outputs for evidence alignment, reviewability, uncertainty handling, source conflicts, scope boundaries, and human-review routing.

It does not determine clinical correctness.

## Steps

1. Input source packet

   The source packet contains the bounded material available to the reviewer. It may include synthetic notes, summaries, references, constraints, or workflow instructions.

2. AI-generated output

   The AI output is the text being reviewed. The harness evaluates how the output relates to the source packet.

3. Claim extraction

   Reviewers identify concrete claims made by the AI output, especially claims that summarize, interpret, prioritize, or imply action.

4. Evidence support review

   Each claim is classified as supported, partially supported, unsupported, or unclear based on the source packet.

5. Unsupported claim review

   Unsupported or over-specific claims are recorded with notes explaining why the source packet does not support them.

6. Omission / missing-context review

   The report flags important context that is absent, unknown, or not addressed by the AI output.

7. Uncertainty handling review

   The report checks whether uncertainty, limitations, missing information, or ambiguous source material were acknowledged.

8. Source conflict review

   The report records conflicts in the source packet and evaluates whether the AI output preserved, ignored, or smoothed over those conflicts.

9. Scope-boundary review

   The report flags places where the output exceeds the allowed workflow boundary. Severity is workflow severity, not patient severity or medical risk.

10. Human-review routing

   The report routes the output for workflow handling, such as revision before review, rejection, escalation, or pending review. Suggested action is workflow routing, not clinical advice.

11. Evaluation report creation

   The final report records findings in a structured JSON format that can be validated against the project schema.
