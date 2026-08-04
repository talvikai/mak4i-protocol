# Competitive Landscape

*Last researched: August 2, 2026. This document is reviewed before every major release.*

**See also:** [VISION.md — Architecture](VISION.md#architecture--where-mak4i-sits) for how MAK4I positions itself as a runtime layer *above* the formats and stores named below, rather than a competing format or store.

Before going public, we did the research most protocols skip: who else is solving this problem, and does MAK4I still say something true and specific once you account for them?

The honest answer: the "portable AI memory" space got crowded fast in mid-2026. Several projects now overlap with parts of what MAK4I originally claimed. This document names them directly, says where they beat us, and defines the narrower claim MAK4I actually defends.

---

## The Landscape as of August 2026

### Direct protocol competitors

**Open Knowledge Format (OKF)** — Google Cloud, published June 12, 2026
A vendor-neutral, Apache 2.0 spec for representing team/system knowledge as a directory of markdown files with YAML frontmatter (`type`, `index.md`, `log.md`, cross-linked concept files forming a graph). No SDK, no runtime, no registry required — "format, not platform." Ships a Claude Code plugin, a BigQuery enrichment agent, and a static HTML visualizer. This is the closest match to MAK4I's original pitch: an open, portable, file-based knowledge layer that any agent can read.

**Open Memory Protocol (OMP)** — community, GitHub
A vendor-neutral spec for AI tools to store, retrieve, and share memory about users and context. Ships its own MCP server plus adapters for Claude Code, Cursor, and GitHub Copilot. Uses `semantic` as a memory type — the same term MAK4I uses. Apache 2.0.

### Funded commercial memory layers

**Mem0** — 41,000+ GitHub stars, $24M Series A, exclusive AWS Agent SDK integration, SOC 2 + HIPAA compliant, 100,000+ developers. The dominant "memory API" for agent builders: add/search/update/delete memory operations with user/session/agent scopes.

**Supermemory** — MIT-licensed core (26.8K stars) with a commercial hosted layer for connectors, team sharing, and compliance. This is the same open-core-plus-hosted-platform model MAK4I uses.

**Zep** — Temporal knowledge graph (open-sourced as Graphiti), strongest at "who changed what when." $500K seed — underfunded relative to Mem0 but architecturally distinct.

**Letta (formerly MemGPT)** — OS-inspired paged memory, academic roots, strong in research and agent-framework contexts.

### Native platform memory (the baseline, not a competitor)

By mid-2026 every major AI platform shipped persistent memory: ChatGPT (rebuilt June 2026), Claude (extended to all tiers), Gemini (Personal Intelligence), Copilot (GA in M365). None of it travels between platforms — each is a walled garden. This is the problem every protocol above is trying to solve, and the reason the category exists at all.

---

## What MAK4I No Longer Gets to Claim Alone

Being direct about this matters more than sounding original:

- "Open protocol for portable AI memory" — OKF and OMP already say this, and OKF shipped first with Google's distribution behind it.
- "Works across Claude, Cursor, ChatGPT" — table stakes; every project above claims the same.
- "Three memory types" (procedural/semantic/episodic) — OMP already uses `semantic` as a type name; the taxonomy itself isn't a moat.
- "MCP server for memory" — OMP already ships one.
- "Vendor-neutral, no lock-in" — the entire category positions this way now.

If MAK4I launches saying only these things, the first credible comment on Hacker News will be "how is this different from OKF?" — and we need an answer that isn't defensive.

---

## What MAK4I Still Defends

**1. Reuse discipline as a first-class protocol behavior, not a side effect.**
Every competitor above is a *store*: you write memory in, you read memory out. None of them enforce a check-before-you-build step as part of the protocol itself. MAK4I's `check-before-create` skill — search the registry before generating anything, reuse or adapt what exists, only create new artifacts when nothing matches — is a discipline, not a database. This is the actual difference: MAK4I is optimizing for *not rebuilding what already exists*, not just for *remembering what happened*.

**2. Measured token savings as the unit of evidence, continuously logged.**
Competitors make efficiency claims in marketing copy (Mem0: "90% token reduction" on a benchmark). MAK4I's SAVINGS_LOG is a running, dated ledger of actual reuse events from real products in production — 38,400+ tokens tracked across specific sessions, specific artifacts, specific reuse vs. new-build classification. This is closer to an audit trail than a benchmark claim.

**3. Skills as a registry-distributed unit, not a config file.**
OKF stores knowledge as markdown files living in *your* repo. Mem0 stores memories as API-retrievable facts about a user or session. Neither treats a *reusable process* (a deployment runbook, a triage framework, a document-generation pattern) as a versioned, publishable, installable package the way `mak4i install company/deployment-standards` does. This is closer to npm's model than either competitor's.

**4. MAK4I Certified — a conformance mark, not just a spec.**
No competitor above has a certification program for implementations. If MAK4I becomes the reference for "an AI reuse-discipline protocol," the certification mark is a coordination point competitors don't have.

---

## The Honest Positioning Statement

**What MAK4I is not:** the first or only open memory format. OKF got there first with more distribution. Mem0 has more funding and more developers today.

**What MAK4I is:** the protocol that treats *not rebuilding what you already built* as the primary discipline — enforced through a check-before-create workflow, proven through a continuously logged savings record, and distributed through a registry of reusable Skills, not just stored facts.

If a team's problem is "the AI doesn't remember my preferences" → Mem0 or native platform memory solves that.
If a team's problem is "our knowledge should live in files, not a vendor's database" → OKF solves that.
If a team's problem is "we keep paying to regenerate things we already built, and we can't prove how much it's costing us" → that's the MAK4I problem, and nobody else is measuring it this way.

---

## What This Means for Launch

- Lead with the reuse-discipline framing in README.md and the launch post, not "portable AI memory" as a category claim.
- Add a "How MAK4I compares" section near the top of the repo — burying this invites exactly the comment thread we're trying to avoid.
- Cite OKF and Mem0 by name. Silence on obvious prior art reads as either not having done the research or hoping nobody asks — both worse than addressing it directly.
- The SAVINGS_LOG becomes the centerpiece of the pitch, not a supporting appendix. It is the one piece of evidence competitors cannot copy retroactively.

---

*This document will be revisited before each major MAK4I release. The competitive landscape in AI memory/context tooling is moving in months, not years — treat this page as perishable, not settled.*
