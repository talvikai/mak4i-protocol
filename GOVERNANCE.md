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
  exclusive control. See [MCP.md](docs/background/OPEN_PROTOCOL_STRATEGY.md#why-keeping-the-protocol-open-is-rational)
  for why this distinction matters and why keeping the protocol open
  is the rational choice, not a concession.
- Talvik, Inc. operates the commercial layer built on top of the
  protocol (the hosted Registry, Enterprise offerings) — see
  [BUSINESS_MODEL.md](docs/background/BUSINESS_MODEL.md).
- Guiding the protocol's direction does not require using Talvik's
  commercial products. Anyone can implement the spec independently.

As the project grows, Talvik intends to establish a community steering
committee (referenced in [CONTRIBUTING.md](CONTRIBUTING.md#stewardship)).
That does not exist yet — until it does, Talvik's maintainers steward
proposed standards through the process below.

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

1. Open a GitHub Issue titled `[MAK-PROPOSAL] ...` (template provided),
   or a pull request that includes the draft.
2. A Talvik maintainer reviews it and assigns the next sequential MAK
   number.
3. The standard is published as **Draft**.
4. **2-week community comment period** (Draft → Review). It is announced
   in the CHANGELOG with its start and end dates.
5. **A Talvik maintainer decides within 1 week** after the comment period
   closes: accept, request changes, or decline with a stated reason
   (Review → Accepted).

**Status ladder:** Reserved → Draft → Review → Accepted → Deprecated.
- *Reserved* applies only to MAK-0002, MAK-0003 and MAK-0007, which were
  reserved by topic before this rule.
- Every new number is assigned sequentially, in proposal order.

**Implementing Drafts.** Implementations, including the Reference, MAY
implement Draft standards experimentally, provided they:
- pin the exact protocol revision they implement;
- report it (for MCP servers, `mak4i_whoami.protocol`).

Findings from implementation return to the protocol as dated revision
entries (protocol first, then implementation). Acceptance happens only
through the comment period above.

**Comment periods for the current Drafts.** MAK-0004 Part A, MAK-0005
Part A, MAK-0006, MAK-0008 and MAK-0009 were merged and revised without a
comment period. Their 2-week comment period starts when the protocol
release that contains this governance text is published. The CHANGELOG
records the dates.

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
| Conformance profiles and criteria | Talvik maintainers — see [CONFORMANCE.md](CONFORMANCE.md) |

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

There is **one protocol release number**:
- **Releases.** The repository is tagged `vMAJOR.MINOR.PATCH`, and
  SPEC.md's version matches it.
- **Schemas.** Every schema's `x-mak4i-schema-version` equals the release
  number (the validator checks this).
- **Standards** keep their own draft revision number (`0.1`, `0.2`) with
  a dated row in their revision history for every change, plus an
  accurate *Last Updated* date.
- **Unreleased changes** are listed under "Unreleased" in the CHANGELOG
  until a maintainer tags the release.
- **Not protocol versions.** Distributable-artifact package versions
  ([MAK-0009 §2.3](standards/MAK-0009.md#2-knowledge-profiles)) and project-record revisions are not protocol
  versions.
- **Breaking changes.** During v0.x, Draft standards may change
  incompatibly. Every such change must be listed in the CHANGELOG under
  "Breaking" with its migration note. From v1.0, breaking changes to an
  Accepted standard need a new MAJOR protocol version or a new MAK
  standard. A silent edit is never allowed.

---

## What This Document Is Not

This is not a legal document and does not replace Talvik, Inc.'s
corporate governance (board, bylaws, etc.) — it describes how the
*open protocol* is stewarded, which is intentionally decoupled from how
the company itself is run.

---

*© 2026 Talvik, Inc.*
