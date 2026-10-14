# Changelog

All notable changes to the MAK4I protocol specification. The specification
version (SPEC.md) is independent of artifact versions (MAK-0001) and of any
implementation's release version.

## Unreleased

### Change feed and MCP resources (optional profile)

Requested in talvikai/mak4i-reference#20.

- **New MAK-0008 §14:** a durable, ordered change feed per project.
  - Events: `record.created`, `record.superseded`, `record.withdrawn`, `resolution.completed`, `project.archived`. They carry identifiers and the authenticated actor, never content.
  - Ordering: a `sequence` and a watermark, so readers never skip.
  - Crash reconciliation, and at least 7 days of retention.
- **New tool** `mak4i_changes` (cursor-based; `read`), new error code `cursor_expired`, and `change_sequence` in `mak4i_get_current`, so "read current, then follow changes" misses nothing.
- **MCP resources** for project current knowledge, record versions and conflicts, with URIs built from immutable IDs.
  - Subscriptions through `resources/subscribe` (MCP 2025-11-25) and `subscriptions/listen` (2026-07-28).
  - `notifications/resources/updated` carries only the URI; live authorization is re-checked at delivery; `list_changed` when the readable project set changes.
  - Notifications are hints without replay; the feed is the reliable mechanism; neither is the audit record.
- **New optional conformance profile** `server-change-feed` (F1–F14) and schema `change-event.schema.json`. No existing profile, tool or field changes behavior for servers that don't claim it.

Owner decisions of 2026-10-12. These are four architecture decisions and
the resolution of every open item in the protocol gap/decision register.
- **Not tagged.** The release number is assigned when a maintainer tags it
  ([GOVERNANCE](GOVERNANCE.md#versioning)).
- **Comment period.** It starts on publication for MAK-0004 Part A,
  MAK-0005 Part A, MAK-0006, MAK-0008 and MAK-0009; the start and end
  dates are recorded here at that time.

### Added
- **[MAK-0009](standards/MAK-0009.md) Knowledge Scopes, Resources and Rule
  Inheritance** (Draft, *architecture-defined*: no conformance criteria or
  binding yet):
  - **Profiles:** Project Record and Distributable Artifact
    (organization-scoped; all projects by default with optional
    `targets`; `active` / `deprecated` / `withdrawn`; latest version by
    default with optional pins; mandatory rules always at latest).
  - **Hierarchy:** organization → project → optional resource group →
    resource. Resources and groups are archive-only with unique active
    names; records can be moved as an audited metadata change.
  - **Rules:** `enforcement: default | mandatory`, `rule_key`,
    `applies_to`, explicit `overrides`; effective-rule computation with
    preserve-and-reactivate; same-scope conflicts generalized to every
    scope.
  - **Authorization:** organization owners for organization knowledge,
    the new project permission `govern` for enforcement and structure;
    project `read` covers inherited organization artifacts.
  - **Audit:** event names defined.
- **Schemas:**
  - New: `artifact` (MAK-0001), `resource`, `resource-group`, `rule`,
    `distributable-artifact`, `artifact-pin`, `effective-rule`.
  - Common definitions: `scopeRef`, `ruleKey`, `enforcement`,
    `packageVersion`, `httpsOrLoopbackUrl`,
    `protocolInfo`, resource and group ids.
  - Vendor extension fields `x_<vendor>_` on output objects.
  - 154 examples covering every tool's input and output; record,
    conflict and resolution states; real content hashes and conflict
    ids.
- **MAK-0006:**
  - §8.6 refused-write security events (required fields;
    deployment-retained);
  - `govern` permission (architecture-defined).
- **MAK-0008:**
  - §13 client requirements, the basis of the Python SDK contract;
  - `artifact_exists` error;
  - `error.correlation_id`;
  - unknown-code rule;
  - `mak4i_whoami.protocol`;
  - result rules (tag matching, search status, successor ids, opaque
    traces);
  - loopback `http` issuer/resource;
  - proxy routing note.
- **CONFORMANCE:**
  - conformance profiles (Server: Project Records, transport options,
    OAuth options, Client/SDK, Artifact);
  - 69 new criteria (P9–P16, C18–C27, I11–I23, M18–M39, K1–K12,
    A1–A4).
- **SPEC:** Knowledge Model, specification status markers, Extensibility.
- **ROADMAP:** approved future protocol scope (F-1 … F-18, MAK-0009
  binding) and entry criteria for the MAK-0002/0003 rewrite.
- **Validator:**
  - check *status*: architecture-defined content stays out of the
    implemented contract;
  - check *consistency*: tool and error tables vs schemas, per-tool
    example coverage, one schema version;
  - schema-based artifact validation with a file-name rule;
  - `scripts/requirements.txt`.

### Added — Drafts (In Progress)
- **[MAK-0002](standards/MAK-0002.md) Context Injection Specification** and
  **[MAK-0003](standards/MAK-0003.md) Memory Resolution Algorithm** (v0.2):
  - The pre-v0.2 working drafts, reconciled with protocol v0.2 and
    MAK-0009 before publishing.
  - Each separates a *Settled design* (only requirements inherited from
    merged standards and owner decisions, each cited) from *Open items*
    (M2-O1 … M2-O22, M3-O1 … M3-O22, cross-referenced) and non-normative
    design notes that keep the unresolved v0.1 alternatives.
  - Each has a reconciliation log.
  - MAK-0003's output is the "applicability result" (`applicability_id`).
- **[MAK-0007](standards/MAK-0007.md) Registry API Contract** (v0.1): initial
  draft covering registry scope, settled design inherited from
  MAK-0001/0006/0009, and open decisions M7-O1 … M7-O17.
- **None of the three is complete, accepted or implemented.**
  - They have no conformance criteria and no schemas yet.
  - The validator check *status* now also requires every Draft (In
    Progress) to declare "Conformance status: In progress" and to have no
    CONFORMANCE criteria.
  - GOVERNANCE defines the "Draft (In Progress)" marker.
  - ROADMAP lists what they need to leave In Progress.

### Changed
- **Governance:**
  - status ladder Reserved → Draft → Review → Accepted → Deprecated;
  - sequential numbering (0002/0003/0007 recorded as reserved);
  - Drafts may be implemented experimentally with a pinned revision;
  - one protocol SemVer release number;
  - revision-history and CHANGELOG discipline in the PR template.
- **Conformance claims** are per profile and protocol version; "MAK4I
  Certified" is removed until a published suite exists (future scope).
- **MAK-0004 / MAK-0005:**
  - Part B is a non-normative design appendix (future scope F-8 / F-9);
  - MAK-0004's design principle is aligned with A6.4 (existence and
    count disclosable).
- **MAK-0001 (v0.2):**
  - Distributable Artifact packaging metadata; `version` is a package
    version;
  - optional `content`; `org/name` ids; `token_estimate` = content size
    in tokens.
- **Check-before-create** is described as a supported discipline (client
  guidance, SDK helper), not a protocol guarantee; a normative rule is
  future scope.
- **The `context-package` schema** is retitled "Current knowledge result";
  the file name is unchanged.
- **Repository hygiene:**
  - neutral sample artifacts and examples (no personal email, company
    branding or product names);
  - sample "Skill" names → "Workflow"; versions bumped to 1.0.1;
  - the bundled document framework and its artifact removed;
  - business, positioning and savings documents moved to
    `docs/background/` (non-normative), with internal references removed;
  - MCP.md limited to the technical relationship.

### Breaking (Draft-stage; migration notes)
- **`mak4i_whoami` output** must include `protocol` (`version`,
  `profiles`) and the `scopes` key. *Migration:* servers add both.
- **Conflict candidates** must carry the `provenance` key (`null` for
  legacy). A `resolved` conflict must carry `resolution`. *Migration:*
  always emit the key.
- **Resolution records** must carry `idempotency_key` (or `null`), unique
  candidate ids, `parameters` matching the action, `completed_at` null
  exactly while pending, and a successor for every `superseded` effect.
  *Migration:* emit as specified.
- **Tool inputs:**
  - unknown arguments → `validation_error`;
  - differing identity claims → `identity_mismatch`;
  - empty `artifact_type`/tag filters and unknown `status` values are
    invalid.
  
  *Migration:* reject instead of ignoring.
- **Duplicate `artifact_id` on create** → `artifact_exists` (was
  implementation-defined). *Migration:* map the error.
- **Client ID Metadata Documents** must declare
  `token_endpoint_auth_method: "none"`.

### Compatibility
- **Existing records** remain valid. The new record fields (`resource_id`,
  `rule`) are optional and architecture-defined.
- **Reference implementation:** the Reference at `62fca93` doesn't yet
  meet the Breaking items above. Its alignment is tracked separately and
  follows this release (protocol first).

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

### Clarified during Reference implementation (2026-10-11)

- MAK-0004 §A8.2/§A8.3: resolutions **reserve** every candidate head
  before applying effects; writes to reserved heads are rejected; an
  abort can only occur before any semantic effect.
- MAK-0005 §A3.3/§A7 and MAK-0004 §A8.2: resolution ownership marker for
  crash-safe recovery; a half-applied supersede under a pending
  resolution is not a `zero_active` error.
- MAK-0008 §10.5/§10.6: list results are wrapped; normative discovery
  defaults (withdrawn/superseded never current, search defaults to
  active, history includes all versions) — taken from issue #4.
- MAK-0006 §2.1, MAK-0005 §A2: non-applicable optional fields may be
  absent or `null`.

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
