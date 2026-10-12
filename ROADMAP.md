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
| 1 — Protocol Spec | Active development | SPEC.md and the MAK standards: MAK-0001 (artifact schema), MAK-0004/0005 Part A (subject conflicts, project records), MAK-0006 (identity and access control) and MAK-0008 (MCP binding and OAuth) are Draft; MAK-0009 (knowledge scopes, resources, rule inheritance) is a Draft architecture standard with no conformance criteria yet; MAK-0002/0003/0007 planned; community RFC |
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

- **A Python SDK** over the MCP binding. Its client contract is
  [MAK-0008 §13](standards/MAK-0008.md#13-client-requirements) (Client/SDK profile); the SDK itself is a
  separate implementation project.
- **A documented REST API and SDKs in other languages** for tools that
  integrate directly rather than through MCP (approved future scope, below).
- **A hosted registry** for discovering and sharing artifacts across
  organizations.
- **Skills** as a first-class MAK4I object — planned and deferred; not
  specified and not supported by any implementation yet.
- **Native registry-level MCP**, so any MCP-compatible tool gains access
  to a hosted MAK4I registry without additional integration work — without
  the protocol's roadmap depending on the current capabilities of any
  single vendor's product.

---

## Approved future protocol scope

Approved by the specification owner on 2026-10-12. Each item below is
**future protocol scope**: approved direction, not yet specified, with no
conformance criteria. Approval here doesn't schedule product delivery;
product Phase 2 delivery timing is decided separately.

| ID | Item | Target |
|---|---|---|
| F-1 | MAK-0002 Context Injection: assembling context packages from current knowledge, effective rules and history | Protocol v0.3, together with F-2. Entry criteria below. |
| F-2 | MAK-0003 Memory/Applicability Resolution | With F-1 |
| F-3 | MAK-0007 Registry API: publish / install / sync, registry visibility, community artifacts | After F-1/F-2 |
| F-4 | Transport-independent REST API binding | Unscheduled. Not implied by the Python SDK. |
| F-5 | SDKs in other languages | After the Python SDK |
| F-6 | Skills as a first-class object | Unscheduled |
| F-7 | Standalone withdrawal, retirement and reinstatement ([issue #4](https://github.com/talvikai/mak4i-protocol/issues/4)) | Protocol v0.3 |
| F-8 | General conflict model (MAK-0004 Part B appendix) | Unscheduled |
| F-9 | General versioning model (MAK-0005 Part B appendix), including package-version semantics and dependencies | With F-3 |
| F-10 | Per-record access control, teams, multi-organization membership, SSO/IdP connectors, SCIM | Unscheduled; connectors and SCIM are commercial-product concerns |
| F-11 | Full MCP 2026-07-28 authorization migration | When target clients require it |
| F-12 | Published conformance suite and certification process | After protocol v1.0 |
| F-13 | Normative check-before-create | With F-3 |
| F-14 | Hosted client metadata document for the Python SDK | With a later SDK release |
| F-15 | Native registry-level MCP | With F-3 |
| F-16 | Multi-replica / high-availability semantics | Unscheduled; the protocol is unaffected |
| F-17 | Encryption of sensitive artifact content | Unscheduled |
| F-18 | Unifying the Project Record and Distributable Artifact shapes | With F-3 |
| — | MAK-0009 interface binding, error codes and conformance criteria | The milestone that implements MAK-0009 ([MAK-0009 §8.4](standards/MAK-0009.md#8-conformance-status-at-this-revision)) |

### Entry criteria for MAK-0002 and MAK-0003 (F-1, F-2)

The existing drafts (an unmerged branch and a local draft) predate
protocol v0.2. Before either can merge as a Draft, it must:

1. Preserve conflicts: assemble open conflicts and integrity errors as
   such, never pre-resolved (MAK-0004 Part A).
2. Align existence disclosure with MAK-0004 §A6.4: `hidden_candidate_count`
   is disclosed.
3. Use authenticated provenance (MAK-0006 §7), not free-text `author`.
4. Know the lifecycle `active` / `superseded` / `withdrawn` (MAK-0005 §A6)
   and the discovery defaults (MAK-0008 §10.6).
5. Use the term "context package" only for its own structure. The
   `get_current` result is the "current knowledge result".
6. Avoid reusing `resolution_id` (it means a conflict resolution).
7. Cite MAK-0006 as the authorization model, with single-project scope
   unless MAK-0006 changes.
8. Break the mutual dependency between the two drafts: decide each draft's
   open decisions jointly, or settle one first.
9. Fix stale titles, section ranges and D-number references.
10. Ship JSON Schemas and valid/invalid examples.
11. Remove "injection" as a certifiable client flow (delivery to an AI
    session stays out of scope).
12. Carry MAK-0009 knowledge:
    - inherited organization artifacts with source identity and version;
    - **effective rules as a required context category, with their
      explanation** (originating scope, enforcement, blocked and
      conflicted states).
13. Pass the validator and cross-document checks, and update STANDARDS,
    SPEC, CONFORMANCE and CHANGELOG together.

