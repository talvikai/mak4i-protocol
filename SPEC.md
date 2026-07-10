# MAK4I Protocol Specification

**Version:** 0.1 (Draft)  
**Status:** Work in Progress  
**Author:** Talvik, Inc.  
**Created:** July 2026  
**License:** MIT  

> This specification is in active development.
> Community feedback welcome via [GitHub Issues](https://github.com/talvikai/mak4i-protocol/issues).

---

## Overview

MAK4I (Memory, Artifacts & Knowledge for Intelligence) is an open,
platform-independent protocol that enables portable AI intelligence
across models, platforms, and organizations.

### Core Principle

> Every AI session should start with context, not from zero.

MAK4I defines how AI knowledge is:
- **Structured** — using a standard artifact schema (MAK-0001)
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

---

## Memory Types

MAK4I defines three memory types. Every artifact must declare its type.

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

## Standards

| Standard | Title | Status |
|----------|-------|--------|
| MAK-0001 | Artifact Metadata Schema | Draft |
| MAK-0002 | Context Injection Specification | Planned |
| MAK-0003 | Memory Resolution Algorithm | Planned |
| MAK-0004 | Conflict Resolution Rules | Planned |
| MAK-0005 | Versioning and Compatibility | Planned |
| MAK-0006 | Access Control Model | Planned |
| MAK-0007 | Registry API Contract | Planned |

---

## Conformance

An implementation is MAK4I Certified when it:

1. Implements all REQUIRED fields from MAK-0001
2. Implements the injection flow defined in MAK-0002
3. Passes the MAK4I Conformance Test Suite

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
