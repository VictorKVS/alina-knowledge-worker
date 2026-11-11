# AK-01 — Failure, Retry and Idempotency Rules

## Retryable
- transient model/provider failure
- transient database/network error
- indexing timeout
- temporary tool unavailability

## Non-retryable without intervention
- invalid source format
- schema violation after max repair attempts
- source hash mismatch
- evidence-policy violation
- unauthorized access
- destructive alias merge ambiguity

## Idempotency
Each job stage receives:
- job_id
- stage_id
- input_hash
- policy_version
- idempotency_key

Same input_hash + policy_version must not create duplicate knowledge units.

## Partial failure
Stages persist checkpoints.
A failed downstream stage must not require re-ingesting unchanged sources.

## Human gate
Ambiguous destructive changes:
- entity merge
- core knowledge replacement
- evidence downgrade/upgrade
- critical procedure replacement
require reviewer approval.
