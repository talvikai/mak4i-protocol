# MAK4I Standards

*Published MAK standards and the conventions that govern protocol
evolution.*

The MAK4I protocol is defined through a series of MAK standards.
Each standard describes one normative aspect of the protocol. This
file is the index — see [SPEC.md](SPEC.md) for the protocol
specification itself and [GOVERNANCE.md](GOVERNANCE.md) for how a
standard is proposed and approved.

## Published and Planned Standards

| Standard | Title | Status | File |
|----------|-------|--------|------|
| MAK-0001 | Artifact Metadata Schema | Draft | [standards/MAK-0001.md](standards/MAK-0001.md) |
| MAK-0002 | Context Injection Specification | Draft (In Progress) | [standards/MAK-0002.md](standards/MAK-0002.md) |
| MAK-0003 | Memory Resolution Algorithm | Draft (In Progress) | [standards/MAK-0003.md](standards/MAK-0003.md) |
| MAK-0004 | Conflict Resolution Specification | Draft | [standards/MAK-0004.md](standards/MAK-0004.md) |
| MAK-0005 | Versioning and Compatibility Specification | Draft | [standards/MAK-0005.md](standards/MAK-0005.md) |
| MAK-0006 | Identity and Access Control | Draft | [standards/MAK-0006.md](standards/MAK-0006.md) |
| MAK-0007 | Registry API Contract | Draft (In Progress) | [standards/MAK-0007.md](standards/MAK-0007.md) |
| MAK-0008 | MCP Binding and Authorization | Draft | [standards/MAK-0008.md](standards/MAK-0008.md) |
| MAK-0009 | Knowledge Scopes, Resources and Rule Inheritance | Draft | [standards/MAK-0009.md](standards/MAK-0009.md) |

MAK-0004 and MAK-0005 each contain a normative **Part A** (governed
project records and subject conflicts) and a **Part B** template whose
design decisions remain open. "Draft" means published for the community
comment period; no standard here is yet Accepted.

MAK-0009 is **architecture-defined** (see [SPEC.md](SPEC.md#specification-status-markers)):
it fixes the model for organization knowledge, resources and rule
inheritance, but has no acceptance criteria or interface binding yet, and
no implementation may claim support for it.

**Draft (In Progress)** (MAK-0002, MAK-0003, MAK-0007) means: published
so the design can be reviewed in the open, but **not complete, not
accepted and not implemented**. Each such document separates:
- a short *Settled design* (agreed, citing the standards it comes from);
- *Open items*;
- non-normative *design notes*.

No conformance requirement depends on these documents, and publishing a
file doesn't make its specification complete. What they need to leave
"In Progress" is in [ROADMAP.md](ROADMAP.md#criteria-for-mak-0002-mak-0003-and-mak-0007).

Canonical JSON Schemas for these standards are in [`schemas/`](schemas/);
validate the repository with `python scripts/validate_protocol.py`.

MAK numbers are assigned sequentially, in proposal order. MAK-0002,
MAK-0003 and MAK-0007 were reserved by topic before that rule — see
[CONTRIBUTING.md](CONTRIBUTING.md#naming-convention).

## Design Principles

Every MAK standard is:

- **Versioned** — semantic versioning at the artifact level (MAK-0001)
- **Backward compatible** — breaking changes require a new standard,
  not a silent edit to an existing one
- **Community reviewed** — a 2-week comment period before acceptance
- **Approved through the governance process** — see
  [GOVERNANCE.md](GOVERNANCE.md#stewardship-principles) for the full
  stewardship principles and approval process

## Related Documents

- [SPEC.md](SPEC.md) — the protocol specification
- [GOVERNANCE.md](GOVERNANCE.md) — proposal and approval process
- [CONFORMANCE.md](CONFORMANCE.md) — conformance profiles and acceptance criteria

---

*© 2026 Talvik, Inc.*
