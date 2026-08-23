# System Architecture

See [../../NERVENET_PRODUCT_SPEC.md](../../NERVENET_PRODUCT_SPEC.md), especially section 22.

Conceptual system flow:

Frontend -> API -> Services -> Database -> ML services -> Agent system -> Digital twin -> Blockchain

Boundaries:

- Frontend: control tower user experience.
- API: validation, authentication boundary, request orchestration.
- Services: business behavior and product rules.
- Repositories: persistence access.
- Database: application state.
- ML services: prediction and model inference.
- Agent system: state, memory, beliefs, relationships, and decisions.
- Digital twin: simulation of candidate actions.
- Blockchain: trusted evidence and provenance.

Current code implements the API, service, repository, database, migration, and Organization foundation only.
