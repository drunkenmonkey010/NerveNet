# Memory System

See [../../NERVENET_PRODUCT_SPEC.md](../../NERVENET_PRODUCT_SPEC.md), especially section 8.

The conceptual memory architecture includes event memory, interaction memory, outcome memory, episodic memory, semantic memory, and agent-specific history.

Memory should support learning without treating every raw signal as permanently important. Some records should persist for auditability, some should aggregate into summaries, and some may decay when they lose operational value. Tenant boundaries and permissions must apply to all memory access.

This task does not implement memory storage.
