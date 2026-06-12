# Walkthrough: Case 001 Missing Context

## What The Source Packet Says

The synthetic source packet says a person reported mild gum soreness during a scheduling call. It does not include duration, exam findings, medication history, or imaging.

## What The AI Output Says

The AI output states that the person has mild gum soreness and should be handled as a routine dental concern.

## What The Evaluation Harness Flags

- The gum soreness statement is supported.
- The routine-handling statement is unsupported.
- Symptom duration and exam findings are missing.
- The output does not acknowledge uncertainty caused by missing context.

## Why The Output Requires Review

The output turns limited source material into a workflow routing conclusion. A human reviewer needs a revised version that preserves the missing context.

## What The Report Does Not Decide

The report does not diagnose, recommend treatment, provide patient advice, assess medical safety, or determine clinical correctness.
