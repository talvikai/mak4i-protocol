# Changelog

All notable changes to the MAK4I protocol specification. The specification
version (SPEC.md) is independent of artifact versions (MAK-0001) and of any
implementation's release version.

## Unreleased

Nothing yet.

## v0.4 (Draft) — proposed in #18, not yet merged or tagged

P1: server-assigned record identifiers and search-before-create
(issue #15, talvikai/mak4i-reference#66). Owner decisions of 2026-11-05
(identifier policy), 2026-11-10 (O1–O6) and 2026-11-11 (S1–S8). Every
schema's `x-mak4i-schema-version` is `0.4.0`, and `protocolInfo.version`
examples report `0.4`. The background and decision record is
[docs/P1_ARTIFACT_ID_DRAFT.md](docs/P1_ARTIFACT_ID_DRAFT.md).

### Record identifiers (MAK-0005 §A8)
- The server assigns every persisted version an opaque `art_<uuid>`
  identifier: on create, on supersession, and for merge and
  separate-subjects versions. Identifiers carry no title, subject, date
  or version.
- A new lineage's `lineage_id` is its first `art_` identifier.
- A multi-step write fixes the successor identifier before its first
  durable step; retries and recovery reuse it.
- Servers resolve references by exact match only; they never strip or
  increment identifiers.
- `created_at` / `updated_at` are unchanged. No date field is added.

### Duplicate handling (MAK-0005 §A5.6–§A5.7, §A8.8; MAK-0004 §A3.6, §A8.5)
- An ordinary create on an occupied subject fails with the new code
  `subject_exists`. A caller with `read` gets the current identifiers in
  the new error `details`; a write-only caller learns only that the
  subject is occupied.
- `allow_competing: true` creates a competing record and forms a
  conflict, as every create did before. It requires `write` and `read`
  and grants no `resolve`.
- The occupancy check and the create are atomic: of concurrent ordinary
  creates on one subject, exactly one succeeds. A create racing with a
  resolution that assigns the same key is also a single claim (one wins).
  A create racing with a release of the key follows the order: release
  first, both succeed; create first, the create fails `subject_exists`
  and the release leaves the key free.
- An optional create `idempotency_key`, scoped to the principal and kept
  for 7 days, makes retries safe. A replay returns the original record,
  unmarked. The same key with different parameters fails with the new
  code `idempotency_key_reused`. Tags are compared as a set.

### Documentation aligned with enforcement
- MAK-0006 §8.6 lists `subject_exists` and `idempotency_key_reused`
  among refused-write causes, replacing the reserved `artifact_exists`.
- README, SPEC.md (reuse discipline) and ROADMAP F-13 say what the
  server now enforces: duplicate keyed subjects are refused; creates
  without a `subject_key` are not checked.
- The DEVELOPER_GUIDE SDK example still passes `artifact_id` to create;
  it changes with the Reference SDK work.

### Search lookup (MAK-0008 §10.5b)
- `mak4i_search` gains `text`, `subject_key`, `limit` and `detail`.
- A lookup (text or subject key) returns summaries, ranked with an exact
  subject match first and a stable tie-breaker, at most 20 by default.
  Conflict candidates carry `conflict_id`.

### Compatibility and upgrade notes
- **Breaking: `mak4i_create` no longer accepts `artifact_id`.** A v0.3
  client that sends one receives `validation_error` with reason
  `server_assigned_id`, and nothing is written. Affected:
  - CLIs and SDKs whose create command or method takes an identifier;
  - stored scripts and prompts that pass one;
  - clients that predicted successor names (for example `x-v3`). This
    was already non-conforming under MAK-0008 §10.5a.

  Clients that build arguments from the live MCP tool schema adapt
  without change.
- **Breaking: duplicate subjects are refused.** An ordinary create that
  formed a conflict in v0.3 fails with `subject_exists` in v0.4. To keep
  the old behavior, a client must request a competing record and hold
  `read`.
- **New error codes** `subject_exists` and `idempotency_key_reused`.
  Older clients handle them through `retryable` (MAK-0008 §9.5).
  `artifact_exists` is reserved and no longer produced.
- **Additive:** create `idempotency_key` and `allow_competing`; the
  search lookup inputs; `common.schema.json` `assignedArtifactId` and
  `idempotencyKey`; the `project-record.schema.json` summary; error
  `reason` `server_assigned_id` and `details`.
- **Unchanged:**
  - every stored identifier, lineage and history link; no migration;
  - legacy identifiers stay valid in every reference (`artifactId` is
    not narrowed);
  - continuing lineages mix legacy and `art_` identifiers;
  - existing open conflicts;
  - type/tag-only searches, which return exactly the v0.3 result.
- **Switch-over:** there is no per-request version negotiation, so the
  behavior changes when a server is upgraded. Operators publish these
  notes to client owners before upgrading.

### Conformance
- P1 amended. P16 replaced: create rejects `artifact_id`.
- New criteria:
  - P17–P22 identifiers and occupancy;
  - P23–P26 independent creates racing versus retries of one request;
  - C28 create vs. key assignment (one claim wins) and C29 create vs.
    release (outcome follows the order);
  - C30 resolution identifiers;
  - M40 search lookup;
  - K13 client handling of `subject_exists`.
- C3, C4, C12 and K10 adjusted. Profiles: Server: Project Records adds
  M40; Client/SDK becomes K1–K13.

### Clarifications before the tag (owner decisions of 2026-11-12)
Found while planning the Reference implementation (owner answers Q1–Q13
and D1–D7, recorded in the P1 Reference implementation plan). They land
in v0.4 itself because v0.4 is not tagged yet.
- **Subject keys are lowercased** (MAK-0005 §A5.2, MAK-0004 §A2, §A4.1).
  - Normalization is NFC, Unicode default lowercase, NFC, trim. This is
    lowercasing, not case folding.
  - Versions persisted from v0.4 store the normalized key. Earlier
    stored keys are never rewritten and are compared in normalized
    form, so case-only duplicates become one subject (a conflict, never
    merged automatically).
  - `conflict_id` uses the normalized key. A conflict on a key with
    uppercase letters gets a new identifier.
  - Length is counted in Unicode code points.
- **Interrupted supersession** (MAK-0005 §A4.5, §A5.6, §A7).
  - A multi-step supersession records an intent, the commit point,
    before marking the old head. After that point it is completed with
    the fixed successor identifier, never cancelled.
  - While pending, the lineage keeps its head, occupies its subject and
    is not `zero_active`. Other writes to that head fail `stale_head`.
  - An uncertain storage outcome is settled from the persisted operation
    identity, not from matching actor or content.
- **New retryable code `operation_pending`** (MAK-0008 §9), with reasons
  `reservation_pending`, `recovery_blocked` and `outcome_unverified`.
  It means "not settled yet", not "nothing written".
  - `internal_error` now covers only failures that committed nothing.
  - A committed create or supersession that cannot complete returns
    `operation_pending` (MAK-0005 §A8.4).
  - A resolution whose recovery is blocked stays pending and is shown to
    operators (MAK-0004 §A8.2).
  - Clients retry with the same `idempotency_key`, or re-read first
    (MAK-0008 §13.6).
- **Reserved keys** (MAK-0005 §A5.6, MAK-0004 §A8.5).
  - A create naming a key that a pending resolution is assigning never
    sees the planned identifier.
  - After a bounded wait the create gets `subject_exists`, proceeds, or
    gets `operation_pending` (`reservation_pending`).
  - "Persists nothing" means no version, head change or live
    reservation. An aborted resolution record stays as audit evidence.
- **Create retries** (MAK-0005 §A8.8).
  - A key is bound from the commit point, also while pending.
  - The retry comparison treats omitted, `null` and `""` rationale as
    equal, and omitted, `null` and `[]` tags as equal.
- **Competing records:** `allow_competing` needs `read` on a free subject
  too (MAK-0005 §A5.7).
- **Search lookup:** `subject_key` matching ignores case. Rank 1 compares
  `text` under the text rules. The snippet limit is 200 code points
  (MAK-0008 §10.5b).
- **Conformance:**
  - P22 and C28 amended.
  - New criteria P27–P31, C31, C32 and K14; Client/SDK becomes K1–K14.

## v0.3 (Draft) — prepared, not yet tagged

Everything merged since v0.2: the v2 alignment (#7, #9), the change feed
and MCP resources (#10), and client-scoped project access (#11). It is
tagged together with MAK4I Reference v2.1.0-rc.1, after the November 4
acceptance checks; the date is added then. Every schema's
`x-mak4i-schema-version` is `0.3.0`, and `protocolInfo.version` examples
report `0.3`.

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
- **Comment period.** It starts on publication for MAK-0004 Part A,
  MAK-0005 Part A, MAK-0006, MAK-0008 and MAK-0009; the start and end
  dates are recorded here at that time.

### Added
- **Client-scoped project access** (CLIENT-AUTH-001; optional profile
  `server-client-policies`; [MAK-0006 §5.7](standards/MAK-0006.md#5-permissions-and-grants)):
  - The same principal can have different effective permissions on a
    project depending on the verified client: a credential, or a
    pre-registered or metadata-document OAuth client. Client-reported
    names are never used.
  - Client policies are ceilings in the §5.3 intersection. Each project
    has a restriction mode (`off` by default; `on` = deny clients
    without a policy).
  - New `client-policy.schema.json` and common `clientIdentity`.
  - Optional error `reason` (`client_not_permitted`) and
    `mak4i_whoami.client`.
  - Refresh tokens are bound to their client (MAK-0008 §6.5).
  - Conformance criteria CP1–CP12.

### Fixed
- `common.schema.json` `protocolInfo.profiles` now lists
  `server-change-feed` (MAK-0008 §14). The profile was defined in #10, but a
  `mak4i_whoami` claiming it failed schema validation.
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
- **Reference implementation:** MAK4I Reference v2.0.0-rc.1 implements the
  Breaking items above. Reference v2.1.0-rc.1 implements v0.3, including
  the optional profiles `server-change-feed` and `server-client-policies`.

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
