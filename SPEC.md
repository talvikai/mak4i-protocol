# MAK4I Protocol Specification

**Version:** 0.2 (Draft)  
**Status:** Work in Progress  
**Last updated:** 2026-10-10 — see [CHANGELOG.md](CHANGELOG.md)  
**Author:** Talvik, Inc.  
**Created:** August 2026  
**License:** MIT  

> This specification is in active development.
> Community feedback welcome via [GitHub Issues](https://github.com/talvikai/mak4i-protocol/issues).

---

## Overview

MAK4I (Memory, Artifacts & Knowledge for Intelligence) is an open,
platform-independent protocol for packaging, identifying, versioning,
sharing, and reusing AI artifacts — across models, platforms, and
organizations.

**Memory is one artifact type this protocol handles — not the whole
protocol.** MAK4I also covers procedural knowledge, project context,
prompts, workflows, and historical decisions. See
[README.md](README.md#what-mak4i-is) for the full picture and
[COMPETITIVE_LANDSCAPE.md](COMPETITIVE_LANDSCAPE.md) for why this
distinction matters relative to memory-focused alternatives.

### Core Principle

> Don't rebuild what already exists. Check the registry, reuse or
> adapt what's there, and only generate something new when nothing
> matches.

This is a **reuse discipline**, specified as protocol behavior rather
than left to individual client implementations. MAK4I defines how AI
artifacts are:
- **Structured** — using a standard artifact schema (MAK-0001)
- **Discovered** — searched before anything new is generated
- **Versioned** — using semantic versioning
- **Injected** — into any AI session before work begins
- **Shared** — via public and private registries

---

## Terminology

| Term | Definition |
|------|-----------|
| **Artifact** | A unit of knowledge conforming to the MAK4I schema |
| **Memory pack** | A collection of related artifacts |
| **Registry** | A store of published artifacts |
| **Injection** | The process of loading artifacts into an AI session |
| **MAK standard** | A formal specification in the MAK-XXXX series |
| **Organization / Project** | Tenancy boundary / unit of authorization ([MAK-0006](standards/MAK-0006.md)) |
| **Principal** | An authenticated identity: `human`, `service` or `agent` ([MAK-0006](standards/MAK-0006.md)) |
| **`agent_id`** | Stable, organization-scoped identifier of an agent principal ([MAK-0006 §3](standards/MAK-0006.md#3-agent-identity-agent_id)) |
| **Grant** | A principal's permissions (`read`, `write`, `resolve`) on one project ([MAK-0006 §5](standards/MAK-0006.md#5-permissions-and-grants)) |
| **Governed project record** | A versioned unit of project knowledge with lineage and provenance ([MAK-0005 Part A](standards/MAK-0005.md#part-a--governed-project-records-normative)) |
| **Subject key** | Explicit name of what a record is authoritative about ([MAK-0005 §A5](standards/MAK-0005.md#a5-subject-keys)) |
| **Conflict** | Two or more lineages claiming the same subject ([MAK-0004 Part A](standards/MAK-0004.md#part-a--subject-conflicts-normative)) |

---

## Artifact Types

MAK4I defines three artifact types. Every artifact must declare its type.
(These correspond to what README.md and VISION.md call Skills, Knowledge,
and History when explaining the same three types by analogy.)

### Procedural (How)
Knowledge describing how work is performed.
Rarely changes. Reusable across projects.

### Semantic (What)
Knowledge describing what is true about a project or organization.
Facts, structures, and definitions.

### Episodic (Why)
Knowledge describing what happened during a project.
Decisions, rationale, history, and context.

---

## Artifact Schema

Defined in [MAK-0001](standards/MAK-0001.md).

### Minimum required fields

```json
{
  "id": "string",
  "version": "semver",
  "type": "procedural | semantic | episodic",
  "name": "string",
  "description": "string",
  "content": "string | object"
}
```

### Full schema

See [MAK-0001](standards/MAK-0001.md) for the complete artifact metadata schema.

---

## Injection Flow

```
Developer
    ↓
mak4i inject
    ↓
MAK4I Client
    ↓
Memory Resolver (fetches artifacts, resolves dependencies)
    ↓
Procedural + Semantic + Episodic memory assembled
    ↓
Injected context
    ↓
AI Session (Claude / ChatGPT / Gemini / any model)
```

The key principle: **MAK4I operates before the prompt, not inside it.**

---

## Versioning

Every artifact uses semantic versioning (MAJOR.MINOR.PATCH).

| Change | Version bump |
|--------|-------------|
| Breaking schema change | MAJOR |
| New optional fields | MINOR |
| Documentation, metadata | PATCH |

Organizations can pin artifact versions exactly like software packages.

---

## Access Control

**Project access (normative, draft):** identities, `agent_id`,
permissions, grants, revocation, provenance and administration are
defined in [MAK-0006](standards/MAK-0006.md). Transport scopes never
widen a project grant.

**Registry visibility (planned):** the levels below describe intended
visibility of *published* artifacts in a future registry (MAK-0007).

| Level | Who can access |
|-------|---------------|
| Public | Anyone |
| Organization | All members of an org |
| Team | Specific team members |
| Private | Individual only |

Sensitive artifacts can be encrypted while remaining protocol-compatible.

---

## CLI Interface

```bash
# Install artifacts from registry
mak4i install company/backend-standards
mak4i install schedovia/context

# Inject into current AI session
mak4i inject

# Publish an artifact
mak4i publish ./my-artifact.json

# List installed artifacts
mak4i list

# Sync with remote registry
mak4i sync
```

---

## MCP Binding

MAK4I is reachable over the Model Context Protocol. Transports (stdio,
Streamable HTTP), authentication (bearer credentials and a
self-contained OAuth 2.1 authorization service pinned to the MCP
2025-11-25 authorization specification), the tool catalog
(`mak4i_whoami` … `mak4i_resolve_conflict`) and the error model are
defined in [MAK-0008](standards/MAK-0008.md).

---

## Schemas

Canonical, machine-readable JSON Schemas (draft 2020-12) for the
normative interfaces live in [`schemas/`](schemas/), with valid and
invalid examples in [`schemas/examples/`](schemas/examples/). Run
`python scripts/validate_protocol.py` (requires `jsonschema>=4.23`) to
validate schemas, examples, artifacts, links and the standards index.

---

## Skills (planned, deferred)

Skills as a first-class MAK4I object — packaged, invocable procedures
with their own lifecycle — are **planned and deferred**. No MAK standard
defines them yet and no reference implementation supports them. (The
word "Skills" elsewhere in this repository is an analogy for procedural
artifacts, not this future object.)

---

## Standards

| Standard | Title | Status |
|----------|-------|--------|
| MAK-0001 | Artifact Metadata Schema | Draft |
| MAK-0002 | Context Injection Specification | Planned |
| MAK-0003 | Memory Resolution Algorithm | Planned |
| MAK-0004 | Conflict Resolution Specification | Draft |
| MAK-0005 | Versioning and Compatibility Specification | Draft |
| MAK-0006 | Identity and Access Control | Draft |
| MAK-0007 | Registry API Contract | Planned |
| MAK-0008 | MCP Binding and Authorization | Draft |

---

## Conformance

An implementation is MAK4I Certified when it:

1. Implements all REQUIRED fields from MAK-0001
2. Implements the injection flow defined in MAK-0002
3. Passes the MAK4I Conformance Test Suite

Implementations of governed project records, identity and the MCP
binding are assessed against the acceptance criteria for MAK-0004 Part A,
MAK-0005 Part A, MAK-0006 and MAK-0008 in [CONFORMANCE.md](CONFORMANCE.md).

See [CONFORMANCE.md](CONFORMANCE.md) for details.

---

## Cross-Platform Compatibility

MAK4I is model-agnostic. Compatible with:
- Claude (Anthropic)
- ChatGPT (OpenAI)
- Gemini (Google)
- Open-source LLMs
- IDE assistants (Cursor, Copilot, Windsurf)
- AI agents
- MCP servers

---

## Contributing

This specification is developed in the open.

- Propose changes via Pull Request
- Discuss via GitHub Issues
- Propose new MAK standards via the MAK-XXXX process

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

*© 2026 Talvik, Inc. — MAK4I Protocol is MIT licensed.*
