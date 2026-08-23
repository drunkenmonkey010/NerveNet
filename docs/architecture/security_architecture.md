# Security Architecture

See [../../NERVENET_PRODUCT_SPEC.md](../../NERVENET_PRODUCT_SPEC.md), especially sections 20 and 21.

Security requirements:

- Environment-based configuration.
- No secrets in source control.
- Authentication and authorization.
- Organization-level multi-tenancy.
- Audit logging for important actions.
- Data isolation.
- Input validation.
- Model input/output validation.
- Blockchain or ledger identity for trusted evidence.

Future schemas and services should make organization ownership explicit so permissions can be enforced consistently.
