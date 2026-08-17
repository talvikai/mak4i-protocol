# Competitive Landscape

*Last researched: August 17, 2026. This document is reviewed before every major release. It intentionally omits star counts, funding figures, and other metrics that change daily — the comparisons below focus on what each project architecturally does, which is stable regardless of when you're reading this.*

**See also:** [ARCHITECTURE.md](ARCHITECTURE.md) for how MAK4I positions itself as a runtime layer *above* the formats and stores named below, rather than a competing format or store.

Before going public, we did the research most protocols skip: who else is solving this problem, and does MAK4I still say something true and specific once you account for them? This document is revisited on a real cadence, not written once — the entries below reflect a second full pass, not the original.

**What changed since the first pass (August 2, 2026):** the ecosystem moved fast. Several projects that were pure stores in early August have since added provenance, trust metadata, and lifecycle fields. That's a real shift, and it narrows one part of what MAK4I originally claimed. It does not narrow the part that actually matters most: nobody else enforces reuse-before-generate as a protocol-level runtime behavior. That distinction is explained in detail below, not asserted.

---

## The Landscape as of August 17, 2026

### Direct protocol competitors

**Open Knowledge Format (OKF)** — Google Cloud, v0.1 published June 12, 2026; **v0.2 published July 24, 2026**
A vendor-neutral, Apache 2.0 spec for representing team/system knowledge as a directory of markdown files with YAML frontmatter. Still explicitly "format, not platform" — no SDK, no runtime, no registry required.

**v0.2 is a material update, worth naming precisely rather than glossing over:** it adds `sources` (provenance signals — external doc, bundle-relative path, or scope descriptor, plus `author`/`usage_count`/`last_modified`), `generated`/`verified` (trust — a consumer derives an *unverified / machine-confirmed / human-reviewed* tier from these), `status`/`stale_after` (lifecycle), and a new `Attested Computation` concept type that binds a sanctioned computation to a deterministic, non-LLM verifier. OKF now covers provenance, trust signals, and lifecycle metadata as first-class frontmatter — three things earlier versions of this document called out as gaps in the format layer. That gap is smaller now. Say so plainly rather than pretending v0.2 didn't happen.

**What v0.2 still deliberately does not do:** OKF's own framing is "adds vocabulary, not rules." It records that a concept is stale, verified, or has sources — it does not check the registry before a new concept is written, does not block an agent from regenerating something that already exists, and has no enforcement mechanism of its own. A small, independent ecosystem of Claude Code plugins has grown around OKF (the most complete example ships an *opt-in* Stop-hook that blocks finishing a session if tracked files changed but the OKF log wasn't updated) — real enforcement, but of *documentation upkeep*, not of *reuse before generation*. That distinction is the whole of MAK4I's remaining differentiation from OKF, and it's worth being precise about it rather than vague.

**Where this leaves MAK4I relative to OKF:** MAK4I does not need to compete with OKF's metadata vocabulary — it can consume it. An artifact described in OKF's frontmatter format is a legitimate input to MAK4I's discovery step; OKF's trust tiers are useful signals a MAK4I client can weigh when deciding whether to reuse or adapt. MAK4I's job starts where OKF's stops: enforcing that discovery happens before generation, not just making the resulting metadata legible.

**Open Memory Protocol (OMP)** — community, GitHub
A vendor-neutral spec for AI tools to store, retrieve, and share memory about users and context, with adapters distributed across several major coding tools. Architecturally, OMP is a store-and-retrieve spec: it standardizes the *shape* of memory records, not a discipline for deciding when to reuse versus regenerate. Uses `semantic` as a memory type — the same term MAK4I uses. Apache 2.0. No enforcement mechanism; unchanged in kind since the last review, though the name "OMP" is now used by more than one unrelated project in this space — worth double-checking which one a given reference means.

### Funded commercial memory layers

**Mem0** — the dominant venture-funded "memory API" for agent builders: add/search/update/delete operations scoped to a user, session, or agent. Architecturally a managed store behind an API, not a protocol — adopting Mem0 means depending on their hosted service and schema. Shipped a token-efficient extraction/retrieval algorithm in April 2026; subsequent activity has been retrieval-quality and integration engineering, not a shift toward reuse enforcement or an open protocol model. Still a pure store: no discovery-before-generation step, no artifact lifecycle beyond memory CRUD.

**ByteRover** — newly relevant, not previously covered. An agent-native memory system built as a hierarchical, file-based "Context Tree" of human-readable markdown rather than a vector or graph database, with explicit relations between entries, provenance, and what it calls an "Adaptive Knowledge Lifecycle" — importance scoring, maturity tiers, and recency-based decay of older entries. This is architecturally the closest thing in the current landscape to MAK4I's own lifecycle and provenance framing. It is still, however, a memory/knowledge substrate: it does not enforce a check-before-create step, and reuse of an existing entry is something a client *can* do, not something the protocol *requires*. Worth monitoring directly — if ByteRover adds an enforced reuse gate on top of its existing lifecycle model, the gap between it and MAK4I narrows further.

**Supermemory** — MIT-licensed core with a commercial hosted layer for connectors, team sharing, and compliance. This is the same open-core-plus-hosted-platform model MAK4I uses. Store-and-retrieve architecture; no reuse-enforcement layer.

**Zep** — Temporal knowledge graph (open-sourced as Graphiti), strongest at "who changed what when." Architecturally distinct from the flat-store approach most competitors take, and its temporal-fact model is a genuine alternative to episodic-style history — but it answers "what changed and when," not "should this be reused instead of regenerated."

**Letta (formerly MemGPT)** — OS-inspired paged memory, academic roots, strong in research and agent-framework contexts. Unchanged in kind since the last review.

### Enterprise artifact/skill registries — newly relevant category

A cluster of enterprise products has emerged around the specific language of "discover and reuse before rebuilding" — closer in *marketing* to MAK4I's positioning than the memory-layer products above, worth naming directly rather than lumping in with stores. Products in this space (TrueFoundry's Skills Registry, and similar "artifact registry for AI" offerings from infrastructure vendors) market centralized discovery, versioning, and governance of agent skills as reusable, portable, executable assets — genuinely adjacent framing. The distinction that still holds: these are commercial registry *products*, not an open protocol, and in every case found, reuse is a capability the registry offers a user, not a rule the protocol enforces before generation is allowed to happen. If reuse is optional, it is a feature. MAK4I's claim is narrower and stricter: reuse-before-generate is specified as protocol behavior, not left to whether a team remembers to check the registry first.

### Native platform memory (the baseline, not a competitor)

Every major AI platform now ships persistent memory, and several have added cross-platform *import* — Claude, Gemini, and others can import memory or chat history from a competing assistant via a one-time, prompt-based transfer. This is real progress on portability as a *user-facing feature*, but it is not a shared standard: no major provider has published a standardized memory export schema, and each import path is a bespoke, one-directional bridge rather than a common format any tool can read or write. None of it travels natively between platforms on an ongoing basis, and none of it involves reuse-before-generate — importing a memory is not the same as checking whether an artifact already exists before building a new one. This remains the baseline problem the entire category — including MAK4I — exists to address, not a competing solution to it.

### Academic work (research, not a shipped competitor)

**Portable Agent Memory** (Ravindran, arXiv:2605.11032, May 2026) — a single-author cryptography/security paper, not a company or funded product. Its actual contribution is narrower and different from MAK4I's: a five-component memory model with Merkle-DAG provenance for tamper-evidence, capability-based access scoping, and an injection-resistant rehydration protocol specifically defending against indirect prompt injection during cross-model memory transfer. It uses the same episodic/semantic/procedural categorization MAK4I uses — worth acknowledging directly rather than pretending the overlap doesn't exist — but its center of gravity is memory security and integrity, not the check-before-create reuse discipline that is MAK4I's actual differentiator. Traction remains minimal: no confirmed author follow-up, and at most a small number of citing works. No registry, no reuse enforcement, no production adoption. Worth revisiting if this moves from a preprint toward an adopted standard or a funded product, but nothing found in this pass changes that assessment.

### MCP and the Agentic AI Foundation — infrastructure, not a competitor

MCP is now governed by the Linux Foundation's Agentic AI Foundation, with continued work on server discovery (metadata files that let a client find and evaluate an MCP server before connecting, similar in spirit to a package registry's listing page). This is relevant infrastructure MAK4I can build on — a natural transport for artifact discovery calls — but it is a tool-connection standard, not a memory or artifact-reuse standard. No MCP-native artifact registry or reuse-discipline standard has emerged from this governance body. Complementary, not competitive, consistent with [MCP.md](MCP.md).

---

## What MAK4I No Longer Gets to Claim Alone

Being direct about this matters more than sounding original. This list has grown since the last review — the honest response to that is naming it, not softening it:

- "Open protocol for portable AI memory" — OKF and OMP already say this, and OKF shipped first with Google's distribution behind it.
- "Works across Claude, Cursor, ChatGPT" — table stakes; every project above claims the same.
- "Three memory types" (procedural/semantic/episodic) — OMP already uses `semantic` as a type name, and the Ravindran paper uses the same three-part split; the taxonomy itself isn't a moat, and is now a converging industry norm rather than a MAK4I-specific framing.
- "MCP server for memory" — OMP already ships one.
- "Vendor-neutral, no lock-in" — the entire category positions this way now.
- **"Artifacts carry provenance, trust signals, and lifecycle metadata"** — this was a defensible differentiator against OKF v0.1. It is not one against OKF v0.2, which now defines all three at the format level. ByteRover independently arrived at a similar lifecycle model. This is no longer something MAK4I can claim as unique, and this document should not imply otherwise anywhere else in the repo.

If MAK4I launches saying only these things, the first credible comment on Hacker News will be "how is this different from OKF v0.2?" — and we need an answer that isn't defensive. The answer is below, and it is narrower than it was two weeks ago.

---

## What MAK4I Still Defends

**1. Reuse discipline as protocol-level, enforced behavior — the primary differentiator, and the only one that hasn't been matched.**
Every competitor above — including OKF v0.2, including ByteRover, including the enterprise registries marketing "discover before you build" — makes reuse *possible* or *legible*. None of them make it *required*. OKF v0.2 lets you know an artifact is stale or verified; it doesn't stop an agent from writing a duplicate one. ByteRover's lifecycle model decays old entries; it doesn't block generation of a new entry that duplicates a live one. The enterprise registries are searchable catalogs — search is optional. MAK4I specifies discovery-before-generation as protocol behavior, not an optional client-side convention:

- **Discovery** — search the registry before generating anything new
- **Reuse** — return an exact match directly, no regeneration
- **Adaptation** — modify an existing artifact when a close-but-not-exact match exists
- **Provenance and lifecycle metadata** — consumed where available (including from OKF-formatted sources), not reinvented
- **Enforcement** — the check-before-create step is a protocol guarantee, not a habit a well-behaved client happens to follow

A competitor could add a "check first" convention to their own SDK tomorrow; making it a protocol-level guarantee, enforced the same way regardless of which client calls it, is a different and harder commitment than a client-side habit. This gap has not closed in this review cycle — if anything, the broader industry conversation about hallucinated resource names and unvetted skill installs (see Security Positioning, below) makes the case for enforcement stronger than it was two weeks ago.

**2. A continuously logged reuse record — evidence the discipline works, not the discipline itself.**
Competitors make efficiency claims in marketing copy (a percentage figure against a benchmark, stated once). MAK4I's SAVINGS_LOG is designed as a running, dated ledger of actual reuse events — every reuse-vs-new-build decision logged as it happens, not summarized after the fact. Today that ledger reflects development-time observations (see [PROBLEM.md](PROBLEM.md)); the intent is for it to extend to real production usage once the Phase 2 reference implementation exists. This matters as *proof*, not as the mechanism: the protocol is the check-before-create discipline above; the log is what's meant to demonstrate that discipline produces value over time, closer to an audit trail than a benchmark claim.

**3. Skills as a registry-distributed unit, not a config file.**
OKF stores knowledge as markdown files living in *your* repo. Mem0 and ByteRover store memories as API-retrievable or file-based entries scoped to a session or project. None of them treat a *reusable process* (a deployment runbook, a triage framework, a document-generation pattern) as a versioned, publishable, installable package the way `mak4i install company/deployment-standards` does. This is closer to npm's model than any competitor's.

**4. MAK4I Certified — a conformance mark, not just a spec.**
No competitor above has a certification program for implementations. If MAK4I becomes the reference for "an AI reuse-discipline protocol," the certification mark is a coordination point competitors don't have.

---

## Security Positioning

This is new to this review, and it strengthens the case for enforcement rather than metadata alone — worth stating plainly rather than overstating.

Independent security research published mid-2026 documented AI coding assistants hallucinating plausible-sounding but nonexistent resource names — package names, repository names, skill names — at a high rate when asked to fetch or install something, creating an opening for attackers to register those exact names in advance ("squatting" on a name an agent is statistically likely to hallucinate and then request). Separately, independent researchers demonstrated that malicious agent skills could be constructed to bypass multiple third-party skill scanners with modest effort. Neither finding is about MAK4I specifically, and neither should be overstated as validating MAK4I directly — but both point at the same underlying fix that the research community has converged on: **an agent should search for whether something already exists, from a trusted source, before fetching or installing it new.** That is a description of check-before-create as a security control, not just an efficiency one. It's a legitimate, additional reason the discipline matters, alongside the original reuse/waste argument — not a claim that MAK4I has been validated by name, which it has not.

---

## The Honest Positioning Statement

**What MAK4I is not:** the first or only open memory format, and — as of this review — no longer the only project describing provenance or lifecycle metadata. OKF got there first on distribution. Mem0 has more funding and more developers today. ByteRover independently arrived at a similar lifecycle model.

**What MAK4I is:** the protocol that treats *not rebuilding what you already built* as an enforced discipline, not an optional convenience — the only project reviewed here that makes discovery-before-generation a protocol guarantee rather than a feature a client can choose to skip. This is evidenced by a continuously logged reuse record, and distributed through a registry of reusable Skills, not just stored facts.

If a team's problem is "the AI doesn't remember my preferences" → Mem0 or native platform memory solves that.
If a team's problem is "our knowledge should live in files, not a vendor's database, and I want provenance and staleness tracked" → OKF v0.2 solves that, and MAK4I can consume it.
If a team's problem is "we keep paying to regenerate things we already built, and nothing actually stops that from happening again" → that's the MAK4I problem, and nobody else reviewed here enforces the fix.

---

## What This Means for Launch

- Lead with the reuse-*enforcement* framing in README.md and the launch post — not "portable AI memory," and not "provenance and lifecycle metadata" as a headline claim, since that's no longer differentiated.
- Position MAK4I as complementary to OKF v0.2 explicitly, including in any launch post — a reader who knows OKF will ask this question regardless, and answering it before being asked is stronger than answering it defensively in the comments.
- Cite OKF, Mem0, and ByteRover by name. Silence on obvious prior art reads as either not having done the research or hoping nobody asks — both worse than addressing it directly.
- The SAVINGS_LOG becomes the centerpiece of the pitch, not a supporting appendix. It is the one piece of evidence competitors cannot copy retroactively.
- Do not claim MAK4I invented provenance, trust metadata, or lifecycle tracking. That claim was defensible on August 2. It is not defensible on August 17, and saying it anyway would be the first thing a technically sharp reader catches.

---

## Industry Convergence — What's Settling vs. What Isn't

As of this review, the broader ecosystem is converging on:
- Memory as a baseline platform feature (every major assistant has it)
- Provenance metadata (OKF v0.2, ByteRover)
- Lifecycle/staleness tracking (OKF v0.2, ByteRover)
- Cross-platform memory *import* as a user-facing convenience (not a shared standard)
- Episodic/semantic/procedural-style taxonomies for categorizing agent knowledge

It is **not** converging on:
- Protocol-level, enforced reuse-before-generate
- Runtime governance sitting above formats and stores, rather than being one itself
- Standardized artifact lifecycle *actions* (deprecate, adapt, supersede) as opposed to lifecycle *metadata* (a stale-after date sitting inert until someone reads it)
- A certification program for conformant implementations

The first list is where the ground has moved under this document since August 2 — pretending otherwise would be the least credible thing this document could do. The second list is where MAK4I still has the field to itself, and it's a narrower field than it was two weeks ago, not the same one.

---

*This document will be revisited before each major MAK4I release. The competitive landscape in AI memory/context tooling is moving in weeks, not months — treat this page as perishable, not settled.*
