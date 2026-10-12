# MAK4I — Memory, Artifacts & Knowledge for Intelligence

> The protocol for not rebuilding what your AI already built.

**Built by [Talvik, Inc.](https://talvik.ai)**

**Status: Developer Preview.** This repository contains the protocol design,
draft specification and documentation. A public
[MAK4I reference implementation](https://github.com/talvikai/mak4i-reference) is available
separately. It supports the core protocol workflow end to end, including
create, retrieve, search, supersede, version history, provenance, operator
CLI access and MCP integration. The reference implementation provides Local
Developer and Enterprise Self-Hosted deployment options and continues to be
validated against the evolving specification. See [ROADMAP.md](ROADMAP.md)
for what exists today versus what's planned.

---

## What MAK4I Is

MAK4I is an open protocol for packaging, identifying, versioning, sharing,
injecting, and reusing AI artifacts across models, platforms, and
organizations.

> **New to MAK4I?** Start with [Understanding MAK4I](docs/UNDERSTANDING_MAK4I.md)
> for a plain-language explanation of MAK4I, what a MAK specification is,
> and how the core MAK standards work together.

A MAK4I artifact can represent:

- Project context
- Procedural knowledge (how to do something, consistently)
- Prompts
- Workflows
- Architecture and API contracts
- Historical decisions and rationale
- Reusable outputs (documents, code, templates)

**Memory is one artifact type — not the entire protocol.** Just as Git
standardized source control and npm standardized package distribution,
MAK4I standardizes how reusable AI artifacts move between tools instead of
being rebuilt from scratch in each one.

```
Claude Code, Cursor, ChatGPT, Gemini, Bedrock, Copilot, internal agents
                              │
                        MCP / SDK / API
                              │
                            MAK4I
                              │
              Registry · Artifacts · Knowledge · Context
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for the full
architecture, including what's actually implemented today versus planned.

---

## Protocol Philosophy

> MAK4I is the protocol. Talvik builds the platform.

```
MAK4I Protocol (open, MIT licensed)
    ↓
Talvik Registry (hosted)
Talvik Enterprise (commercial)
Talvik SDK (Python, Node.js, Go, Rust)
Talvik CLI (mak4i install, inject, publish)
```

**Open protocol forever. Commercial ecosystem on top.**

Following the open protocol + commercial ecosystem approach used by
projects such as Git, Kubernetes, and OpenTelemetry.

---

## How MAK4I Is Different

The AI memory space is crowded — [Mem0](https://mem0.ai), [Google's Open Knowledge Format](https://github.com/google/okf), [Open Memory Protocol](https://github.com/SMJAI/open-memory-protocol), and every major platform's native memory all solve some version of "the AI doesn't remember." MAK4I was designed after evaluating the existing landscape of AI memory, knowledge, and interoperability projects. See [COMPETITIVE_LANDSCAPE.md](docs/background/COMPETITIVE_LANDSCAPE.md) for the full comparison.

MAK4I isn't trying to out-remember them. It solves a narrower, different problem:

| If your problem is... | Look at |
|---|---|
| "The AI doesn't remember my preferences" | Mem0, native platform memory |
| "Our knowledge should live in files, not a vendor's database" | Google's OKF |
| "I want lifecycle and staleness tracked, but nothing stops duplicate work" | OKF v0.2, ByteRover |
| "We keep paying to regenerate things we already built, and the knowledge to avoid it is scattered across tools" | **MAK4I** |

MAK4I is built around a **reuse discipline**: look up existing knowledge before generating anything, reuse or adapt what exists, and only create new when nothing matches. The protocol supports that discipline — deterministic lookup of current knowledge, explicit conflicts when competing writes collide, authenticated provenance on every version, and client guidance and SDK tooling for checking first ([MAK-0008 §13.9](standards/MAK-0008.md#13-client-requirements)). It doesn't enforce the check today; a normative check-before-create rule is approved future scope ([ROADMAP.md](ROADMAP.md#approved-future-protocol-scope)). Every reuse decision is logged with a real token-savings estimate — not a benchmark claim, a running ledger designed to track actual reuse over time (currently reflecting development-time observations — see [Reference Implementation](#reference-implementation) below).

---

## The Problem

Every AI tool represents reusable knowledge differently — Claude has
Projects, Artifacts, and Skills; Cursor has Rules; ChatGPT has Memory;
GitHub Copilot has Instructions. None of those representations travel
between tools. Switch tools and you start from zero.

You re-explain your stack, regenerate code that already exists,
re-establish context that was already shared.

That's waste — computational, financial, and environmental.

At 1 million AI sessions per day each wasting 1,000 tokens —
that is **1 billion tokens per day** in avoidable generation.

As AI moves toward metered compute billing, that waste becomes
a direct dollar cost for every business running AI at scale.

**MAK4I fixes this.**

---

## Three Memory Types

| Type | Answers | Examples |
|------|---------|---------|
| **Procedural** | How? | Code frameworks, deployment pipelines, engineering playbooks |
| **Semantic** | What? | System architecture, schemas, API contracts, domain models |
| **Episodic** | Why? | Decisions made, rationale, sprint history, team conventions |

Together they provide complete project continuity across any AI tool.

---

## How It Works

The registry-backed `install` / `inject` workflow below is the intended
end-state and is **planned, illustrative** (see [ROADMAP.md](ROADMAP.md#approved-future-protocol-scope)). Today
the reference implementation provides MCP access for AI clients (the ten
[MAK-0008](standards/MAK-0008.md) tools, including conflict resolution) and an operator CLI
for records, conflicts and administration.

```bash
# Install memory packs
mak4i install company/backend-standards
mak4i install example-org/app-context

# Inject before any AI session
mak4i inject

# AI session starts with full context
# No re-explaining. No regenerating. Continue instantly.
```

---

## Quick Example

```json
{
  "id": "example-app-stack-context",
  "version": "1.0.1",
  "type": "semantic",
  "layer": "context",
  "name": "Example App Stack Context",
  "description": "Stack context for an example appointment-scheduling SaaS, so sessions don't re-explain the architecture",
  "token_estimate": 1500,
  "tags": ["stack", "context", "saas", "example"]
}
```

---

## Reference Implementation

A working reference implementation (MVP) exists and is in Developer
Preview. It implements the core protocol workflow — create, retrieve,
search, supersede, version history and provenance — with an operator CLI
and MCP access, and has been exercised end to end against several
independent AI clients it was tested with, through MCP. This is a proof of
protocol behavior, not a production platform. Its source is public at
[talvikai/mak4i-reference](https://github.com/talvikai/mak4i-reference), with Local Developer and
Enterprise Self-Hosted deployment options.

Talvik is beginning validation with developers and early design partners.

### Early reuse observations

MAK4I's core reuse mechanism — checking for and reusing existing artifacts
instead of regenerating them — was applied during MAK4I's own development.
The figures below are development-time observations, not production
traffic.

| Metric | Value |
|--------|-------|
| Tokens saved (dev-time observation) | 38,400+ |
| Sessions tracked | 29 |
| Sample artifacts in this repository | 13 ([ARTIFACT_INDEX.md](ARTIFACT_INDEX.md)) |

See [docs/background/MAK4I_SAVINGS_LOG.md](docs/background/MAK4I_SAVINGS_LOG.md) for the full,
dated session-by-session breakdown.

---

## Roadmap

MAK4I uses the **MAK-XXXX** convention for protocol standards. See
[ROADMAP.md](ROADMAP.md) for the full phase-by-phase roadmap and
[VISION.md](VISION.md#standards-process) for the standards list. MAK4I is
in **Developer Preview**: the specification is in active development and a
working reference implementation exists.

---

## Vision

*Write knowledge once. Inject anywhere. Continue instantly.*

*MAK4I is to AI sessions what npm is to Node.js.*

**Portable AI Memory. Open Forever.**

---

## Links

- Website: [talvik.ai](https://talvik.ai/)
- Documentation: [GitHub](https://github.com/talvikai/mak4i-protocol)
- Company: Talvik, Inc.
- License: MIT

---

*© 2026 Talvik, Inc. — MAK4I Protocol is open source, MIT licensed.*
