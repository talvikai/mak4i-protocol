# Developer Guide

*Planned developer tooling and integration experience for MAK4I. The
tools described in this document are roadmap targets and are not
available in Phase 0 unless explicitly stated otherwise.*

*CLI, SDK, Registry UI, and editor/CI integrations for building with
MAK4I. See [ARCHITECTURE.md](ARCHITECTURE.md) for the underlying API
these tools call, and [MCP.md](MCP.md) for the MCP integration path.*

------------------------------------------------------------------------

## Current Status

MAK4I is currently in Phase 0.

The CLI, SDKs, hosted Registry UI, VS Code extension, GitHub Action, and
MCP server described below are planned capabilities. Their commands,
APIs, interfaces, and behavior may change as the reference
implementation is developed.

The examples in this document illustrate the intended developer
experience; they are not currently available production interfaces.

------------------------------------------------------------------------

## Developer Tools

MAK4I is intended to support both AI systems and developers through a
broader developer ecosystem.

There are two distinct users of MAK4I:

    AI Systems (planned via MCP server):
      MCP-compatible AI tools will be able to connect to MAK4I
      They will be able to discover and consume relevant artifacts
      MAK4I can provide reusable context through the integration

    Developers (via dev tools):
      Humans who BUILD with MAK4I
      They create, publish, and manage artifacts
      They integrate MAK4I into their products and pipelines

### Planned Tool 1 --- MAK4I CLI

The CLI is planned as the primary command-line interface for developers.

``` bash
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

------------------------------------------------------------------------

### Planned Tool 2 --- MAK4I SDK

For developers who want to integrate MAK4I into their own code.

``` python
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

Additional language SDKs may follow in later phases.

Comparable to: Stripe SDK, Twilio SDK, Anthropic SDK

------------------------------------------------------------------------

### Planned Tool 3 --- MAK4I Registry UI

Planned hosted Registry UI (Phase 4)

-   Browse and search published artifacts
-   Manage organization artifact packs
-   View team token savings analytics
-   Create and manage teams
-   One-click install to any project

Comparable to: npmjs.com, Docker Hub, PyPI

------------------------------------------------------------------------

### Planned Tool 4 --- MAK4I VS Code Extension

Planned editor integration (Phase 4+)

-   Search and install artifacts without leaving VS Code
-   See which artifacts are loaded for the current project
-   View token savings in real time
-   One-click inject before opening Claude Code
-   Create new artifacts from selected code

Comparable to: GitLens, Prettier, ESLint plugins

------------------------------------------------------------------------

### Planned Tool 5 --- MAK4I GitHub Action

Planned CI/CD integration for artifact management (Phase 4+)

``` yaml
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

What it does: - Auto-publishes new artifacts on merge - Validates
artifacts against MAK-0001 on every PR - Posts token savings summary to
PR comments - Keeps team artifact registry in sync with codebase

------------------------------------------------------------------------

### The Developer Day-to-Day Experience

**Without MAK4I:**

    Developer opens Claude Code.
    "Before we start, our stack is Node.js,
     we use PostgreSQL, our API follows REST,
     here are our naming conventions..."

    Next day, new session: same explanation again.
    New team member joins: weeks of onboarding.

**With MAK4I:**

``` bash
mak4i inject
# Relevant project artifacts are made available to the
# connected AI tool, including standards, patterns,
# and conventions.

# New team member joins:
mak4i install company/*
```

------------------------------------------------------------------------

### Intended Developer Value

    Problem they recognize immediately:
      "I explain my stack to Claude every single day"
      "AI suggestions don't follow our team standards"
      "New hires take weeks to get productive with AI tools"

    Intended developer experience:
      mak4i inject     → provide relevant project context without
                         repeatedly re-explaining it
      mak4i install    → make shared team artifacts available to
                         compatible tools
      mak4i publish    → publish reusable artifacts for team reuse

    Planned measurement:
      mak4i logs       → provide visibility into measured reuse and
                         associated token savings

------------------------------------------------------------------------

### MAK4I for Enterprise Development Teams

When an organization adopts MAK4I:

    Platform/IT team publishes once:
      company/security-policies
      company/coding-standards
      company/api-contracts
      company/deployment-runbooks
      company/incident-playbooks

    Every developer installs once:
      mak4i install company/*

    Intended result:
      Shared organizational artifacts can be made available
      to compatible AI tools.
      Designed to reduce repeated onboarding context.
      Provides AI systems with access to shared organizational
      standards and policies.
      Planned tooling will provide measurement and reporting
      of reuse and associated token savings.

This is the enterprise value proposition: not just developer
productivity --- organizational AI alignment.

------------------------------------------------------------------------

### The npm Parallel

    npm:                          MAK4I:
      Reusable code packages        Reusable AI artifacts
      npm registry                  MAK4I Registry
      npm CLI                       mak4i CLI
      package.json                  mak4i.json
      npm install lodash            mak4i install company/standards
      npm publish                   mak4i publish

    npm standardized how developers share code.
    MAK4I aims to standardize how reusable AI artifacts are shared, discovered, and reused.

------------------------------------------------------------------------
