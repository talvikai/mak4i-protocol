# MAK4I Roadmap

*Phase scope and status. See [ARCHITECTURE.md](ARCHITECTURE.md) for what's
actually implemented today versus planned, and [MCP.md](MCP.md) for how
MCP relates to MAK4I.*

---

## Where MAK4I is

MAK4I is in **Developer Preview**. Phase 1 (the specification) is in active
development, and Phases 2 and 5 have initial working implementations in the
reference MVP. The phases are no longer strictly sequential — nothing below
is marked done until it actually works.

| Phase | Status | Scope |
|-------|--------|-------|
| 0 — Foundation | Complete | Public repo, protocol design, problem statement, vision |
| 1 — Protocol Spec | Active development | SPEC.md and the MAK standards: MAK-0001 (artifact schema), MAK-0004/0005 Part A (subject conflicts, project records), MAK-0006 (identity and access control) and MAK-0008 (MCP binding and OAuth) are Draft; MAK-0002/0003/0007 planned; community RFC |
| 2 — Reference Implementation | Initial MVP complete | Working reference implementation of the core workflow — create, retrieve, search, supersede, version history, provenance — with an operator CLI and MCP access. Hardening and expansion are ongoing. |
| 3 — Reusable Artifacts | Planned | Community artifacts across artifact types; reuse-workflow validation with developers and early design partners |
| 4 — Hosted Registry | Planned | Public registry for discovering, versioning and sharing artifacts, with governance and access controls |
| 5 — MCP Integration | Initial integration working | MAK4I is reachable through MCP in the reference implementation today. Native registry-level MCP and broader interoperability remain ahead. |
| 6 — Funding | Planned | Pre-seed fundraising, informed by real usage data |

---

## The Multi-Tool Workflow

MAK4I's founding use case is a workflow gap its own builders live with:
architecture and requirements decisions get made in one AI tool, get
manually re-explained to a second tool to implement, and get manually
re-explained again to document. Nothing persists between them
automatically.

### Working today — via MCP

```
AI client A (decision made)
       │  recorded through an MCP tool call
       ▼
MAK4I reference implementation
   (artifact stored, with lineage, provenance and an audit event)
       │  retrieved through an MCP tool call — conflict/integrity checked
       ▼
AI client B (implements from the current decision, no re-explaining)
```

The reference implementation closes this gap today through MCP: a decision
recorded through one MCP-connected AI client is discoverable by another,
with conflict and integrity checks, version history and provenance — no
REST integration required. It has been exercised end to end this way
against several independent AI clients it was tested with.

### Still ahead

- **A documented REST API and language SDKs** for tools that integrate
  directly rather than through MCP (e.g. `POST /artifacts`,
  `GET /artifacts/search`, `POST /inject` or equivalent), so a
  documentation or presentation tool can read MAK4I-stored decisions and
  close the loop between "decision made" and "decision documented".
- **A hosted registry** for discovering and sharing artifacts across
  organizations.
- **Skills** as a first-class MAK4I object — planned and deferred; not
  specified and not supported by any implementation yet.
- **Native registry-level MCP**, so any MCP-compatible tool gains access
  to a hosted MAK4I registry without additional integration work — without
  the protocol's roadmap depending on the current capabilities of any
  single vendor's product.
