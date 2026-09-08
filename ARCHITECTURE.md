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

## What the Reference Implementation Ships Today

The diagram above is the target architecture — the destination, not the
starting point. Being direct about the gap between the two is part of how
this protocol earns trust. Here is what the working reference
implementation (MVP) covers today:

```
              MCP-connected AI clients   │   Operator CLI
                              │
              MCP server (stdio + Streamable HTTP)
                              │
                        MAK4I engine
            ┌─────────────────────────────────────┐
            │  Create / retrieve / search      ✓   │
            │  Supersede (lineage preserved)   ✓   │
            │  Version history                 ✓   │
            │  Provenance + audit log          ✓   │
            │  Conflict detection (surfaced)   ✓   │
            │  Integrity checks (fail-closed)  ✓   │
            │  Check-before-create discipline  ✓   │
            │  ─────────────────────────────────   │
            │  Identity / auth beyond bearer   —   │
            │  Sync / revocation / write policy —  │
            └─────────────────────────────────────┘
                              │
                     Storage adapters
            ┌─────────────────────────────────────┐
            │  Local JSON store                ✓   │
            │  Object storage (GCS) adapter    ✓   │
            │  OKF / SQL / vector adapters     —   │
            └─────────────────────────────────────┘
```

Items marked `—` are specified or planned, not built; each has a target
phase in [ROADMAP.md](ROADMAP.md). The object-storage adapter is one
storage backend behind the same interface, not a requirement — the engine
contains no storage-, database- or provider-specific workflow logic. The
reference implementation is deployed for testing but is a proof of
protocol behavior, not a production service; its source will be published
when it is release-ready.

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

