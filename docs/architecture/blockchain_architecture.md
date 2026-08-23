# Blockchain Architecture

See [../../NERVENET_PRODUCT_SPEC.md](../../NERVENET_PRODUCT_SPEC.md), especially section 18.

Blockchain is a trusted evidence and provenance layer, not the primary application database. PostgreSQL stores operational application state. The ledger should store or anchor important evidence, agreements, decisions, outcomes, and hashes.

Candidate ledger events include shipment custody transfer, important state transition, decision record, outcome record, agreement, and evidence hash.

The initial implementation may use a local ledger abstraction before integrating a production blockchain network.
