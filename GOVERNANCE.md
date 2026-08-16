# Governance

This document defines who stewards the MAK4I protocol, how changes are
proposed and reviewed, and how versioning works. It's the canonical
answer to "who guides this project and how does it change" — other
documents reference this one rather than repeating it.

---

## Stewardship

**Talvik, Inc.** is the steward of the MAK4I protocol.

- The protocol specification (SPEC.md and the MAK-XXXX standards) is
  MIT licensed and open forever — stewardship is not the same as
  exclusive control. See [MCP.md](MCP.md#why-keeping-the-protocol-open-is-rational)
  for why this distinction matters and why keeping the protocol open
  is the rational choice, not a concession.
- Talvik, Inc. operates the commercial layer built on top of the
  protocol (the hosted Registry, Enterprise offerings) — see
  [BUSINESS_MODEL.md](BUSINESS_MODEL.md).
- Guiding the protocol's direction does not require using Talvik's
  commercial products. Anyone can implement the spec independently.

As the project grows, Talvik intends to establish a community steering
committee (referenced in [CONTRIBUTING.md](CONTRIBUTING.md#stewardship)).
That does not exist yet as of Phase 0 — until it does, Talvik's
maintainers steward proposed standards through the process below.

### Stewardship Principles

Talvik commits to:

- Keeping the protocol open — MIT licensed, forever
- Making decisions transparently, in the open, via GitHub
- Publishing rationale for significant specification changes, not just
  the outcome
- Considering community feedback before finalizing a decision
- Maintaining backward compatibility whenever practical

These principles are what "steward" means in practice — guiding the
project's direction openly, not controlling it as a closed asset.

---

## How Changes Are Proposed

Two categories of change, with different processes:

### Protocol standards (MAK-XXXX)

A new or modified standard — a schema change, a new specification like
context injection or access control — follows the process in
[CONTRIBUTING.md](CONTRIBUTING.md#1-propose-a-new-mak-standard-mak-xxxx):

1. Open a GitHub Issue titled `[MAK-PROPOSAL] ...` (template provided)
2. A Talvik maintainer reviews and assigns a MAK number
3. **2-week community comment period** (Draft → Review)
4. **A Talvik maintainer reviews within 1 week** after the comment
   period closes, and either accepts, requests changes, or declines
   with a stated reason (Review → Accepted)
5. Reference implementation follows acceptance

Numbers are assigned sequentially as proposals are accepted, not
reserved by topic — see [CONTRIBUTING.md](CONTRIBUTING.md#naming-convention)
and [SPEC.md](SPEC.md#standards) for the current list.

### Everything else (docs, artifacts, code, bug fixes)

Standard pull request process — see
[CONTRIBUTING.md](CONTRIBUTING.md#pull-request-guidelines) for the
checklist and commit format. No special approval process beyond normal
PR review.

---

## Who Reviews What

| Change type | Who reviews |
|---|---|
| New MAK-XXXX standard | Talvik maintainers, after the community comment period |
| Breaking change to an existing standard | Talvik maintainers — must remain backward compatible per the stewardship principles above, or be proposed as a new major version |
| New artifact added to the registry | Whoever proposes it, via normal PR review — no special approval beyond following [MAK-0001](standards/MAK-0001.md) schema |
| Documentation fixes, typos, clarity improvements | Normal PR review |
| Conformance suite / MAK4I Certified criteria | Talvik maintainers — see [CONFORMANCE.md](CONFORMANCE.md) |

**Release manager:** Official releases of the MAK4I specification are
published by Talvik maintainers.

---

## Versioning

```
Specification versions

MAK4I v0.x  →  Draft. Breaking changes expected between minor versions.
      ↓
MAK4I v1.x  →  First stable release, end of Phase 1 (see ROADMAP.md).
      ↓          Backward-compatibility guarantee begins here.
MAK4I v2.x  →  Future major version, only for changes that can't be
                made backward-compatible.
```

The protocol follows [Semantic Versioning (SemVer)](https://semver.org/):
`MAJOR.MINOR.PATCH`. A MAJOR version bump signals a breaking change; MINOR
adds functionality in a backward-compatible way; PATCH is a
backward-compatible fix or clarification.

- **Individual artifacts** use the same SemVer scheme per
  [MAK-0001](standards/MAK-0001.md) — the schema defines this at the
  artifact level, independent of the protocol specification's own
  version.
- **The protocol specification** (SPEC.md) versions independently —
  currently v0.1 (Draft). v1.0 is targeted for the end of Phase 1 and
  is expected to be the first version carrying a backward-compatibility
  guarantee going forward.
- **Breaking changes** to the core schema or an accepted standard
  require a new MAK-XXXX proposal, not a silent edit to an existing
  one — this keeps prior implementations valid rather than breaking
  them retroactively.

---

## What This Document Is Not

This is not a legal document and does not replace Talvik, Inc.'s
corporate governance (board, bylaws, etc.) — it describes how the
*open protocol* is stewarded, which is intentionally decoupled from how
the company itself is run.

---

*© 2026 Talvik, Inc.*
