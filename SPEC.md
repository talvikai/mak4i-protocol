# MAK4I Protocol Specification

**Version:** 0.3 (Draft). Changes since the last tag are listed in [CHANGELOG.md](CHANGELOG.md); a release is tagged by a maintainer ([GOVERNANCE.md](GOVERNANCE.md#versioning))  
**Status:** Work in Progress  
**Last updated:** 2026-10-16  
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
[COMPETITIVE_LANDSCAPE.md](docs/background/COMPETITIVE_LANDSCAPE.md) for why this
distinction matters relative to memory-focused alternatives.

### Core Principle

> Don't rebuild what already exists. Check the registry, reuse or
> adapt what's there, and only generate something new when nothing
> matches.

This is a **reuse discipline** that MAK4I supports with protocol
structure and client guidance. It is not an enforcement guarantee: the
protocol defines how to look up current knowledge before writing
([MAK-0008 §13.9](standards/MAK-0008.md#13-client-requirements)), and conflicts make competing writes
visible ([MAK-0004](standards/MAK-0004.md)), but no standard forces a client to check first.
MAK4I defines how AI knowledge is:
- **Structured**: project records ([MAK-0005](standards/MAK-0005.md)) and
  distributable artifacts ([MAK-0001](standards/MAK-0001.md), [MAK-0009](standards/MAK-0009.md));
- **Discovered**: deterministic lookup of current knowledge
  ([MAK-0008](standards/MAK-0008.md)), which clients should consult before creating;
- **Versioned**: record revisions and package versions;
- **Governed**: identity, permissions, provenance, conflicts and rules;
- **Injected** *(in progress, [MAK-0002](standards/MAK-0002.md))*: assembled into an AI session
  before work begins;
- **Shared**: within an organization today (architecture-defined); via
  public registries in the future ([MAK-0007](standards/MAK-0007.md), in progress).

---

## Terminology

| Term | Definition |
|------|-----------|
| **Artifact** | A unit of knowledge. MAK4I has two knowledge profiles, Project Records and Distributable Artifacts ([MAK-0009 §2](standards/MAK-0009.md#2-knowledge-profiles)) |
| **Project Record** | Knowledge kept within one project; not shared with other projects ([MAK-0005 Part A](standards/MAK-0005.md#part-a--governed-project-records-normative)) |
| **Distributable Artifact** | Organization-scoped knowledge shared with that organization's projects ([MAK-0009 §2.2](standards/MAK-0009.md#2-knowledge-profiles)) — *architecture-defined* |
| **Revision / package version** | A project record's lineage position (`version`: `"1.0"`, `"2.0"`) vs a distributable artifact's semantic version (`package_version`); never compared ([MAK-0009 §2.3](standards/MAK-0009.md#2-knowledge-profiles)) |
| **Resource / resource group** | A logical collection inside one project, optionally in one non-nested group ([MAK-0009 §3](standards/MAK-0009.md#3-resources-and-resource-groups)) — *architecture-defined* |
| **Rule / enforcement** | Knowledge carrying a `rule` object with `enforcement: default \| mandatory`, inherited downward with explicit overrides ([MAK-0009 §4](standards/MAK-0009.md#4-rules-enforcement-and-inheritance)) — *architecture-defined* |
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

## Knowledge Model

```
Organization ─┬─ Distributable Artifacts (organization-scoped, shared with its projects)
              └─ Project ─┬─ Project Records (project-wide)
                          ├─ Resource ── Project Records
                          └─ Resource Group ── Resource ── Project Records
```

- **Project Records** stay in their project. **Distributable Artifacts**
  are shared only within their organization; a public registry is not
  implied ([MAK-0009](standards/MAK-0009.md)).
- **Rules** at organization, project, resource-group or resource scope are
  inherited downward. `default` rules may be explicitly overridden at a
  lower scope; `mandatory` rules may not. Effective context explains which
  rule applies and where it came from. MAK4I governs effective context; it
  does not guarantee that an external AI follows it.
- **Authorization** is by project grant today. Resource-group and
  resource grants are future and additive; there is no explicit deny.

### Specification status markers

| Marker | Meaning |
|---|---|
| **Implemented contract** | Normative and covered by acceptance criteria in [CONFORMANCE.md](CONFORMANCE.md). Implementations are assessed against it today. |
| **Architecture-defined** | Normative design that fixes the model for future implementations. It has no acceptance criteria and no interface binding yet. Schemas, and individual schema properties, carry `"x-mak4i-status": "architecture"`; standards say `Conformance status: Architecture`. Implementations MUST NOT claim support for it, and `scripts/validate_protocol.py` keeps it out of the MCP tool contract. |

At this revision, MAK-0009 (distributable artifacts, resources, resource
groups, rules and inheritance) is architecture-defined. MAK-0002, MAK-0003
and MAK-0007 are Drafts (In Progress), with no acceptance criteria and
no binding. Everything in
MAK-0004 Part A, MAK-0005 Part A, MAK-0006 and MAK-0008 that CONFORMANCE.md
lists is the implemented contract.

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

Project records are defined by [MAK-0005 Part A](standards/MAK-0005.md#part-a--governed-project-records-normative).
Packaging metadata for distributable artifacts is defined in [MAK-0001](standards/MAK-0001.md)
(its field mapping onto the Distributable Artifact profile is in [MAK-0009 §2.2](standards/MAK-0009.md#2-knowledge-profiles)).

### Minimum required fields (MAK-0001 packaging metadata)

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

## Injection Flow (planned, illustrative)

*Illustrative only. Context assembly (MAK-0002) and memory resolution
([MAK-0003](standards/MAK-0003.md)) are Drafts (In Progress), not complete ([MAK-0002](standards/MAK-0002.md));
there is no `mak4i inject` command today. Until they are specified,
[MAK-0008 §10.6](standards/MAK-0008.md#10-tool-catalog) is the only injection rule.*

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

Project records are versioned by **revision**, their position in a lineage
(`"1.0"`, `"2.0"`, …, [MAK-0005 §A2](standards/MAK-0005.md#a2-record-fields)).
Distributable artifacts use a semantic **package version**
(MAJOR.MINOR.PATCH). The two are never compared or converted
([MAK-0009 §2.3](standards/MAK-0009.md#2-knowledge-profiles)). The bump guidance below applies
to package versions only, and is illustrative until
[MAK-0005 D-001](standards/MAK-0005.md#decision-d-001--version-representation-and-semantics) is decided.

| Change | Version bump |
|--------|-------------|
| Breaking schema change | MAJOR |
| New optional fields | MINOR |
| Documentation, metadata | PATCH |

Projects can pin an organization artifact to a package version
([MAK-0009 §2.2](standards/MAK-0009.md#2-knowledge-profiles)); a mandatory rule always applies at its latest
version.

---

## Access Control

**Project access (normative, draft):** identities, `agent_id`,
permissions, grants, revocation, provenance and administration are
defined in [MAK-0006](standards/MAK-0006.md). Transport scopes never
widen a project grant. A project grant governs every resource and
resource group in the project. Resource-group and resource grants are
future work; they will be additive (never narrowing project access), and
there is no explicit deny. Resource metadata is not an access
restriction ([MAK-0009 §7](standards/MAK-0009.md#7-authorization-current-and-future)).

**Registry visibility (planned, illustrative):** the levels below
describe intended visibility of *published* artifacts in a future
registry (MAK-0007). Teams and individual-only visibility are not part of
[MAK-0006](standards/MAK-0006.md) (no teams, project grants only), and will be defined with the
registry, consistently with MAK-0006.

| Level | Who can access |
|-------|---------------|
| Public | Anyone |
| Organization | All members of an org |
| Team | Specific team members |
| Private | Individual only |

Encryption of sensitive artifact content is approved future scope
([ROADMAP.md](ROADMAP.md#approved-future-protocol-scope)); no standard defines it today.

---

## CLI Interface (planned, illustrative)

*Illustrative only. These registry commands depend on MAK-0002 and
[MAK-0007](standards/MAK-0007.md), which are Drafts (In Progress). Implementations document their own CLIs and
map them to the MAK-0008 tools ([MAK-0008 §10.3](standards/MAK-0008.md#10-tool-catalog)).*

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
invalid examples in [`schemas/examples/`](schemas/examples/). Validate the
repository with:

```bash
pip install -r scripts/requirements.txt
python scripts/validate_protocol.py
```

Schema keywords specific to MAK4I:
- `x-mak4i-schema-version`: the schema's version (equal to the protocol
  release).
- `x-mak4i-status`: `architecture` marks architecture-defined schemas and
  properties.
- `x-mak4i-tools`: the tool list in `mcp-tools.schema.json`.

---

## Extensibility

- **Inputs are closed.** Servers reject arguments that a tool's input
  schema doesn't define (`validation_error`,
  [MAK-0008 §10.2](standards/MAK-0008.md#10-tool-catalog)).
- **Clients ignore unknown output fields** and handle unknown error codes
  by their `retryable` flag ([MAK-0008 §9.5](standards/MAK-0008.md#9-error-model)).
- **New protocol fields** are added only as OPTIONAL fields in a MINOR
  protocol release.
- **Vendor fields.** Implementation-specific fields in outputs use the
  prefix `x_<vendor>_` (for example `x_acme_trace`). Output schemas
  accept them through `patternProperties`.
- **Vendor tools.** Implementation-specific tools MUST NOT use the
  `mak4i_` prefix ([MAK-0008 §10.4](standards/MAK-0008.md#10-tool-catalog)).
- **Naming asymmetries kept for compatibility.** Tool inputs and records
  say `project`, while grants and `mak4i_list_projects` say `project_id`.
  A supersession's `reason` input is stored as the record's `rationale`.

---

## Skills (planned, deferred)

Skills as a first-class MAK4I object (packaged, invocable procedures
with their own lifecycle) are **approved future scope**
([ROADMAP.md](ROADMAP.md#approved-future-protocol-scope)). No MAK standard defines them yet and no
reference implementation supports them. Where "Skills" appears
elsewhere in this repository, it is an analogy for procedural knowledge,
not this future object.

---

## Standards

| Standard | Title | Status |
|----------|-------|--------|
| MAK-0001 | Artifact Metadata Schema | Draft |
| MAK-0002 | Context Injection Specification | Draft (In Progress) |
| MAK-0003 | Memory Resolution Algorithm | Draft (In Progress) |
| MAK-0004 | Conflict Resolution Specification | Draft |
| MAK-0005 | Versioning and Compatibility Specification | Draft |
| MAK-0006 | Identity and Access Control | Draft |
| MAK-0007 | Registry API Contract | Draft (In Progress) |
| MAK-0008 | MCP Binding and Authorization | Draft |
| MAK-0009 | Knowledge Scopes, Resources and Rule Inheritance | Draft |

---

## Conformance

Conformance is claimed per **profile and protocol version**, for example
"conformant to *Server: Project Records* and *Transport: HTTP + OAuth*
at protocol 0.2". The profiles and their acceptance criteria are in
[CONFORMANCE.md](CONFORMANCE.md#conformance-profiles). There is no "MAK4I Certified" badge until a
published conformance suite and certification process exist (approved
future scope).

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
