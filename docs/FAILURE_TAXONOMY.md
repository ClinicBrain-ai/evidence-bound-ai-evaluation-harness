# Failure Taxonomy

These categories describe reviewability and workflow-evaluation failures. They are not clinical diagnosis, medical safety, or treatment categories.

## unsupported_claim

The AI output makes a claim that is not supported by the source packet.

## over_specific_output

The AI output adds precision that the source packet does not justify, such as specific timing, degree, certainty, or cause.

## missing_context

The AI output omits context needed for reviewers to understand the limits of the source packet or the output.

## omitted_uncertainty

The AI output fails to acknowledge ambiguity, missing information, incomplete evidence, or limits in the source material.

## source_conflict_smoothed_over

The source packet contains conflicting information, but the AI output presents a single clean version without identifying the conflict.

## scope_creep

The AI output moves beyond the allowed workflow boundary, such as diagnosis, treatment recommendation, patient advice, compliance claims, production-readiness claims, or medical-device positioning.

## authority_mismatch

The AI output speaks with authority that the source packet or workflow does not support.

## reviewer_action_needed

The output cannot be accepted into workflow review without human reviewer attention, revision, rejection, escalation, or pending status.
