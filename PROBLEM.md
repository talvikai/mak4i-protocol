# The Problem MAK4I Solves

## Every AI Platform Solves This Differently

Every AI tool has its own way to represent reusable knowledge.

```
Claude has Projects, Artifacts, and Skills.
Cursor has Rules.
ChatGPT has Memory.
GitHub Copilot has Instructions.
```

Every platform invents its own format. None of them are portable.

To make this concrete, the rest of this document uses Claude's
terminology — Projects, Artifacts, Skills — as a worked example. Every
term below has an equivalent in every other platform above, under a
different name and a different, incompatible format.

If you use Claude, you already understand three things:

```
Projects    A way to group related conversations, files, and context.
            "Everything about my product lives in this Project."

Artifacts   What Claude generates for you — a document, a component,
            a workflow, a code framework. The OUTPUT of a session.

Skills      Repeatable processes that use Artifacts to produce
            consistent results every time.
            "Always generate my fix docs this way."
            "Always triage issues using this framework."
```

These three things are powerful.

**But they only work inside Claude.ai.**

---

## Why a Protocol?

Today's AI platforms all represent reusable knowledge differently.

Claude has Skills. Cursor has Rules. ChatGPT has Memory. GitHub Copilot
has Instructions. Every platform invents its own format.

MAK4I does not replace those systems. It standardizes how reusable AI
artifacts are packaged, identified, versioned, shared, discovered, and
reused across tools — regardless of which platform's native format they
started in.

Just as Git standardized source control, MAK4I standardizes reusable AI
artifacts.

---

## The Problem

```
Your Projects    → locked inside Claude.ai
Your Artifacts   → disappear when the session ends
Your Skills      → can't be used in Claude Code, Cursor, or ChatGPT
```

Start a new session — your Skills are gone.
Switch to a different AI tool — start from zero.
Bring a new team member on — they have none of your context.

Every session, every tool, every team member starts cold.

---

## What "Starting Cold" Costs

Every time a session starts cold, the AI regenerates things
that already exist:

```
Skills re-explained:
  "Here's how I want you to triage issues..."
  "Here's the format for my fix documents..."
  "Here's how we deploy to Cloud Run..."

Artifacts re-generated:
  The same deployment workflow. Again.
  The same code scaffold. Again.
  The same architecture diagram. Again.

Project context re-established:
  "My stack is Firebase Auth, React, Node.js, GCP Cloud Run..."
  "We're building an appointment scheduling SaaS called Schedovia..."
  "We use Square for payments and Twilio for SMS..."
```

This is not just annoying. It is measurable waste, at a scale covered in
the [Appendix: Economic Impact](#appendix-economic-impact) below.

---

## Three Types of Waste — Mapped to What You Already Know

### Skill Waste — repeatable processes re-explained every session

Your Skills are the most painful to lose. You spent time defining
exactly how you want the AI to work. You tuned the output format.
You got it right. Then the session ends and it's gone.

```
Example:
  You taught Claude your issue triage framework.
  P0 = blocking pilots. P1 = fix this sprint.
  Perfect format. Consistent output.
  
  Next session: gone.
  You re-explain it from scratch.
  The AI gets it slightly wrong.
  You correct it. Again.
```

### Knowledge Waste — project context re-uploaded every session

Your Project knowledge — your stack, your architecture, your API
contracts — hasn't changed. But every session you re-upload it,
re-explain it, or paste it in manually.

```
Example:
  "My stack is Firebase Auth, React, Node.js,
   GCP Cloud Run us-east5, Cloud SQL PostgreSQL,
   Memorystore Redis, Twilio, Resend, Square..."
   
  You type this every. single. session.
  Or you paste it from a notes file.
  Manual, error-prone, doesn't scale.
```

### History Waste — decisions re-litigated every session

Your team made an architecture decision three months ago.
You documented the reasoning. Now a new session starts and
the AI suggests the exact thing you decided against.

```
Example:
  "We chose Firebase Auth over Auth0 because..."
  "We deferred multi-location to v2.0 because..."
  "We picked Square for pilots because..."
  
  Without history, the AI re-opens closed decisions.
  You waste time re-litigating instead of building.
```

---

## The Portability Gap

Every AI platform has created its own representation of reusable
knowledge — Claude, Cursor, Copilot, Gemini, ChatGPT, and every platform
that comes after them.

**None of those formats are interoperable. Teams end up rebuilding the
same knowledge for every platform.**

```
Claude Skill    →  can't use in Cursor
Cursor Rule     →  can't use in Claude Code
Claude Artifact →  can't inject into ChatGPT
Claude Project  →  can't share with a Copilot user

Your team member uses Cursor.
You use Claude Code.
Neither of you has access to the other's reusable knowledge —
even when it describes the exact same project.
```

You're not just losing context between sessions.
You're losing it between tools, between team members,
and between every model upgrade.

---

## Early Evidence, and What's Next

MAK4I's reuse mechanism was first demonstrated informally during its own
development: rather than regenerating documents, code patterns, and other
artifacts from scratch each time a similar need came up, existing artifacts
were checked for and reused. The figures below come from that development
process — not from a live API or production traffic, since the API does
not yet exist (see [ROADMAP.md](ROADMAP.md), Phase 2).

| Metric | Value |
|--------|-------|
| Tokens saved (dev-time observation) | 38,400+ |
| Sessions tracked | 29 |
| Artifacts registered | 9 across 6 types |

### What was saved and how:

| Artifact | What it is | Tokens saved per use |
|----------|-----------|---------------------|
| wd-docx-framework | Skill — how to generate professional documents | 1,200 |
| schedovia-stack-context | Knowledge — full project stack and architecture | 1,500 |
| issue-triage-framework | Skill — how to triage P0/P1/P2/P3 issues | 400 |
| cloud-run-429-diagnosis | History — diagnosis pattern from a real incident | 350 |
| gcp-wildcard-cert-godaddy | Skill — how to provision SSL certs on GCP | 500 |
| multitenant-slug-auth-pattern | Skill — reusable auth pattern for SaaS | 600 |
| appointment-parser-prompt | Skill — how to parse appointments from SMS | 250 |

These are development-time observations, not measured production savings.
Production validation is planned for Phase 2, once the reference API exists
and WD Technology Solutions (Schedovia, and AIOps, a MAK4I-native product
in planning) becomes the first real integration target.

---

## Why Existing Solutions Don't Solve This

### Claude Projects / ChatGPT Projects
- Groups conversations within one tool — doesn't travel between tools
- Resets when you switch models or tools
- Not designed for team sharing or versioning
- No community ecosystem

### Claude Skills / Cursor Rules / Copilot Instructions
- Each tool has its own version — none are portable
- A Claude Skill can't be used in Cursor
- A Cursor Rule can't be used in Claude Code
- No standard format — every tool reinvents this

### Claude Memory / ChatGPT Memory
- Covers personal preferences — not project knowledge
- Not shareable with team members
- No versioning — memory changes silently
- Locked to one platform

### Model Context Protocol (MCP)
- Defines how AI tools connect to data sources (the transport)
- Does not define how knowledge is stored, versioned, or structured
- MAK4I is complementary to MCP — MAK4I becomes an MCP server
- MCP moves data. MAK4I defines what the data IS.

### Copy-paste context
- What most developers do today
- Manual, error-prone, doesn't scale
- No versioning, no sharing, no consistency
- MAK4I standardizes what people are already doing manually

---

## The Solution

MAK4I makes your Projects, Artifacts, and Skills permanent and portable.

```
With MAK4I:

  Your Skills     → stored, versioned, injectable into any AI tool
  Your Artifacts  → saved permanently, not lost when sessions end
  Your Knowledge  → travels with you across Claude, Cursor, ChatGPT
  Your History    → preserved, preventing decisions from being re-opened

  mak4i inject
  → Every session starts with your Skills loaded
  → Every session starts with your Project context loaded
  → Every session continues where the last one left off
  → Works in Claude, Claude Code, Cursor, any MCP-compatible tool
```

Write once. Use anywhere. Never start from zero.

MAK4I standardizes reusable AI artifacts the same way Git standardized
source code and npm standardized package distribution. The protocol lets
artifacts move between models, IDEs, organizations, and future AI
platforms — without rewriting or regenerating them.

[Read the specification →](SPEC.md)

---

## Appendix: Economic Impact

```
1,000,000 AI sessions per day
× 1,000 tokens wasted per session re-establishing context
= 1,000,000,000 tokens per day in avoidable generation
```

**1 billion tokens per day. Every day.**

As AI moves toward metered compute billing — Sam Altman has stated
publicly that AI will eventually be billed like electricity — that waste
becomes a direct dollar cost for every business running AI at scale.

It is also an environmental cost. Measurable electricity. Measurable water.
Measurable carbon. Generated to reproduce knowledge that already existed.

This calculation illustrates scale; it is not a measurement of any
specific organization's usage.

---

*© 2026 Talvik, Inc.*
