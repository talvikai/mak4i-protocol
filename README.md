# MAK4I — Memory, Artifacts & Knowledge for Intelligence

> The protocol for not rebuilding what your AI already built.

**Built by [Talvik, Inc.](https://talvik.ai)**

**Status: Phase 0 — Foundation.** This repo currently contains the protocol
design, specification draft, and documentation. The reference API
implementation (backend, CLI, SDK) has not been built yet — that's Phase 2.
See [ROADMAP.md](ROADMAP.md) for what exists today versus what's planned.

---

## What MAK4I Is

MAK4I is an open protocol for packaging, identifying, versioning, sharing,
injecting, and reusing AI artifacts across models, platforms, and
organizations.

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

Following the same open protocol + commercial ecosystem model used by
projects such as Git/GitHub, Kubernetes, and Terraform.

---

## How MAK4I Is Different

The AI memory space is crowded — [Mem0](https://mem0.ai), [Google's Open Knowledge Format](https://github.com/google/okf), [Open Memory Protocol](https://github.com/SMJAI/open-memory-protocol), and every major platform's native memory all solve some version of "the AI doesn't remember." MAK4I was designed after evaluating the existing landscape of AI memory, knowledge, and interoperability projects. See [COMPETITIVE_LANDSCAPE.md](COMPETITIVE_LANDSCAPE.md) for the full comparison.

MAK4I isn't trying to out-remember them. It solves a narrower, different problem:

| If your problem is... | Look at |
|---|---|
| "The AI doesn't remember my preferences" | Mem0, native platform memory |
| "Our knowledge should live in files, not a vendor's database" | Google's OKF |
| "We keep paying to regenerate things we already built, and can't prove how much it costs" | **MAK4I** |

MAK4I is a **reuse discipline**, enforced as a protocol behavior: check the registry before generating anything, reuse or adapt what exists, and only create new when nothing matches. Every reuse decision is logged with a real token-savings estimate — not a benchmark claim, a running ledger designed to track actual reuse over time (currently reflecting development-time observations — see [Proof of Concept](#proof-of-concept) below).

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

```bash
# Install memory packs
mak4i install company/backend-standards
mak4i install schedovia/context

# Inject before any AI session
mak4i inject

# AI session starts with full context
# No re-explaining. No regenerating. Continue instantly.
```

---

## Quick Example

```json
{
  "id": "schedovia-stack-context",
  "version": "1.0.0",
  "type": "context",
  "layer": "episodic",
  "name": "Schedovia Stack Context",
  "description": "Full stack context for Schedovia — eliminates re-explaining architecture each session",
  "token_estimate": 1500,
  "tags": ["schedovia", "stack", "context"]
}
```

---

## Proof of Concept

MAK4I's core reuse mechanism — checking for and reusing existing artifacts
instead of regenerating them — was demonstrated during MAK4I's own
development process, before any API existed. Early figures below reflect
that development-time observation, not production traffic.

| Metric | Value |
|--------|-------|
| Tokens saved (dev-time observation) | 38,400+ |
| Sessions tracked | 29 |
| Artifacts registered | 9 across 6 types |

See [docs/MAK4I_SAVINGS_LOG.md](docs/MAK4I_SAVINGS_LOG.md) for the full,
dated session-by-session breakdown.

[WD Technology Solutions](https://western-digital.net) is Talvik's design
partner and the intended first production adopter, once the Phase 2 API is
live. See [ROADMAP.md](ROADMAP.md) for the integration plan.

---

## Roadmap

MAK4I uses the **MAK-XXXX** convention for protocol standards. See
[ROADMAP.md](ROADMAP.md) for the full phase-by-phase roadmap and
[VISION.md](VISION.md#standards-process) for the standards list —
this repo is currently **Phase 0 — Foundation** (Aug 2026).

---

## Vision

*Write knowledge once. Inject anywhere. Continue instantly.*

*MAK4I is to AI sessions what npm is to Node.js.*

**Portable AI Memory. Open Forever.**

---

## Links

- Website: [talvik.ai](https://talvik.ai)
- Developer docs: [talvik.dev](https://talvik.dev)
- Company: Talvik, Inc.
- License: MIT

---

*© 2026 Talvik, Inc. — MAK4I Protocol is open source, MIT licensed.*
