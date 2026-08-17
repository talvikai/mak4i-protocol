# Architecture

*The detailed runtime, registry, storage adapter, and implementation
architecture for MAK4I. [VISION.md](VISION.md) links here for the
high-level summary; this document is the full version.*

---

## Where MAK4I Sits

MAK4I is not another memory format competing with [OKF](https://github.com/google/okf)
or another memory store competing with [Mem0](https://mem0.ai). It's the runtime layer
that sits *above* formats and stores, deciding who gets to read, write, and trust memory —
regardless of which format or store it lives in.

```
                          Applications
   Cursor | Claude Code | Bedrock | ChatGPT | Gemini | Internal agents
                              │
                        MCP / SDK / API
                              │
                     MAK4I Memory Runtime
            ┌─────────────────┼─────────────────┐
            │  Identity       │  Authorization   │
            │  Retrieval      │  Write policy    │
            │  Provenance     │  Lifecycle       │
            │  Sync           │  Audit           │
            │  Conflicts      │  Revocation      │
            └─────────────────┼─────────────────┘
                              │
                  Format and storage adapters
            ┌─────────────────┼─────────────────┐
            │  OKF bundles    │  SQL / vector DB │
            │  Git repos      │  AgentCore       │
            │  Knowledge APIs │  Enterprise KBs  │
            └─────────────────────────────────────┘
```

**In one line:** MAK4I consumes and governs artifact metadata while
defining protocol behavior above the format layer. OKF is a format.
Mem0 is a store. MAK4I is the runtime that governs memory access, trust,
and reuse across all of them.

This placement matters for one specific reason: it's the honest answer to
*"why not just use OKF"* or *"how is this different from Mem0."* MAK4I doesn't
ask a team to abandon their format or store — it's format-agnostic by
design. An artifact described in OKF's frontmatter, or held in Mem0's
store, is a legitimate input MAK4I can read; MAK4I doesn't require
reinventing provenance or trust metadata that a format already defines.
What MAK4I adds is what sits above all of them: the enforced
check-before-create discipline and audit trail that no format or store
provides on its own, regardless of how well that format or store
describes the artifact once it exists. See
[COMPETITIVE_LANDSCAPE.md](COMPETITIVE_LANDSCAPE.md) for the full comparison.

---

## What v0.1 Actually Ships (August 2026)

The diagram above is the target architecture — the destination, not the
starting point. Being direct about the gap between the two is part of how
this protocol earns trust. Here is the thin vertical slice that exists today:

```
                          Applications
                   Claude Code | Claude.ai (via CLI)
                              │
                         CLI / local API
                              │
                     MAK4I Runtime (v0.1)
            ┌─────────────────────────────────────┐
            │  Retrieval        ✓ implemented      │
            │  Provenance       ✓ implemented      │
            │  Check-before-create discipline  ✓   │
            │  Savings log (audit-lite)        ✓   │
            │  ─────────────────────────────────   │
            │  Identity          spec'd, not built │
            │  Authorization     spec'd, not built │
            │  Sync / Conflicts  roadmap (Phase 3+) │
            │  Write policy      roadmap (Phase 4)  │
            │  Revocation        roadmap (Phase 4+) │
            └─────────────────────────────────────┘
                              │
                  Format and storage adapters
            ┌─────────────────────────────────────┐
            │  Local JSON artifacts    ✓ v0.1      │
            │  Git repo (this repo)    ✓ v0.1      │
            │  OKF bundle adapter      roadmap      │
            │  SQL / vector DB adapter roadmap      │
            └─────────────────────────────────────┘
```

Every box marked `roadmap` has a target phase in [ROADMAP.md](ROADMAP.md).
Nothing on this page claims to be built unless it is built — if you clone
this repo today, the `✓ implemented` boxes are what you get.

---

## The Registry Model

Skills, Knowledge, and History become reusable dependencies —
just like npm packages.

```bash
# Install what you need
mak4i install company/backend-standards
mak4i install company/deployment-skills
mak4i install schedovia/context

# Inject before any AI session
mak4i inject

# Every session starts with full context
# Your Skills loaded. Your Knowledge loaded. Your History loaded.
# Continue instantly. Never start from zero.
```

### Community marketplace

Just as npm has millions of packages, the MAK4I registry will have
Skills, Knowledge packs, and History templates contributed by the community.

| Category | Example packs |
|----------|--------------|
| Skills — Frontend | React patterns, Next.js deployment, CSS frameworks |
| Skills — Backend | FastAPI scaffold, Node.js Express, Django setup |
| Skills — Infrastructure | Terraform AWS, GCP Cloud Run, Kubernetes |
| Skills — AI | Prompt engineering, RAG patterns, Claude Code workflows |
| Knowledge — Compliance | HIPAA checklist, SOC2 controls, GDPR requirements |
| Skills — API Gateways | Apigee X, IBM DataPower, Kong, Azure APIM |

---

