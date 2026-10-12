# Developer Guide

*Planned developer tooling and integration experience for MAK4I. Except
where a section explicitly says otherwise, the tools described in this
document are roadmap targets and are not yet generally available.*

*CLI, SDK, Registry UI, and editor/CI integrations for building with
MAK4I. The normative interface these tools call is the MCP binding,
[MAK-0008](standards/MAK-0008.md); see also [MCP.md](MCP.md).*

------------------------------------------------------------------------

## Current Status

MAK4I is in Developer Preview.

A working reference implementation of the core protocol workflow exists.
It provides **MCP access** today (the ten [MAK-0008](standards/MAK-0008.md) tools, including
conflict listing and resolution), and an **operator CLI** for records,
conflicts and administration. Each implementation documents its own
tool ↔ CLI mapping ([MAK-0008 §10.3](standards/MAK-0008.md#10-tool-catalog)). Its source is
public at [talvikai/mak4i-reference](https://github.com/talvikai/mak4i-reference).

The Python SDK (contract: [MAK-0008 §13](standards/MAK-0008.md#13-client-requirements)), the hosted Registry UI,
other-language SDKs, a VS Code extension, a GitHub Action, and the
broader registry-oriented CLI described below are planned. Their
commands, APIs, interfaces, and behavior may change.

The examples in this document illustrate the intended developer
experience; except where noted, they are not currently available
production interfaces.

------------------------------------------------------------------------

## Developer Tools

MAK4I is intended to support both AI systems and developers through a
broader developer ecosystem.

There are two distinct users of MAK4I:

    AI Systems (via MCP server — working in the reference implementation):
      MCP-compatible AI clients connect to MAK4I
      They discover and consume relevant artifacts
      MAK4I provides reusable context through the integration

    Developers (via dev tools):
      Humans who BUILD with MAK4I
      They create, publish, and manage artifacts
      They integrate MAK4I into their products and pipelines

### MAK4I CLI

**Today (reference implementation):** an operator CLI. Illustrative
command names; the reference implementation's documentation is
authoritative —

``` bash
mak4i create ...            # record a new project record
mak4i supersede ...         # next version of a lineage
mak4i search ...            # deterministic lookup by type / tags / status
mak4i get-current ...       # current records plus conflicts
mak4i history ...           # every version in a lineage
mak4i conflict list|show|resolve ...   # MAK-0004 conflicts
mak4i doctor                # integrity report
# administration: organizations, projects, principals, grants,
# credentials, OAuth clients and authorizations, audit events
```

**Planned:** a broader registry-oriented CLI as the primary command-line
interface for developers —

``` bash
mak4i init                          # set up MAK4I in a project
mak4i inject                        # inject all relevant artifacts
mak4i install company/standards     # install an artifact pack
mak4i publish ./my-artifact.json    # publish to registry
mak4i list                          # list installed artifacts
mak4i validate                      # validate against MAK-0001
mak4i diff v1.0 v1.1                # compare artifact versions
mak4i logs                          # view token savings
```

Comparable to: npm CLI, pip, git

------------------------------------------------------------------------

### Planned Tool 2 --- MAK4I Python SDK

For developers who want to integrate MAK4I into their own code. The SDK
is a separate package, `mak4i-sdk` (import `mak4i_sdk`), that talks to
the same MCP endpoint AI clients use. Its client contract is
[MAK-0008 §13](standards/MAK-0008.md#13-client-requirements) and the CONFORMANCE Client/SDK profile.

``` python
# Python SDK (planned; interface subject to the SDK's own release)
from mak4i_sdk import AsyncMAK4IClient, BearerAuth

async with AsyncMAK4IClient("https://mak4i.example.com/mcp", auth=BearerAuth.from_env()) as c:
    current = await c.get_current("prj_123", artifact_type="caching_decision")
    existing = await c.find_existing("prj_123", artifact_type="caching_decision", subject_key="primary-cache")
    if existing is None:
        await c.create("prj_123", artifact_id="cache-choice", artifact_type="caching_decision",
                       title="Cache", content="Use Redis", subject_key="primary-cache")
```

A REST API and SDKs in other languages are approved future scope
([ROADMAP.md](ROADMAP.md#approved-future-protocol-scope)); the Python SDK does not imply them.

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
