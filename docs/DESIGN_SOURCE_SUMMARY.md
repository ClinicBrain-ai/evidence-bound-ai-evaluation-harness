# Design Source Summary

This project is informed by `source/clinical-ai-review-harness.md`, which frames AI-generated clinical-adjacent text as something that must be reviewed against source evidence, workflow boundaries, uncertainty, and human reviewer judgment.

The source artifact contributes several core design principles:

- Fluency is not grounding. An AI output can read smoothly while making claims that are not clearly supported by the source packet.
- Omissions are evaluation failures. An output can avoid obvious false statements but still fail review by omitting relevant uncertainty, limitations, or missing information.
- Reviewer action categories matter. Reviewers need structured ways to mark claims as acceptable, unsupported, in need of correction, out of scope, or requiring escalation.
- Revision behavior matters. A useful review process should identify what needs to change and why, not only label a problem.
- The harness is a scaffold, not a standalone safety system. It helps organize review but does not certify clinical correctness, safety, or deployment readiness.
- Evaluation focuses on the relationship between claims and evidence, not surface text quality.

This repository turns those ideas into a repo-ready foundation with examples, JSON Schema validation, and safety-bounded documentation. It does not copy the source artifact as the final project; it uses the source as the conceptual foundation.
