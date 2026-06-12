# Walkthrough: Case 003 Source Conflict

## What The Source Packet Says

The synthetic source packet contains two statements: one says no medication allergies were reported, and another says allergy status was not confirmed. It does not say which source should control.

## What The AI Output Says

The AI output says the person has no medication allergies documented.

## What The Evaluation Harness Flags

- The claim is partially supported by one source.
- The output omits the conflicting source.
- The source conflict is smoothed over.
- The output resolves a conflict that should remain visible to a human reviewer.

## Why The Output Requires Review

A reviewer needs to see the unresolved conflict. The output should be revised or escalated for human review rather than presenting a clean conclusion.

## What The Report Does Not Decide

The report does not diagnose, recommend treatment, provide patient advice, assess medical safety, or determine clinical correctness.
