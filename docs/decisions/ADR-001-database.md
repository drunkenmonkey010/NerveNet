# ADR-001: PostgreSQL as Primary Application Database

## Context

NerveNet needs a reliable transactional store for organizations and future operational entities such as users, agents, shipments, observations, decisions, outcomes, and permissions.

## Decision

Use PostgreSQL as the primary application database.

## Consequences

PostgreSQL provides transactional consistency, mature indexing, relational constraints, migrations, and broad operational support. Application state can be queried and evolved through versioned schemas.

## Alternatives considered

- Document database: flexible, but weaker fit for relational integrity and multi-entity transactional workflows.
- Blockchain as primary database: poor fit for high-volume mutable application state.
- Files or local storage: not appropriate for multi-user, multi-tenant production services.
