# Competitive Landscape

*Last researched: August 2, 2026. This document is reviewed before every major release. It intentionally omits star counts, funding figures, and other metrics that change daily — the comparisons below focus on what each project architecturally does, which is stable regardless of when you're reading this.*

**See also:** [ARCHITECTURE.md](ARCHITECTURE.md) for how MAK4I positions itself as a runtime layer *above* the formats and stores named below, rather than a competing format or store.

Before going public, we did the research most protocols skip: who else is solving this problem, and does MAK4I still say something true and specific once you account for them?

The honest answer: the "portable AI memory" space got crowded fast in mid-2026. Several projects now overlap with parts of what MAK4I originally claimed. This document names them directly, says where they beat us, and defines the narrower claim MAK4I actually defends.

---

## The Landscape as of August 2026

### Direct protocol competitors

**Open Knowledge Format (OKF)** — Google Cloud, published June 12, 2026
A vendor-neutral, Apache 2.0 spec for representing team/system knowledge as a directory of markdown files with YAML frontmatter (`type`, `index.md`, `log.md`, cross-linked concept files forming a graph). No SDK, no runtime, no registry required — "format, not platform." Ships a Claude Code plugin, a BigQuery enrichment agent, and a static HTML visualizer. This is the closest match to MAK4I's original pitch: an open, portable, file-based knowledge layer that any agent can read.

**Open Memory Protocol (OMP)** — community, GitHub
A vendor-neutral spec for AI tools to store, retrieve, and share memory about users and context, with adapters distributed across several major coding tools. Architecturally, OMP is a store-and-retrieve spec: it standardizes the *shape* of memory records, not a discipline for deciding when to reuse versus regenerate. Uses `semantic` as a memory type — the same term MAK4I uses. Apache 2.0.

### Funded commercial memory layers

**Mem0** — the dominant venture-funded "memory API" for agent builders: add/search/update/delete operations scoped to a user, session, or agent. Architecturally a managed store behind an API, not a protocol — adopting Mem0 means depending on their hosted service and schema, the same lock-in shape as any vendor API, whatever memory operations or platform integrations happen to be current at any given time.

**Supermemory** — MIT-licensed core with a commercial hosted layer for connectors, team sharing, and compliance. This is the same open-core-plus-hosted-platform model MAK4I uses.

**Zep** — Temporal knowledge graph (open-sourced as Graphiti), strongest at "who changed what when." Architecturally distinct from the flat-store approach most competitors take.

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

**1. Reuse discipline as protocol-level behavior — the primary differentiator.**
Every competitor above is architected as a *store*: an artifact goes in, an artifact comes back out on request. None of them enforce a check-before-you-build step as part of the protocol itself — that logic, if it exists at all, lives in whatever application is calling their API. MAK4I specifies this as protocol behavior, not an optional client-side convention:

- **Discovery** — search the registry before generating anything new
- **Reuse** — return an exact match directly, no regeneration
- **Adaptation** — modify an existing artifact when a close-but-not-exact match exists
- **Provenance** — every artifact tracks what it was derived from
- **Lifecycle** — versioning and deprecation are first-class, not bolted on

This is architectural, not a feature list: MAK4I's unit of value is *not
rebuilding what already exists*, evaluated every time an artifact is
requested — not simply persisting and returning facts on demand. A
competitor could add a "check first" convention to their own SDK
tomorrow; making it a protocol-level guarantee, enforced the same way
regardless of which client calls it, is a different and harder
commitment than a client-side habit.

**2. A continuously logged reuse record — evidence the discipline works, not the discipline itself.**
Competitors make efficiency claims in marketing copy (a percentage figure against a benchmark, stated once). MAK4I's SAVINGS_LOG is designed as a running, dated ledger of actual reuse events — every reuse-vs-new-build decision logged as it happens, not summarized after the fact. Today that ledger reflects development-time observations (see [PROBLEM.md](PROBLEM.md)); the intent is for it to extend to real production usage once the Phase 2 reference implementation exists. This matters as *proof*, not as the mechanism: the protocol is the check-before-create discipline above; the log is what's meant to demonstrate that discipline produces value over time, closer to an audit trail than a benchmark claim.

**3. Skills as a registry-distributed unit, not a config file.**
OKF stores knowledge as markdown files living in *your* repo. Mem0 stores memories as API-retrievable facts about a user or session. Neither treats a *reusable process* (a deployment runbook, a triage framework, a document-generation pattern) as a versioned, publishable, installable package the way `mak4i install company/deployment-standards` does. This is closer to npm's model than either competitor's.

**4. MAK4I Certified — a conformance mark, not just a spec.**
No competitor above has a certification program for implementations. If MAK4I becomes the reference for "an AI reuse-discipline protocol," the certification mark is a coordination point competitors don't have.

---

## The Honest Positioning Statement

**What MAK4I is not:** the first or only open memory format. OKF got there first with more distribution. Mem0 has more funding and more developers today.

**What MAK4I is:** the protocol that treats *not rebuilding what you already built* as the primary discipline — enforced through a check-before-create workflow, evidenced by a continuously logged reuse record, and distributed through a registry of reusable Skills, not just stored facts.

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
