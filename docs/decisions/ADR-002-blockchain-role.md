# ADR-002: Blockchain as Evidence and Provenance Layer

## Context

NerveNet may need tamper-evident records for custody transfers, agreements, decisions, outcomes, and evidence hashes.

## Decision

Use blockchain or ledger technology as a trusted evidence/provenance layer, not as the primary application database.

## Consequences

PostgreSQL remains responsible for application state and normal transactional workflows. Blockchain records can provide auditability and tamper evidence for selected events without slowing ordinary state management.

## Alternatives considered

- Blockchain as primary database: rejected because application state needs efficient updates and queries.
- No ledger: simpler, but loses a path to trusted cross-party evidence.
- Append-only database table only: useful as a baseline, but may not provide cross-party trust.
