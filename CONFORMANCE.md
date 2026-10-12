# MAK4I Conformance

**Status:** Draft  
**Version:** 0.2  
**Created:** August 2026  
**Last Updated:** 2026-10-12

---

## How conformance is claimed

An implementation claims conformance **per profile and protocol
version**: "conformant to *Server: Project Records* and *Transport: HTTP
+ OAuth* at protocol 0.2". It backs the claim with evidence for every
criterion of those profiles, for example its own tests mapped one-to-one
to the criterion ids below. It reports the claimed profiles in
`mak4i_whoami.protocol.profiles`
([MAK-0008 §10.5](standards/MAK-0008.md#10-tool-catalog)).

A published, shared conformance suite and a certification process (and
any badge) are **approved future scope**
([ROADMAP.md](ROADMAP.md#approved-future-protocol-scope)). Until they exist, no implementation may be
described as "MAK4I Certified".

## Conformance profiles

| Profile (`profiles` value) | Applies to | Requires |
|---|---|---|
| **Server: Project Records** (`server-project-records`) | Servers storing governed records | All criteria of MAK-0005 Part A (P), MAK-0004 Part A (C), MAK-0006 (I), and MAK-0008 tool, error and catalog criteria (M15, M17, M19, M20, M34–M37) |
| **Transport: stdio** (`transport-stdio`) | Servers offering stdio | I17 plus the server profile |
| **Transport: HTTP + credential** (`transport-http-credential`) | Servers offering Streamable HTTP with principal credentials | M1 (with OAuth disabled: `realm` challenge), M7, M11, M14, M18, M21, M22, M38, M39 |
| **Transport: HTTP + OAuth** (`transport-http-oauth`) | Servers offering the OAuth service | All M criteria not listed elsewhere, including M16 (two real clients) |
| **OAuth option: CIMD** (`oauth-cimd`) / **DCR** (`oauth-dcr`) | Servers enabling these registration modes | M12, M32 for the enabled mode |
| **Client/SDK** (`client-sdk`) | Clients and SDKs | K1–K12 |
| **Artifact** (`artifact`) | MAK-0001 packaging metadata documents | A1–A4 |

Architecture-defined standards (below) belong to no profile.

---

## Acceptance criteria

Each item names the governing section. The criteria are written as
observable behaviors, so an implementation's tests (or a future shared
suite) can map evidence to them one-to-one.

### MAK-0005 Part A: project records

- [ ] P1 Create starts a lineage at version 1.0 with `lineage_id = artifact_id` (§A3.1).
- [ ] P2 Supersede of a non-head fails `artifact_not_active`; nothing written (§A4.1).
- [ ] P3 Two concurrent supersessions of one head: exactly one succeeds, the other fails `stale_head`, no partial write (§A4.2).
- [ ] P4 Versions are immutable except lifecycle pointers (§A3.3).
- [ ] P5 Subject key normalized (NFC + trim), carried forward, change rejected `subject_key_change`, release recorded, no reclaim (§A5).
- [ ] P6 Legacy versions without subject fields or provenance remain readable and are never rewritten (§A5.5).
- [ ] P7 Integrity errors (`zero_active`, `multiple_active`, `dangling_pointer`) are reported, never guessed (§A7).
- [ ] P8 Records validate against `project-record.schema.json`.
- [ ] P9 Server-assigned fields supplied by a writer are rejected or ignored, never stored; omitted and `null` optional fields are treated alike (§A2).
- [ ] P10 Every non-legacy version carries authenticated provenance (§A2, MAK-0006 §7).
- [ ] P11 A failed supersession leaves the lineage unchanged and is recorded in the security log (§A4.4, MAK-0006 §8.6).
- [ ] P12 Write ordering never leaves two active versions after a crash; a headless lineage is an integrity error (§A4.5).
- [ ] P13 Subject keys longer than 512 characters (after normalization) are rejected (§A5.2).
- [ ] P14 `withdrawn` is set only by conflict resolution and is terminal (§A6).
- [ ] P15 A head half-superseded by a pending resolution is not reported as `zero_active` (§A7).
- [ ] P16 A create with an existing `artifact_id` fails `artifact_exists`; nothing is written (§A2, MAK-0008 §9).


### MAK-0004 Part A: subject conflicts

- [ ] C1 Same-lineage update supersedes; no conflict (§A3.6).
- [ ] C2 Different subjects (type or key) coexist; shared tags never conflict (§A2, §A3.3).
- [ ] C3 Two lineages with one subject (e.g. RED vs YELLOW) form a conflict; neither is returned as current; no newest-wins (§A3.1, §A6.1).
- [ ] C4 A third contributor extends the same conflict (same `conflict_id`) (§A3.6, §A4.1).
- [ ] C5 Identical content still conflicts and reports `identical_content: true` (§A3.4).
- [ ] C6 Filters never hide one side of a conflict (§A6.2).
- [ ] C7 select_winner, merge and separate_subjects each produce the effects of §A7.3–§A7.5 and a complete record (§A7.6).
- [ ] C8 separate_subjects without an assignment for every candidate, or with colliding keys, is rejected (§A7.5).
- [ ] C9 A principal without `resolve` (or without `read`) is denied and nothing changes (§A7.1).
- [ ] C10 Stale candidate set → `conflict_changed`; second resolution of a generation → `conflict_not_open`; identical retry with the same idempotency key returns the same record (§A8).
- [ ] C11 Concurrent resolutions of one conflict: exactly one completes (§A8.4).
- [ ] C12 A new contribution after resolution creates a new conflict with a new `conflict_id` (§A7.7).
- [ ] C13 Releasing a candidate's key during an open conflict fails `subject_in_conflict` (§A3.7).
- [ ] C14 History preserves every original version and every resolution record (§A7.6).
- [ ] C15 A second client (different principal and/or transport) retrieves the same conflicted or resolved state (§A3.2).
- [ ] C16 A resolution reserves every candidate before any effect; a write to a reserved candidate fails `conflict_changed`; a resolution that can't reserve aborts with no effect and the conflict stays open with the same id (§A8.2, §A8.3).
- [ ] C17 Crashing after any single write of any resolution never shows the subject (or a separation target) as resolved while pending; recovery yields the uninterrupted result (§A8.2).
- [ ] C18 `conflict_id` equals `"cfl_" + sha256(org\nproject\ntype\nkey\ngeneration)[:32]`; two implementations derive the same id for the same subject and generation (§A4.1).
- [ ] C19 Readers treat a `resolving` conflict as conflicted; no candidate is returned as current while a resolution is pending (§A4.2).
- [ ] C20 Conflict details carry every required candidate field, including `provenance` (null only for legacy), ordered by `artifact_id` (§A5).
- [ ] C21 `mak4i_get_current` with a conflicted subject carries the explicit `instruction` not to choose a side (§A6.3).
- [ ] C22 Unreadable candidates are counted in `hidden_candidate_count` and never disclosed (§A6.4).
- [ ] C23 `write` is neither required nor sufficient to resolve; `resolve` + `read` is (§A7.1).
- [ ] C24 A merge result carries `merged_from` and `resolution_id`; merged originals are superseded by it (§A7.4).
- [ ] C25 Unknown conflict id → `not_found`; a conflict already resolved → `conflict_not_open` (§A8.1).
- [ ] C26 The same idempotency key with *different* parameters is rejected, never treated as a retry (§A8.4).
- [ ] C27 Resolution start, completion, abort and rejection are audited with actor and correlation id (§A9).


### MAK-0006: identity and access control

- [ ] I1 Agent principals require a valid, organization-unique, immutable `agent_id`; humans/services have none (§3).
- [ ] I2 Two agent principals with separate grants write records attributed to their own `principal_id` and `agent_id` (§7).
- [ ] I3 Identity fields in request arguments never change authorization or recorded authorship; a mismatching explicit claim fails `identity_mismatch` (§3.6, §3.7).
- [ ] I4 OAuth client names and MCP `clientInfo` are recorded only as unverified client metadata (§3.8, §7.3).
- [ ] I5 Effective permissions = live grant ∩ ceiling; scopes never widen (§5.3).
- [ ] I6 Revocation policy table holds per request: revoked credential, revoked authorization, deactivated principal, suspended org, removed grant, archived project (§6.3).
- [ ] I7 Denials do not reveal project existence (§5.5).
- [ ] I8 Owners cannot administer other organizations; members cannot administer anything (§8.2, §8.3).
- [ ] I9 Every administrative action yields an attributable event without secrets (§8.5).
- [ ] I10 Secrets are shown once and never appear in list/show output or logs (§6.1).
- [ ] I11 Organizations have a stable id and status; suspension blocks every principal and project without altering records (§1).
- [ ] I12 When both are emitted, `type` equals `principal_type` (§2.2).
- [ ] I13 The last active owner can't be deactivated; reactivation doesn't restore OAuth authorizations revoked by deactivation (§2.3).
- [ ] I14 Renaming a principal changes neither ids nor recorded provenance (§2.4, §7.4).
- [ ] I15 `bot_id`, if accepted, is an input-only alias of `agent_id` (§3.1).
- [ ] I16 A deactivated agent's `agent_id` is never reassigned; agents are never created implicitly (§3.4, §3.5).
- [ ] I17 A stdio session re-checks authentication before each operation; a revoked credential fails with `access_denied` (§6.4).
- [ ] I18 Operator actions record `auth_method = operator` and the principal acted for, or `null` for instance-level bootstrap (§7.6).
- [ ] I19 No unauthenticated remote administration endpoint exists, including for bootstrap (§8.1).
- [ ] I20 No operation deletes principals, projects, grants, credentials or records (§8.4).
- [ ] I21 Owners can retrieve their organization's administrative events durably (§8.5).
- [ ] I22 Every refused write by an authenticated principal (grant, scope, identity, validation, concurrency, lifecycle) emits a security event with the §8.6 fields and no secrets; a 403 scope refusal is attributed to the principal (§8.6).
- [ ] I23 If an external identity adapter is provided, it maps a stable external subject, verifies assertions, and never alters grants as a side effect (§9).


### MAK-0008: MCP binding and authorization

- [ ] M1 Unauthenticated MCP request → 401 with `resource_metadata` and `scope` challenge (§4.2).
- [ ] M2 Protected-resource and authorization-server metadata served unauthenticated, with URLs correct behind the configured path prefix (§3, §4).
- [ ] M3 Authorization code + PKCE S256 succeeds; wrong verifier, missing challenge, `plain` method fail (§5.1, §6.3).
- [ ] M4 Unregistered or mismatched redirect URI → error page, no redirect; loopback port rule honored (§5.2).
- [ ] M5 Code reuse fails and revokes the authorization (§6.2).
- [ ] M6 Wrong `resource` at authorize or token → `invalid_target`; token for another resource rejected at the MCP endpoint (§5.1, §6.6).
- [ ] M7 Expired or revoked access token → 401 `invalid_token`; no fallback identity (§2.2, §6.6).
- [ ] M8 Refresh rotates; replaying a rotated refresh token fails and revokes the authorization (§6.5).
- [ ] M9 Sign-in codes are single use, expire, are rate-limited and are never accepted as bearer tokens (§5.3, §11.1).
- [ ] M10 Consent page shows principal, client (unverified label), redirect host and scopes; CSRF enforced (§5.4, §5.5).
- [ ] M11 Principal credentials keep working; malformed / duplicate / query-string authorization rejected (§2).
- [ ] M12 Metadata advertises only enabled registration modes (§4.3, §8.1); CIMD fetch refuses non-public addresses (§8.3).
- [ ] M13 OAuth state survives a restart (§6.8).
- [ ] M14 No secret appears in logs or error messages (§11.2).
- [ ] M15 Tool errors carry `error.code` from §9; tool results validate against `mcp-tools.schema.json`.
- [ ] M16 Interoperability: at least two independent OAuth-capable MCP clients complete discovery, authorization, tool calls, refresh and revocation against a reachable HTTPS deployment (client versions recorded).
- [ ] M17 Discovery defaults: withdrawn/superseded versions are never current; `mak4i_search` defaults to active; history includes every version (§10.6).
- [ ] M18 Plain HTTP is accepted only on loopback; remote deployments require HTTPS (§1.2, §3).
- [ ] M19 An MCP session is bound to its authenticating principal; a request on it as another principal fails without effect (§1.3).
- [ ] M20 Health and readiness endpoints reveal no record, identity or configuration data (§1.4).
- [ ] M21 Foreign tokens (ID tokens, other issuers) are rejected and never forwarded (§2.4).
- [ ] M22 Advertised URLs come from configuration; forwarded headers are honored only from configured trusted proxies (§3.3, §3.4).
- [ ] M23 Sign-in codes are issued only by local tooling, carry ≥128 bits, and are stored hashed; no password or credential-for-token exchange exists (§5.3.1, §5.3.2).
- [ ] M24 The browser session lasts at most 15 minutes; an agent may be the resource owner through a sign-in code issued for it (§5.3.3, §5.3.4).
- [ ] M25 Remembered consent applies only to owner-pre-registered clients and the same principal and scopes (§5.4.2).
- [ ] M26 Pages set HttpOnly/SameSite/Secure cookies, `Cache-Control: no-store` and `frame-ancestors 'none'` (§5.5).
- [ ] M27 The authorization response carries `iss` (§5.6).
- [ ] M28 Codes and tokens carry ≥128 bits and are stored hashed; access-token lifetime defaults to 1 h (max 24 h) (§6.1, §6.4).
- [ ] M29 Authorizations end after the idle (7 d) or absolute (30 d) lifetime; refresh may narrow but never widen scope and re-checks the principal (§6.5).
- [ ] M30 Revocation accepts access and refresh tokens and answers 200 for unknown tokens (§6.7).
- [ ] M31 An authorization request without `scope` grants `mak4i:read mak4i:write`; credentials have no scope ceiling (§7.2, §7.4).
- [ ] M32 Pre-registered clients are bound to one organization; CIMD fetches honor timeout, size, no-redirect and cache limits; DCR, if enabled, registers public clients only (§8.2–§8.4).
- [ ] M33 Owners can list and disable clients and revoke one authorization, a principal's or a client's authorizations, each audited (§8.5).
- [ ] M34 Tool errors carry a text block with the message; denials never reveal existence; `correlation_id` links to the server event (§9.2–§9.4).
- [ ] M35 Unknown tool arguments → `validation_error`; differing identity claims → `identity_mismatch` (§10.2).
- [ ] M36 The implementation documents its tool ↔ CLI mapping; no implementation-specific tool uses the `mak4i_` prefix (§10.3, §10.4).
- [ ] M37 `mak4i_whoami` always carries `scopes` (null for credentials) and `protocol` (§10.5).
- [ ] M38 Token, revocation and registration endpoints are rate-limited (§11.1); signing keys, if any, are persisted outside configuration and rotatable (§11.3).
- [ ] M39 The configuration contract is validated at startup and the implementation refuses to start when it is invalid (§12).

### MAK-0008 §13: clients and SDKs (Client/SDK profile)

- [ ] K1 Connects over Streamable HTTP; refuses plain HTTP to a non-loopback host (§13.1).
- [ ] K2 Sends tokens only in the Authorization header, to the resource origin; never logs or prints them (§13.2).
- [ ] K3 Completes OAuth discovery from a 401 challenge, including a path-prefixed deployment (§13.3a).
- [ ] K4 Uses authorization code + PKCE S256 with `resource`; rejects a response whose `iss` or `state` mismatches (§13.3b–d).
- [ ] K5 A loopback redirect with any port works against a registered loopback URI (§13.3e).
- [ ] K6 Refresh rotation: stores the new refresh token; on `invalid_grant`, re-authorizes and never replays (§13.4).
- [ ] K7 Unwraps list results; ignores unknown output fields, tested with an added `x_test_` field (§13.5).
- [ ] K8 Maps every §9 code to a typed error; an unknown code falls back to `retryable` (§13.6).
- [ ] K9 No automatic retry of non-retryable errors; `stale_head`/`conflict_changed` helpers re-read first (§13.6).
- [ ] K10 Never sends identity arguments; resolution retries reuse the idempotency key (§13.7).
- [ ] K11 Reports the server's protocol version and warns on mismatch (§13.8).
- [ ] K12 Every tool call's arguments validate against `mcp-tools.schema.json`, and every valid output example in `schemas/examples/mcp-tools/` parses into the client's models (§10.1).

### MAK-0001: artifact packaging metadata (Artifact profile)

- [ ] A1 The document validates against `artifact.schema.json` (MAK-0001 Validation Rules 1–6).
- [ ] A2 `id` is `name` or `org/name` with lowercase-hyphenated segments.
- [ ] A3 `version` is a semantic version (a package version, never a project-record revision).
- [ ] A4 Dates are valid ISO 8601 dates; `token_estimate`, if present, is a positive integer estimating the content size in tokens.

---

## Architecture-defined standards (no criteria at this revision)

[MAK-0009](standards/MAK-0009.md) (distributable artifacts, resources, resource groups, rules
and inheritance) is **architecture-defined**:
- no acceptance criteria are defined for it here;
- an implementation MUST NOT claim support for it;
- no implementation is assessed against it at this revision.

The project-record fields it reserves (`resource_id`, `rule`), and the
`govern` permission, are not required by any profile. Criteria will be
added in the milestone that binds and implements MAK-0009
([MAK-0009 §8.4](standards/MAK-0009.md#8-conformance-status-at-this-revision)). The validator check *status*
(`scripts/validate_protocol.py`) enforces this boundary.
