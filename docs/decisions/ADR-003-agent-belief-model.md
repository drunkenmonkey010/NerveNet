# ADR-003: Agent Beliefs Separate from World State

## Context

Agents may observe different evidence and have different histories with the same logistics entity.

## Decision

Represent agent beliefs separately from world state.

## Consequences

NerveNet can model uncertainty, disagreement, recency, confidence, and agent-specific experience. This adds complexity, but it is central to the product concept.

## Alternatives considered

- Single global score per entity: simpler, but cannot represent differing perspectives.
- Store only raw events: auditable, but does not directly support decision-making.
- Treat beliefs as model outputs only: too narrow, because beliefs also require source, context, and memory.
