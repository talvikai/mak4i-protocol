# Developer Guide

*CLI, SDK, Registry UI, and editor/CI integrations for building with
MAK4I. See [ARCHITECTURE.md](ARCHITECTURE.md) for the underlying API
these tools call, and [MCP.md](MCP.md) for the MCP integration path.*

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

