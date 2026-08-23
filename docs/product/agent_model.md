# Agent Model

See [../../NERVENET_PRODUCT_SPEC.md](../../NERVENET_PRODUCT_SPEC.md), especially sections 4 and 5.

An agent is a modeled logistics entity with identity, state, goals, constraints, capabilities, observations, actions, memory, beliefs, and relationships. Agents are not just database rows. Rows preserve facts; agents use facts and evidence to form context-specific beliefs and decisions.

Currently planned agent types include Shipment Agent, Carrier Agent, Warehouse Agent, and Customer Agent. Future/proposed types include Vehicle Agent, Hub Agent, and Route/Infrastructure Agent.

Implementation note: this repository should introduce agent tables and services only after the first MVP schema is explicitly designed.
