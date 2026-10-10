# Changelog

All notable changes to the MAK4I protocol specification. The specification
version (SPEC.md) is independent of artifact versions (MAK-0001) and of any
implementation's release version.

## v0.2 (Draft) — 2026-10-10

Specification changes required by the MAK4I Reference implementation's
v2.0.0-rc.1 work (OAuth, agent identity, deterministic conflicts,
administration). All standards below are **Draft** and open for the
community comment period in [GOVERNANCE.md](GOVERNANCE.md); none is
Accepted.

### Added

- **[MAK-0006](standards/MAK-0006.md) Identity and Access Control** (v0.1):
  organizations, projects, principals (`human` / `service` / `agent`),
  `agent_id` (format, organization-scoped uniqueness, immutability,
  authenticated binding, spoofing behavior), permissions `read` / `write` /
  `resolve`, grants as the only authorization unit, effective permissions
  (grant ∩ transport ceiling), revocation policy, authenticated provenance,
  administration and audit events.
- **[MAK-0008](standards/MAK-0008.md) MCP Binding and Authorization** (v0.1):
  stdio and Streamable HTTP; bearer-credential and OAuth access-token
  precedence (no fallback); OAuth 2.1 profile pinned to MCP authorization
  2025-11-25 plus RFC 9207 (protected-resource and authorization-server
  metadata, PKCE S256, resource indicators, exact / loopback redirect
  matching, CLI-issued sign-in codes, consent, single-use codes, refresh
  rotation with replay revocation, revocation, pre-registration, Client ID
  Metadata Documents, optional DCR); scopes; tool catalog incl.
  `mak4i_list_conflicts`, `mak4i_get_conflict`, `mak4i_resolve_conflict`;
  error model; configuration contract.
- **[MAK-0005](standards/MAK-0005.md) Part A** (v0.2): governed project
  records — fields, lineage, immutability, stale-head supersession, subject
  keys (normalization, stability, release), lifecycle incl. resolution-only
  `withdrawn`, integrity errors.
- **[MAK-0004](standards/MAK-0004.md) Part A** (v0.2): deterministic subject
  conflicts — detection, conflict identity and state, details, retrieval
  without leaking or hiding candidates, select-winner / merge /
  separate-subjects resolution, resolution record, concurrency and
  idempotency.
- Canonical JSON Schemas (draft 2020-12) in [`schemas/`](schemas/) with valid
  and invalid examples; `scripts/validate_protocol.py` and a CI workflow that
  validate schemas, examples, MAK-0001 artifacts, Markdown links/anchors and
  the standards index.
- Acceptance criteria for the draft standards in [CONFORMANCE.md](CONFORMANCE.md).

### Changed

- [SPEC.md](SPEC.md) v0.1 → v0.2: terminology, access-control split
  (project access normative via MAK-0006; registry visibility planned), MCP
  binding, schemas, skills marked planned/deferred, standards table.
- MAK-0006 retitled from "Access Control Model" to "Identity and Access
  Control"; MAK-0008 added to the index.

### Fixed

- Standards index drift: STANDARDS.md, SPEC.md and VISION.md listed
  MAK-0004/0005 as Planned although the files existed.
- Six broken `MAK-000X-template.md` links in MAK-0004 / MAK-0005.
- CONTRIBUTING.md mis-grouped the standards; README quick example used a
  `type` value invalid under MAK-0001; DEVELOPER_GUIDE.md said the reference
  implementation source was not public.

### Compatibility

The specification is pre-1.0 (GOVERNANCE.md: v0.x may change). Additions are
backward compatible for existing deployments of bearer credentials and
records without subject keys or provenance (MAK-0006 §7.5, MAK-0005 §A5.5).
Behavior changes an implementation must make to conform: a conflict may no
longer be hidden by a tag filter (MAK-0004 §A6.2), and releasing a key of a
candidate in an open conflict is rejected (MAK-0004 §A3.7).

## v0.1 (Draft) — 2026-08-20

Initial public preview (tag `v0.1.0`).
