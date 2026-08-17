# MAK4I Vision

*This document covers the long-term vision, core philosophy, and a
high-level view of the architecture and roadmap. For the detailed
version of each, see:*

- *[ARCHITECTURE.md](ARCHITECTURE.md) — full runtime, registry, and
  storage adapter architecture*
- *[ROADMAP.md](ROADMAP.md) — complete phase-by-phase roadmap and the
  Phase 2/5 integration workflow*
- *[MCP.md](MCP.md) — how MAK4I relates to the Model Context Protocol*
- *[BUSINESS_MODEL.md](BUSINESS_MODEL.md) — pricing tiers and the
  Talvik/WD Technology relationship*
- *[DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) — CLI, SDK, and tooling*

---

## The Long-Term Vision

MAK4I makes your Projects, Artifacts, and Skills permanent and portable
across every AI model, platform, and organization.

Just as Git standardized source control and npm standardized package distribution,
MAK4I standardizes knowledge continuity for AI.

---

## High-Level Architecture

MAK4I is not another memory format, and not another memory store. It's a
runtime layer that sits above whatever format or store a team already
uses, adding the discipline that neither formats nor stores enforce on
their own: checking whether an artifact already exists — and reusing or
adapting it — *before* generating something new. Formats like OKF define
what an artifact's metadata looks like, including provenance and
lifecycle fields; MAK4I defines what happens at the moment of creation,
which no format enforces by itself.

```
        Applications (Claude Code, Cursor, ChatGPT, Gemini, ...)
                              │
                        MCP / SDK / API
                              │
                     MAK4I Memory Runtime
                              │
                  Format and storage adapters
```

The full version of this diagram — including the detailed runtime
responsibilities and the honest breakdown of what's actually implemented
today versus roadmap — is in [ARCHITECTURE.md](ARCHITECTURE.md).

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

Every AI tool represents reusable knowledge differently, and none of those
representations travel between tools. The full problem statement — the
scale of the waste this causes, the portability gap between platforms, and
the economic impact — lives in [PROBLEM.md](PROBLEM.md).

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
  mak4i-artifact-schema       The MAK4I data model
  company-api-contracts       Your internal API specifications
  domain-glossary             Your business terminology
  database-schema             Your current table structure

Once stored as a MAK4I artifact:
  mak4i inject company-api-contracts
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

## The Analogy

| Standard | What it standardized | Ecosystem built on top |
|----------|---------------------|----------------------|
| Git | How code changes are tracked | GitHub, GitLab, Bitbucket |
| npm | How packages are published and consumed | npmjs.com, Yarn, pnpm |
| Docker | How applications are packaged | Docker Hub, registries |
| Kubernetes | How containers are orchestrated | GKE, EKS, AKS |
| **MAK4I** | **How AI Skills, Knowledge, and History are stored and injected** | **Talvik Registry, Enterprise** |

The protocol is open forever. The ecosystem is built on top. See
[BUSINESS_MODEL.md](BUSINESS_MODEL.md) for how that ecosystem generates
revenue without compromising the open protocol.

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

The full phase-by-phase roadmap, including the Phase 2 and Phase 5
integration workflow, is in [ROADMAP.md](ROADMAP.md). Summary:

| Phase | When | Key Output |
|-------|------|-----------|
| 0 — Foundation | Aug 2026 | Public repo, spec, problem statement ← **YOU ARE HERE** |
| 1 — Protocol Spec | Aug-Sep 2026 | SPEC.md v1.0, community RFC open |
| 2 — Reference Impl | Oct-Nov 2026 | Python + Node.js SDK, CLI |
| 3 — First Artifacts | Dec 2026 | 10+ community artifacts open source |
| 4 — Hosted Registry | Jan-Feb 2027 | Public registry, free tier live |
| 5 — MCP Integration | Feb-Mar 2027 | Native support for MCP-compatible tools |
| 6 — Funding | Apr-Jun 2027 | Pre-seed conversations with production data |

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
