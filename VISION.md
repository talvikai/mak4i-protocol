# MAK4I Vision

## The Long-Term Vision

MAK4I makes your Projects, Artifacts, and Skills permanent and portable
across every AI model, platform, and organization.

Just as Git standardized source control and npm standardized package distribution,
MAK4I standardizes knowledge continuity for AI.

---

## Architecture — Where MAK4I Sits

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

**In one line:** OKF is a format. Mem0 is a store. MAK4I is the runtime that
governs memory access, trust, and reuse across all of them.

This placement matters for one specific reason: it's the honest answer to
*"why not just use OKF"* or *"how is this different from Mem0."* MAK4I doesn't
ask a team to abandon their format or store — it sits above whatever they
already chose and adds the discipline (check-before-create, provenance,
audit) that none of those layers enforce on their own. See
[COMPETITIVE_LANDSCAPE.md](COMPETITIVE_LANDSCAPE.md) for the full comparison.

### What v0.1 Actually Ships (August 2026)

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

Every box marked `roadmap` has a target phase in the [Roadmap](#roadmap)
section below. Nothing on this page claims to be built unless it is built —
if you clone this repo today, the `✓ implemented` boxes are what you get.

---

## Start Here — Three Things You Already Know

If you use Claude, you already understand this:

```
Projects    Group related conversations, files, and context together.
            "Everything about my product lives in this Project."

Artifacts   What Claude generates — documents, code, components,
            workflows. The OUTPUT of a Claude session.

Skills      Repeatable processes that produce consistent results.
            "Always triage issues this way."
            "Always generate my fix docs in this format."
            "Always deploy using this checklist."
```

These three concepts exist in every major AI tool:

| Concept | Claude | Cursor | GitHub Copilot | ChatGPT |
|---------|--------|--------|----------------|---------|
| Projects | Projects | Workspaces | Repositories | Projects |
| Artifacts | Artifacts | Generated files | Suggestions | Canvas |
| Skills | Skills | Rules | Instructions | Custom instructions |

**Every tool has its own version. None of them talk to each other.**

---

## The Problem MAK4I Solves

```
Claude Skill    → can't use in Cursor
Claude Artifact → can't inject into Claude Code  
Claude Project  → can't share with your team on ChatGPT

Switch tools:     start from zero
End a session:    Skills gone
New team member:  no context
Model upgrade:    history lost
```

Your Skills, Artifacts, and Project knowledge are locked inside
whichever tool created them. Every session, every tool, every
team member starts cold.

**MAK4I fixes this.**

---

## What MAK4I Does

```
Claude Artifact  =  Session OUTPUT
                    Claude generated something you can see
                    Lives in the browser session
                    Gone when you close the tab

MAK4I Artifact   =  Session INPUT
                    Permanent. Versioned. Portable.
                    Inject it into ANY AI session
                    Works across Claude, Cursor, ChatGPT, any tool
```

MAK4I is the layer between what AI tools generate and
what you can actually reuse — permanently, everywhere.

### From Claude to MAK4I in four steps:

```
Step 1:  Claude generates a deployment workflow (Artifact)
Step 2:  mak4i publish gcp-cloudrun-deploy
Step 3:  Next session: mak4i inject gcp-cloudrun-deploy
Step 4:  Claude already has the workflow — continue instantly

The Artifact was the output.
The MAK4I artifact is the preserved, reusable version.
MAK4I is the memory layer that makes Artifacts permanent.
```

---

## Three Memory Types — Mapped to What You Know

### Skills → Procedural artifacts (How)

Repeatable processes. The way you want things done.

```
Examples:
  issue-triage-framework      How to triage P0/P1/P2/P3
  gcp-cloudrun-deploy         How to deploy to Cloud Run
  claude-code-fix-doc         How to format fix requirements
  appointment-parser-prompt   How to parse appointments from SMS

Once stored as a MAK4I artifact:
  mak4i inject issue-triage-framework
  → Claude already knows your triage process
  → Same consistent output every session
  → Works in Claude Code, Cursor, any tool
```

### Knowledge → Semantic artifacts (What)

What is true about your project right now.

```
Examples:
  schedovia-stack-context     Your full tech stack and architecture
  mak4i-artifact-schema       The MAK4I data model
  company-api-contracts       Your internal API specifications
  domain-glossary             Your business terminology

Once stored as a MAK4I artifact:
  mak4i inject schedovia-stack-context
  → Claude knows your entire stack instantly
  → No re-explaining Firebase Auth, GCP, Twilio, Square
  → Start building immediately
```

### History → Episodic artifacts (Why)

What happened. Decisions made. Rationale preserved.

```
Examples:
  cloud-run-429-diagnosis     A real incident and how it was resolved
  architecture-decisions      Why you chose X over Y
  sprint-retrospectives       What the team learned each sprint
  pilot-feedback              What early customers said

Once stored as a MAK4I artifact:
  mak4i inject architecture-decisions
  → Claude won't re-suggest what you already decided against
  → History prevents re-litigating closed decisions
  → Institutional memory survives model upgrades
```

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

## The Analogy

| Standard | What it standardized | Ecosystem built on top |
|----------|---------------------|----------------------|
| Git | How code changes are tracked | GitHub, GitLab, Bitbucket |
| npm | How packages are published and consumed | npmjs.com, Yarn, pnpm |
| Docker | How applications are packaged | Docker Hub, registries |
| Kubernetes | How containers are orchestrated | GKE, EKS, AKS |
| **MAK4I** | **How AI Skills, Knowledge, and History are stored and injected** | **Talvik Registry, Enterprise** |

The protocol is open forever. The ecosystem is built on top.

---

## MCP Integration

MAK4I is complementary to Anthropic's Model Context Protocol (MCP).

```
MCP defines:    How AI tools connect to external data (the transport)
MAK4I defines:  What that data IS — Skills, Knowledge, History (the content)

They work together:
  MAK4I registry → exposed as MCP server
  Claude Code connects to MAK4I via MCP
  mak4i inject = MCP resource call
  
  Any MCP-compatible tool gets instant access
  to the full MAK4I registry — automatically
```

Think of it this way:

```
MCP  =  the USB-C standard (how devices connect)
MAK4I = the files on the drive (what gets transferred)

You need both.
MCP without MAK4I: a connection with nothing to transfer
MAK4I without MCP: content with no standard way to deliver it
```

Phase 5 of the MAK4I roadmap (Feb-Mar 2027) builds MAK4I as a native MCP server.
After that, any MCP-compatible tool — Claude Code, Cursor, Windsurf, and any
future AI tool — automatically gains access to MAK4I memory without additional
integration work.

---

## Two Companies, One Protocol

Talvik, Inc. builds MAK4I — the open protocol and enterprise platform.
WD Technology Solutions builds products on MAK4I — the first commercial adopter.

```
Talvik, Inc.
  MAK4I Protocol (open, MIT licensed)
    Talvik Registry (hosted)
      Talvik Enterprise (commercial)

WD Technology Solutions (first customer + design partner)
  Schedovia    — appointment scheduling SaaS
  Reminder AI  — SMS appointment reminders
  AIOps        — AI operations platform (coming 2027)
```

WD Technology products are not just revenue.
They are Talvik's best sales material.

**The AIOps connection:**

WD Technology's AIOps Platform is the most powerful proof point for Talvik's
enterprise story. AIOps powered by MAK4I — where AI agents know your
infrastructure, alert history, runbooks, and incident patterns without being
re-briefed every session — becomes the case study that sells MAK4I to enterprises.

```
Talvik pitch to a Fortune 500:
"WD Technology's AIOps platform runs on MAK4I.
 Engineers stopped re-explaining their infrastructure
 to the AI every session. Diagnosis time dropped 60%.
 Now imagine that across your 500 internal AI tools."
```

Production evidence from WD Technology (as of August 2026):
- 25,100+ tokens saved across 27 sessions
- 9 artifacts across 6 types in production
- 3 products using MAK4I
- Projected 12-month savings: ~3,000,000 tokens

---

## Standards Process

MAK4I uses the **MAK-XXXX** convention for protocol standards.

```
MAK-0001  Artifact Metadata Schema         (draft)
MAK-0002  Context Injection Specification  (planned)
MAK-0003  Memory Resolution Algorithm      (planned)
MAK-0004  Conflict Resolution Rules        (planned)
MAK-0005  Versioning and Compatibility     (planned)
```

Anyone can propose a new MAK standard via GitHub.
See [CONTRIBUTING.md](CONTRIBUTING.md) for the process.

### Conformance

Every implementation can be tested against the MAK4I Conformance Suite.
The **MAK4I Certified** badge signals full protocol conformance.
Similar to CNCF conformance for Kubernetes.

---

## Roadmap

| Phase | When | Key Output |
|-------|------|-----------|
| 0 — Foundation | Aug 2026 | Public repo, spec, problem statement ← **YOU ARE HERE** |
| 1 — Protocol Spec | Aug-Sep 2026 | SPEC.md v1.0, community RFC open |
| 2 — Reference Impl | Oct-Nov 2026 | Python + Node.js SDK, CLI |
| 3 — First Artifacts | Dec 2026 | 10+ community artifacts open source |
| 4 — Hosted Registry | Jan-Feb 2027 | Public registry, free tier live |
| 5 — MCP Integration | Feb-Mar 2027 | Native Claude Code + Cursor support |
| 6 — Funding | Apr-Jun 2027 | Pre-seed conversations with production data |

---

## Business Model

| Tier | What | Price |
|------|------|-------|
| Protocol | Full MAK4I spec, MIT licensed | Free forever |
| Community Registry | Public artifact marketplace | Free |
| Pro | Private artifacts, analytics, history | $15/month |
| Team | Shared org registry, admin, team Skills | $20/seat/month |
| Enterprise | Self-hosted, SSO, SLA, governance | Custom |

---

## Vision Statement

Claude has Projects, Artifacts, and Skills.
Every AI tool has its own version.
None of them talk to each other.

**MAK4I makes all three permanent and portable.**

Your Skills work in any AI tool.
Your Artifacts are saved forever.
Your Knowledge travels with you.

Write once. Use anywhere. Never start from zero.

*MAK4I is to AI sessions what npm is to Node.js.*

**Portable AI Memory. Open Forever.**

---

*© 2026 Talvik, Inc. — talvik.ai*

---

## Developer Tools

MAK4I is not just for AI models. It is a complete developer ecosystem.

There are two distinct users of MAK4I:

```
AI Models (via MCP server):
  Claude, Cursor, Copilot connect automatically
  They use artifacts without developer intervention
  The AI "knows things" because MAK4I injected them

Developers (via dev tools):
  Humans who BUILD with MAK4I
  They create, publish, and manage artifacts
  They integrate MAK4I into their products and pipelines
```

### Tool 1 — MAK4I CLI

The primary developer interface. Works from any terminal.

```bash
mak4i init                          # set up MAK4I in a project
mak4i inject                        # inject all relevant artifacts
mak4i install company/standards     # install an artifact pack
mak4i publish ./my-artifact.json    # publish to registry
mak4i search "fastapi deployment"   # search the registry
mak4i list                          # list installed artifacts
mak4i validate                      # validate against MAK-0001
mak4i diff v1.0 v1.1               # compare artifact versions
mak4i logs                          # view token savings
```

Comparable to: npm CLI, pip, git

---

### Tool 2 — MAK4I SDK

For developers who want to integrate MAK4I into their own code.

```python
# Python SDK (Phase 2)
from mak4i import MAK4IClient

client = MAK4IClient(api_key="...")

# Inject context before an AI call
context = client.inject(project="schedovia")

# Publish a new artifact programmatically
client.artifacts.publish({
    "id": "my-fastapi-scaffold",
    "type": "procedural",
    "content": scaffold_template,
    "token_estimate": 800
})

# Search the registry
results = client.artifacts.search("kubernetes deployment")
```

Node.js, Go, and Rust SDKs follow in later phases.

Comparable to: Stripe SDK, Twilio SDK, Anthropic SDK

---

### Tool 3 — MAK4I Registry UI

Web dashboard at registry.talvik.ai (Phase 4)

- Browse and search published artifacts
- Manage organization artifact packs
- View team token savings analytics
- Create and manage teams
- One-click install to any project

Comparable to: npmjs.com, Docker Hub, PyPI

---

### Tool 4 — MAK4I VS Code Extension

Right inside the editor (Phase 4+)

- Search and install artifacts without leaving VS Code
- See which artifacts are loaded for the current project
- View token savings in real time
- One-click inject before opening Claude Code
- Create new artifacts from selected code

Comparable to: GitLens, Prettier, ESLint plugins

---

### Tool 5 — MAK4I GitHub Action

Automate artifact management in CI/CD pipelines (Phase 4+)

```yaml
name: MAK4I Sync
on: [push]
jobs:
  sync:
    steps:
      - uses: talvikai/mak4i-action@v1
        with:
          api_key: ${{ secrets.MAK4I_KEY }}
          project: my-project
```

What it does:
- Auto-publishes new artifacts on merge
- Validates artifacts against MAK-0001 on every PR
- Posts token savings summary to PR comments
- Keeps team artifact registry in sync with codebase

---

### The Developer Day-to-Day Experience

**Without MAK4I:**
```
Developer opens Claude Code.
"Before we start, our stack is Node.js,
 we use PostgreSQL, our API follows REST,
 here are our naming conventions..."

Next day, new session: same explanation again.
New team member joins: weeks of onboarding.
```

**With MAK4I:**
```bash
mak4i inject
# Claude Code already knows your stack,
# standards, patterns, and conventions.
# Start building immediately.

# New team member joins:
mak4i install company/*
# Productive in hours, not weeks.
```

---

### Why Developers Adopt MAK4I

```
Problem they recognize immediately:
  "I explain my stack to Claude every single day"
  "AI suggestions don't follow our team standards"
  "New hires take weeks to get productive with AI tools"

Solution that's immediately obvious:
  mak4i inject     → never explain your stack again
  mak4i install    → AI follows your team standards
  mak4i publish    → share knowledge across the team

Proof they can verify:
  mak4i logs       → real token savings, measured honestly
```

---

### MAK4I for Enterprise Development Teams

When an organization adopts MAK4I:

```
Platform/IT team publishes once:
  company/security-policies
  company/coding-standards
  company/api-contracts
  company/deployment-runbooks
  company/incident-playbooks

Every developer installs once:
  mak4i install company/*

Result:
  Every developer's AI tool knows all company
  standards automatically.
  AI suggestions are always compliant.
  New hire onboards in hours not weeks.
  Token savings are measurable and reportable.
```

This is the enterprise value proposition:
not just developer productivity — organizational AI alignment.

---

### The npm Parallel

```
npm:                          MAK4I:
  Reusable code packages        Reusable AI knowledge
  npm registry                  MAK4I Registry
  npm CLI                       mak4i CLI
  package.json                  mak4i.json
  npm install lodash            mak4i install company/standards
  npm publish                   mak4i publish

npm standardized how developers share code.
MAK4I standardizes how developers share AI knowledge.
```

---

## How MAK4I Relates to MCP

A common question: **Is MAK4I competing with MCP?**

No. They solve different problems at different layers.

```
MCP defines:    How AI models connect to external tools
                (the transport and communication layer)

MAK4I defines:  What AI knowledge IS and how it's stored
                (the content and memory layer)

They work together:
  MAK4I Registry → exposed as MCP server
  AI tools connect to MAK4I via MCP
  MAK4I artifacts flow through MCP to the AI

MCP without MAK4I:  a connection with nothing persistent to transfer
MAK4I without MCP:  knowledge stored with no standard delivery method
Together:           persistent, portable AI memory delivered anywhere
```

### The Anthropic/MCP — Talvik/MAK4I Parallel

| | Anthropic + MCP | Talvik + MAK4I |
|---|---|---|
| Created | MCP protocol | MAK4I protocol |
| License | Apache 2.0 (open) | MIT (open) |
| Directly commercialize the protocol? | No | No |
| How they benefit | Claude API revenue grows as MCP drives more Claude usage | MAK4I Registry revenue grows as protocol adoption grows |
| What's paid | Claude API + Claude.ai subscriptions | Hosted Registry, Enterprise, Cloud API |
| Model-dependent? | Yes — MCP benefits Anthropic mainly when Claude is used | No — MAK4I earns revenue regardless of which AI model is used |
| Governance | Anthropic owned | Talvik owned (community steering committee planned) |

### The Key Difference

```
Anthropic with MCP:
  MCP makes Claude more useful
  Anthropic earns money from Claude — not from MCP
  If someone uses MCP with GPT-4 instead of Claude
  → Anthropic gets nothing from that usage

Talvik with MAK4I:
  MAK4I is model-agnostic by design
  Talvik earns money from the Registry — not from any AI model
  If someone uses MAK4I with GPT-4 instead of Claude
  → Talvik still earns Registry revenue

This makes Talvik's model more durable than Anthropic's MCP model.
MAK4I captures value from the memory layer
regardless of which AI model sits on top.
```

### The Closer Parallel — Git and GitHub

```
Git (protocol):
  Linus Torvalds created it
  Open source, free forever
  Linux Foundation governs it
  No direct commercialization of Git itself

GitHub (platform):
  Microsoft built the hosted platform on top
  Free for public repos
  Paid for private repos, teams, enterprise
  $7.5B acquisition by Microsoft in 2018

MAK4I (protocol):      Git equivalent
  Talvik created it
  Open source, MIT licensed, free forever
  Talvik governs it (community steering coming)

Talvik Registry (platform):   GitHub equivalent
  Talvik builds the hosted platform on top
  Free community tier
  Paid Pro, Team, Enterprise tiers
  The protocol drives adoption
  The platform captures the value
```

### Why Keeping the Protocol Open Is Rational

```
If MAK4I had a paid protocol:
  → Developers avoid it
  → Less adoption
  → Less registry revenue
  → Talvik fails

If MAK4I is free forever:
  → Developers adopt it freely
  → More adoption
  → More registry users
  → More enterprise customers
  → Talvik wins

The protocol being open is not a weakness.
It is the growth engine for the commercial platform.

This is why Git is free and GitHub is worth billions.
This is why Linux is free and Red Hat sold for $34B.
This is why Kubernetes is free and GKE generates
hundreds of millions for Google annually.

MAK4I will follow the same pattern.
```

### What Prevents a Fork from Competing?

A legitimate question: if MAK4I is open source,
can someone fork it and build a competing registry?

Yes. And that is fine.

```
A fork of MAK4I has:
  The protocol code ✓
  
A fork of MAK4I does NOT have:
  The community artifacts ✗
  The production evidence ✗
  The enterprise trust built over time ✗
  The first-mover brand recognition ✗
  The MAK4I Certified conformance ecosystem ✗

GitHub won not because it owned Git
but because it built the best platform,
the largest community, and the most trust.

Talvik wins the same way.
```
