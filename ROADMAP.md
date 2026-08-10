# MAK4I Roadmap

*Phase timing and scope. See [ARCHITECTURE.md](ARCHITECTURE.md) for what's
actually implemented today versus planned, and [MCP.md](MCP.md) for how
MCP fits into Phase 5.*

---

## Roadmap

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

## The Multi-Tool Workflow: Phase 2 vs. Phase 5

MAK4I's founding use case is a workflow gap its own builders live with
today: architecture and requirements decisions get made in one AI tool,
get manually re-explained to a second tool to implement, and get manually
re-explained again to document. Nothing persists between them
automatically. MAK4I is designed to close that gap — but not all at once,
and not on the same timeline for every integration path, since different
tools reach MAK4I through different mechanisms.

### Phase 2 (Oct-Nov 2026) — Direct REST API integration

```
AI tool (decisions made)
       │  written to MAK4I via REST API
       ▼
MAK4I  (artifact stored: architecture decision, requirement, spec)
       │  read via REST API, CLI, or SDK
       ▼
AI tool (implements from stored context)
```

Phase 2 targets AI tools and workflows that can call a REST API directly
— no MCP server required. The MAK4I endpoints this depends on (`POST
/api/v1/artifacts`, `GET /api/v1/artifacts/search`, `POST /api/v1/inject`)
are scoped for the Phase 2 reference implementation, alongside a CLI and
SDK for the same integration path.

A second use case in the same phase: MAK4I-stored decisions being read by
a documentation or presentation tool, closing the loop between "decision
made" and "decision documented" — available to any tool capable of REST
API, CLI, or SDK access.

### Phase 5 (Feb-Mar 2027) — MCP integration

```
AI tool
       │  via MCP server (mcp.talvik.ai)
       ▼
MAK4I
```

Phase 5 builds MAK4I as a native MCP server, extending access to any
MCP-compatible tool without requiring direct REST API integration. See
[MCP.md](MCP.md) for how MCP and MAK4I relate architecturally.

**Why the split matters:** Phase 2 targets what's achievable with existing
integration surfaces (REST API, CLI, SDK) and requires no new
infrastructure. Phase 5 extends reach to any tool that speaks MCP, without
the protocol's roadmap depending on the current capabilities of any single
vendor's product — those capabilities change faster than a roadmap should.
