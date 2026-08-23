# Data Architecture

PostgreSQL is the primary application database. It stores operational state and supports transactional consistency for entities such as organizations, future users, agents, shipments, observations, decisions, outcomes, and permissions.

Future data domains should preserve these distinctions:

- Facts: current or historical operational state.
- Evidence: sourced observations with provenance.
- Beliefs: agent-specific estimates derived from evidence and history.
- Predictions: versioned model outputs.
- Decisions: selected actions and reasoning inputs.
- Outcomes: observed results after actions.
- Ledger references: hashes or identifiers for trusted evidence records.

Data must be organization-scoped for multi-tenancy unless a future cross-tenant sharing model is explicitly specified.
