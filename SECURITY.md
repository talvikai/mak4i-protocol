# Security Policy

## Current Scope (Phase 0)

As of Phase 0, this repository contains protocol documentation, the
draft specification, artifact metadata (JSON), and the
`frameworks/wd-docx-framework` document-generation tool. There is no
hosted API, registry, or production service yet — that begins in
Phase 2 (see [ROADMAP.md](ROADMAP.md)). This policy will be expanded
once a hosted service exists.

## Reporting a Vulnerability

If you find a security issue in anything currently in this repository —
for example, an issue in `frameworks/wd-docx-framework`, or a problem
with how an artifact's metadata could be misused — please report it
privately rather than opening a public GitHub issue.

**Email: hello@talvik.ai**

Include:
- A description of the issue and where it is (file, artifact, or
  component)
- Steps to reproduce, if applicable
- The potential impact, as best you understand it

We aim to acknowledge reports within a reasonable timeframe and will
work with you on a fix and disclosure timeline before any public
details are shared.

## Supported Versions

Given the repository's current stage (Phase 0, pre-1.0 specification),
only the latest state of `main` is supported. There are no maintained
release branches yet.

## Scope Going Forward

Once Phase 2 ships a hosted reference implementation, this document
will be updated to cover:

- API authentication and authorization
- Data handling for artifacts submitted to the registry
- Dependency and supply-chain practices for the SDK and CLI

Until then, if in doubt about whether something is a security concern
worth reporting privately versus a general bug worth a public issue,
default to reporting it privately at hello@talvik.ai — that costs
nothing and avoids any risk of a genuine issue being disclosed
publicly before it's understood.

---

*© 2026 Talvik, Inc.*
