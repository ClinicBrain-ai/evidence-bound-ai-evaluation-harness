# Walkthrough: Case 002 Unsupported Specificity

## What The Source Packet Says

The synthetic source packet says a person asked about sensitivity near a recently repaired tooth. It does not include the repair date, tooth number, severity, duration, exam findings, or imaging.

## What The AI Output Says

The AI output says the sensitivity is in tooth 14, follows a filling completed last week, and is likely expected after the recent repair.

## What The Evaluation Harness Flags

- The general sensitivity statement is supported.
- The tooth number, procedure type, and timing are unsupported.
- The expectedness statement exceeds the source packet.
- The output does not preserve uncertainty around missing details.

## Why The Output Requires Review

The output adds specific facts and interpretive language that the source packet does not support. This makes it unsuitable for workflow review without substantial revision.

## What The Report Does Not Decide

The report does not diagnose, recommend treatment, provide patient advice, assess medical safety, or determine clinical correctness.
