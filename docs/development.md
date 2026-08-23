# NerveNet Development Guide

## Principles

1. No hardcoded environment-specific paths.
2. No secrets in source code.
3. Configuration must come from environment/configuration files.
4. Services should communicate through defined interfaces.
5. Every major component must be testable independently.
6. Production and development environments should use the same application code.
7. ML models must be versioned and accessed through a model abstraction.
8. Blockchain functionality must be accessed through a blockchain abstraction.