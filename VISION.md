# MAK4I Vision

## The Long-Term Vision

MAK4I makes your Projects, Artifacts, and Skills permanent and portable
across every AI model, platform, and organization.

Just as Git standardized source control and npm standardized package distribution,
MAK4I standardizes knowledge continuity for AI.

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

Production evidence from WD Technology (as of July 2026):
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
| 0 — Foundation | Jul 2026 | Public repo, spec, problem statement ← **YOU ARE HERE** |
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
