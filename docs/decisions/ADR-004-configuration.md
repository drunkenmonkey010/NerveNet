# ADR-004: Externalized Environment Configuration

## Context

NerveNet runs across local development, tests, containers, and future deployment environments. Configuration values include database URLs, host/port settings, storage paths, provider choices, and secrets.

## Decision

Externalize environment-specific configuration through environment variables and `.env` files loaded by `pydantic-settings`.

## Consequences

The codebase avoids hardcoded machine paths and secrets. Deployments can configure infrastructure without code changes. `.env` must remain ignored, while `.env.example` documents expected settings.

## Alternatives considered

- Hardcoded settings: rejected because it is insecure and environment-specific.
- Multiple checked-in config files with secrets: rejected because it risks credential leakage.
- Runtime-only manual configuration: possible, but harder for local development.
