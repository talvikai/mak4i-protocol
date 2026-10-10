# MAK4I Conformance

**Status:** Draft  
**Version:** 0.2  
**Created:** August 2026  

---

## What is MAK4I Certified?

An implementation is **MAK4I Certified** when it fully conforms
to the MAK4I protocol specification and passes the
MAK4I Conformance Test Suite.

```
MAK4I Certified ✓
```

This badge signals that an artifact, SDK, registry, or client
correctly implements the MAK4I protocol.

Similar to:
- OpenAPI → Swagger Validator
- Kubernetes → CNCF Conformance Tests
- HTTP → W3C validation

---

## Certification Levels

| Level | What is certified | Requirements |
|-------|------------------|-------------|
| **Artifact** | A single MAK4I artifact | Passes MAK-0001 schema validation |
| **SDK** | A language SDK | Implements inject, publish, list, sync |
| **Registry** | A MAK4I registry | Implements Registry API (MAK-0007) |
| **Client** | A MAK4I client | Implements full injection flow (MAK-0002) |

---

## Conformance Test Suite

> Status: Planned. The reference implementation is being validated against
> the evolving specification; a published conformance suite follows as the
> specification stabilizes.

The MAK4I Conformance Test Suite will include:

### Artifact Tests
- [ ] Schema validation (MAK-0001)
- [ ] Required fields present
- [ ] Version format valid (semver)
- [ ] Type enum valid
- [ ] ID format valid

### Injection Tests
- [ ] Artifact loads correctly
- [ ] Dependencies resolved
- [ ] Context assembled correctly
- [ ] Injected into AI session successfully

### Registry Tests
- [ ] Artifact publish
- [ ] Artifact fetch by ID
- [ ] Artifact version resolution
- [ ] Access control enforcement

---

## Acceptance Criteria for Draft Standards

These criteria define what an implementation must demonstrate for the
draft standards below. Each item names the governing section. They are
written as observable behaviors so an implementation's own tests (or a
future shared suite) can map evidence to them one-to-one.

### MAK-0005 Part A: project records

- [ ] P1 Create starts a lineage at version 1.0 with `lineage_id = artifact_id` (§A3.1).
- [ ] P2 Supersede of a non-head fails `artifact_not_active`; nothing written (§A4.1).
- [ ] P3 Two concurrent supersessions of one head: exactly one succeeds, the other fails `stale_head`, no partial write (§A4.2).
- [ ] P4 Versions are immutable except lifecycle pointers (§A3.3).
- [ ] P5 Subject key normalized (NFC + trim), carried forward, change rejected `subject_key_change`, release recorded, no reclaim (§A5).
- [ ] P6 Legacy versions without subject fields or provenance remain readable and are never rewritten (§A5.5).
- [ ] P7 Integrity errors (`zero_active`, `multiple_active`, `dangling_pointer`) are reported, never guessed (§A7).
- [ ] P8 Records validate against `project-record.schema.json`.

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

---

## How to Get Certified

> Process to be defined as the conformance suite is published.

1. Implement the MAK4I protocol
2. Run the conformance test suite against your implementation
3. Submit results via GitHub PR
4. Receive MAK4I Certified badge

---

## Reference Implementation

Talvik maintains a reference implementation of the core protocol workflow,
currently in Developer Preview. It serves as the canonical conformance
baseline as the specification and conformance suite mature. Its source is
public at [talvikai/mak4i-reference](https://github.com/talvikai/mak4i-reference).

---

*© 2026 Talvik, Inc.*
