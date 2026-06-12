# Clinical AI Review Harness

## Executive Summary

The Clinical AI Review Harness is a local-only review framework for checking whether AI-generated clinical-adjacent outputs remain grounded in source evidence, appropriately scoped, uncertainty-aware, and suitable for human review.

This is a portfolio/research artifact. It is designed to demonstrate evaluation thinking, not to serve as a clinical tool.

## Problem

AI-generated clinical-adjacent outputs can sound fluent, complete, and confident even when they drift beyond the available evidence. A polished output may contain unsupported claims, omit important uncertainty, blur source facts with interpretation, or exceed the workflow boundary.

Healthcare AI teams therefore need more than a final-answer review. They need a structured way to inspect the relationship between the AI output, the source packet, the reviewer criteria, and the workflow boundary.

## Why It Matters

In healthcare contexts, the risk is not only that an AI output is wrong. The risk is that it may be partly supported, partly unsupported, partly incomplete, and still persuasive.

A review harness helps teams ask:

- Which claims are directly supported by evidence?
- Which claims are plausible but unsupported?
- Which claims exceed the available case material?
- What did the output omit?
- Did it handle uncertainty appropriately?
- Did it stay inside the intended workflow?
- What should a human reviewer accept, correct, reject, or escalate?

This is the review layer that makes human-in-the-loop AI more meaningful.

## Approach

I designed the Clinical AI Review Harness as a repeatable review loop for evaluating AI-generated clinical-adjacent outputs against source material and reviewer criteria.

The harness is organized around:

- Input case packet
- AI-generated review output
- Evidence check
- Claim classification
- Omission review
- Uncertainty review
- Human reviewer judgment
- Revision notes
- Boundary assessment

The core design choice is to evaluate the relationship between claims and evidence, not merely the surface quality of generated text.

## Key Discoveries

1. **Fluency is not the same as grounding.** AI outputs can read well while making claims that are not clearly supported by the available source material.
2. **Omissions are evaluation failures too.** A review output can avoid obvious false statements while still failing to mention important uncertainty, missing information, or limitations.
3. **Evaluation needs reviewer action categories.** Human reviewers need a way to mark claims as acceptable, needs correction, unsupported, out of scope, or requires escalation.
4. **Revision behavior matters.** A safer workflow should not only identify issues; it should document how the output should be revised and why.
5. **The harness is strongest as a scaffold, not a standalone safety system.** It helps make review more systematic, but it does not certify clinical correctness or deployment readiness.

## What I Built / Produced

- A public case-study artifact explaining the Clinical AI Review Harness.
- A review-loop model for checking AI-generated clinical-adjacent outputs against source packets.
- A claim-evaluation framing for evidence alignment, overreach, omissions, uncertainty, and boundary assessment.
- A human review structure that supports acceptance, correction, rejection, revision, and escalation.
- Clear limitations that keep the artifact within local-only portfolio/research scope.

## What It Demonstrates

This case study demonstrates practical AI evaluation judgment in a healthcare context. It shows that I can think beyond whether an answer sounds good and toward whether each claim is supportable, bounded, reviewable, and appropriate for the workflow.

For healthcare AI teams, this is relevant to:

- AI output evaluation
- Clinical-adjacent documentation review
- Human-in-the-loop AI systems
- Healthcare AI product QA
- Responsible AI evaluation
- Clinical safety review workflows
- Reviewer rubric design
- Failure-mode documentation

## Hiring Signal

This project signals that I can work with clinical AI product, evaluation, and safety teams to design review workflows for AI-generated content. I can help define what reviewers should look for, how claims should be classified, and how outputs should be revised before they are trusted inside a workflow.

Strong fit signals:

- Claim-level evaluation mindset
- Evidence alignment and overreach detection
- Omission and uncertainty awareness
- Human reviewer workflow design
- Safety-boundary discipline
- Ability to communicate evaluation logic to engineering and non-engineering stakeholders

## Limitations

- The harness does not certify clinical correctness.
- It depends on reviewer expertise, source quality, and clear evaluation criteria.
- It has not yet been validated across large datasets, multiple clinical domains, or multiple reviewer groups.
- It is currently best understood as a local-only portfolio/research scaffold for structured review.
- It is not a production monitoring system, regulatory validation framework, clinical deployment artifact, or patient-facing system.

## Future Work

- Add a scoring rubric for evidence alignment, uncertainty handling, omissions, and scope control.
- Add inter-rater reliability tracking across multiple reviewers.
- Add a structured failure taxonomy for unsupported claims, overextension, missing caveats, outdated evidence, and authority mismatch.
- Add model-comparison views to evaluate different AI outputs against the same source packet.
- Add annotation-tool integration or a lightweight reviewer interface.
- Add audit-trail concepts showing how outputs were corrected over review cycles.
