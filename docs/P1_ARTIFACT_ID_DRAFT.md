# P1 draft: server-assigned record identifiers

Related: [Protocol #15](https://github.com/talvikai/mak4i-protocol/issues/15), [Reference #66](https://github.com/talvikai/mak4i-reference/issues/66).

This review draft captures the approved identity requirements for governed project records. It does not change the current protocol or the current MCP schema. The identity contract and P1 search, duplicate and retry behavior ship together.

Status: **decision record**. On 2026-11-11 the owner confirmed S8 and approved landing the text. The normative text now lives in MAK-0004, MAK-0005 and MAK-0008, CONFORMANCE.md and the schemas, as protocol v0.4 (see CHANGELOG.md). Where this document and the standards differ, the standards govern.
- §1 holds the settled identity rules. §3 has the specification text as proposed.
- §5 records the owner's direction of 2026-11-10 on the six choices O1–O6, with proposed text for each.
- §6 records the owner's answers to S1–S8 (2026-11-11).
- §7 compares Reference implementation options for O5.
- The §3.5 schema list and the examples in §4.2 describe the state before the v0.4 schema changes; the schema changes have since been applied.

## 1. Settled requirements

- The server assigns each newly persisted record version a unique, opaque `art_<uuid>` identifier, including the first version and every successor. An operation that does not persist a new version does not allocate a new record ID.
- Clients consume the returned `artifact_id`. They do not choose a new ID or derive a successor ID from a prior ID. IDs do not encode titles, subjects, dates or version numbers. Use the existing title, subject key, tags, version and timestamp fields for those meanings.
- A successor retains its lineage. Existing lineage IDs, record IDs and history links remain unchanged. A new successor to a legacy head can have a generated ID while its lineage and predecessor still carry legacy IDs.
- Existing IDs remain valid for authorized lookup, history and references under the existing operation rules. This does not permit writing against a stale head. No rename, backfill or rewrite is required.
- Preserve server-managed `created_at` and `updated_at` and their current semantics. No new date field. Business dates such as meeting and target dates remain content or metadata already supported by the record model.

## 2. What the current protocol already says (v0.3, main `177503a`)

| Rule today | Where | Effect on this work |
|---|---|---|
| `artifact_id` is unique within the project and never reused | MAK-0005 §A2 | Kept. Generated IDs also satisfy it. |
| `lineage_id` = `artifact_id` of the lineage's first version | MAK-0005 §A2, §A3.1; CONFORMANCE P1 | Kept. A new lineage's ID is its first `art_` ID (O2). |
| Server-assigned fields MUST NOT be accepted from writers | MAK-0005 §A2 | `artifact_id` joins that list. A legacy create that sends one is rejected (O1). |
| A successor's `artifact_id` is assigned by the server and opaque | MAK-0008 §10.5a | Already the contract for `mak4i_supersede`. The change extends it to create and resolutions, and adds the format. |
| `mak4i_create` *requires* a caller `artifact_id`; a clash fails with `artifact_exists` | `mcp-tools.schema.json`; MAK-0008 §9; CONFORMANCE P16 | Replaced (O1). |
| Creating a record on an occupied subject always succeeds and creates or extends a conflict; writes are never refused for that reason | MAK-0004 §A3.6, §A8.5 | Changed: an ordinary create is refused (O3), atomically (O5). An explicitly requested competing record keeps today's behavior. |
| A merge or separate-subjects resolution supersedes a head with a new version | MAK-0004 §A7.4, §A7.5 | These versions get generated IDs as well (§3.3). |
| A pending resolution is completed, not abandoned, on retry or recovery | MAK-0004 §A8.2 | Generated successor IDs must be fixed before the first durable step (§3.1, A8.4). |
| `idempotency_key` exists only for resolutions (8–200 characters) | MAK-0004 §A8.4; MAK-0008 §13.7 | Added to create (O4). |
| `mak4i_search` filters by type, tags and status, and returns full records | MAK-0008 §10.1, §10.5a, §10.6 | Extended (O6). |
| Every ID field in every schema is `common.schema.json#/$defs/artifactId` (any non-empty string) | `schemas/` | Must stay that way so legacy IDs keep validating (§3.5). |
| `write` does not imply `read`; an operation that returns record content also requires `read` | MAK-0006 §5.1 | Governs what a refused create may disclose (O3). |
| The existence and count of unreadable conflict candidates may be disclosed, but not their identity | MAK-0004 §A6.4, D-007 | Same rule applied to an occupied subject (O3). |

## 3. Proposed specification text: identifiers

Written as it would land in the standards. Section numbers are proposals.

### 3.1 MAK-0005: new §A8 "Record identifiers"

> **A8.1 Assignment.** The server MUST assign a new `artifact_id` to every record version it persists: the first version of a lineage (create), every successor (supersession, §A4), and every version a conflict resolution writes (MAK-0004 §A7.4–§A7.5). A client never chooses, proposes or derives the identifier of a version it is writing.
>
> **A8.2 Format.** A server-assigned identifier is `art_` followed by a UUID in its canonical lowercase hyphenated text form (RFC 9562), for example `art_3f2b9c4e-8d1a-4b7e-9c55-0e6a1f2d7b43`. The identifier is opaque. Its UUID version and bits carry no meaning, and clients MUST NOT parse them. It MUST NOT encode a title, subject key, tag, date, version, predecessor identifier or other record content. The meaning of a version is carried by `title`, `subject_key`, `tags`, `version`, `supersedes` and the timestamps, never by its identifier.
>
> **A8.3 Uniqueness.** An assigned identifier MUST be unique among *all* versions in the project, including legacy versions (A8.5) whose identifiers happen to have the same shape. It is never reused, including after a failed write. The server MUST write a new version only if its identifier is absent (create-if-absent), and on a collision MUST assign another identifier instead of failing the operation.
>
> **A8.4 One identifier per persisted version.** An operation that persists no version assigns no visible identifier. This covers a rejected, failed or aborted write; a `select_winner` resolution; a resolution reservation (MAK-0004 §A8.2 step 2); and a recognised create retry, which returns the identifier of the original version (§5, O4). If a write takes more than one durable step (§A4.5, MAK-0004 §A8.2), the successor identifier MUST be fixed *before* the first durable step that refers to it: the old head's `superseded_by`, or the pending resolution record's `effects[].successor_artifact_id`. A retry or recovery of that write MUST complete with that same identifier, never a newly assigned one, so that no lineage gains two successors.
>
> **A8.5 Legacy identifiers.** Versions persisted before this revision keep their identifiers exactly as stored, in any form the earlier revision allowed. Implementations MUST NOT rename, rewrite, backfill or re-derive them, or the `lineage_id`, `supersedes`, `superseded_by`, `merged_from` and resolution references that point to them. A lineage MAY mix legacy and server-assigned identifiers. Every operation that accepts a record reference MUST accept a legacy identifier wherever it accepted one before: lookup, history, `old_id`, resolution candidates and assignments, and change-feed fields. It MUST NOT require references to match A8.2.
>
> **A8.6 No interpretation of identifiers.** A server MUST resolve a reference only by exact identifier match. It MUST NOT strip, increment or otherwise transform an identifier to find a record, head or lineage. A superseded or withdrawn identifier, legacy or not, stays readable under the read rules, and a write naming it as `old_id` still fails with `artifact_not_active` (§A4.1). Readability never makes a version a writable head.
>
> **A8.7 Time and order.** `created_at` and `updated_at` keep the meaning of §A2 and §A3.3. This revision adds no date field. Order within a lineage is given by `version` and the `supersedes` chain. Order in time is given by the timestamps. Identifiers are not an ordering key. Where a rule sorts by `artifact_id` for determinism (for example conflict candidates, MAK-0004 §A5), the order stays deterministic but is not chronological.

Consequential edits in MAK-0005:

- **§A2 table, `artifact_id` row:** "Server-assigned (A8). Unique within the project; never reused; opaque."
- **§A2, after the table:** `artifact_id` is added to the server-assigned fields that "MUST NOT be accepted from writers" (O1).
- **§A2 `lineage_id` row and §A3.1:** unchanged wording: "`artifact_id` of the lineage's first version". For a new lineage that is its first `art_` identifier (O2). No separate lineage namespace.
- **§A4.3:** append "The successor's `artifact_id` is assigned per A8. It is never derived from `old_id`."
- **Revision history:** a row for the release summarising A8, A5.6 and A5.7 (§5).

### 3.2 MAK-0008 (MCP binding), identifier part

- **§10.5a, replace the successor bullet with:**
  > Every tool that persists a record version assigns its `artifact_id` on the server (MAK-0005 §A8). Clients read the identifier from the result: the record returned by `mak4i_create` and `mak4i_supersede`, and `effects[].successor_artifact_id` and `resulting_heads` in the resolution record returned by `mak4i_resolve_conflict`. Supplying both a different `subject_key` and `release_subject_key: true` fails with `subject_key_change`, and so does releasing on a lineage that has no key.
- **§10.1 table, `mak4i_create`:** "Create a record (new lineage); the server assigns its identifier."
- **§13.7 Writes, add:**
  > A client MUST NOT construct, guess or derive record identifiers. It MUST use the identifier returned by the server for any later reference, MUST NOT parse identifiers (MAK-0005 §A8.2), and MUST NOT order records by identifier.
- **§14 change feed:** no text change. `artifact_id`, `lineage_id` and `previous_artifact_id` carry whatever identifiers the versions have, legacy or generated.
- Create input, errors, retries and search: §5.

### 3.3 MAK-0004 (conflict resolution), identifier part

- **§A7.4 merge, add:** "The new version's `artifact_id` is assigned by the server (MAK-0005 §A8), and is reported as the `successor_artifact_id` of `into_artifact_id` and in `resulting_heads`."
- **§A7.5 separate_subjects, add:** the same for each candidate whose key changes.
- **§A7.3 select_winner:** no change, because it persists no version (MAK-0005 §A8.4).
- **§A8.2 step 1, add:** "The record created in state `pending` fixes the `successor_artifact_id` of every effect that will write a version. Steps 3 and 4, any retry and any recovery use those identifiers (MAK-0005 §A8.4)."
- §A3.6 and §A8.5: changed by O3 and O5 (§5).

### 3.4 CONFORMANCE.md (proposed criteria; added when the standards text lands)

| Criterion | From |
|---|---|
| Every create, supersession, merge and separate-subjects version gets a new `art_` identifier in the A8.2 form, distinct from every version in the project. | §1 |
| A successor of a legacy head gets a generated identifier, keeps `lineage_id`, and has `supersedes` equal to the legacy identifier unchanged. | §1 |
| History of a mixed lineage returns every version in `version` order with its stored identifier. No identifier is rewritten. | §1 |
| A superseded legacy or generated identifier used as `old_id` fails `artifact_not_active`. A transformed identifier (suffix stripped or incremented) is not resolved. | §1 |
| A crash or retry of a multi-step supersession or resolution completes with the successor identifier fixed before the first durable step. No lineage gains two successors. | §1 |
| Possessing an identifier confers no access. The existing `access_denied` / `not_found` rules apply unchanged. | §1 |
| P1: a new lineage's `lineage_id` equals its first `art_` identifier. | O2 |
| P16, replaced: a create that sends `artifact_id` fails `validation_error`, writes nothing, and reports the server-assigned reason. | O1 |
| An ordinary create on an occupied subject fails `subject_exists` and writes nothing. Current identifiers are returned only to a caller with `read`. | O3 |
| A competing create succeeds only when requested by a caller with `write` and `read`, and forms or extends a conflict. A write-only caller asking for one fails without learning the current identifiers. Contributing a competing record grants no `resolve`. | O3, S1 |
| The same principal, key and request returns the original record, unmarked. The same key with a different request fails without writing; tag order alone is not a difference. N concurrent identical requests create exactly one record. After the 7-day retention window the key is not matched and the create is checked as a new request. | O4, S2, S3, S5 |
| N concurrent ordinary creates on one free subject: exactly one succeeds and N−1 fail `subject_exists`. No competing record is persisted. Test on every store the implementation supports. | O5 |
| Search finds a record by exact `subject_key` and by title text without tag knowledge. It returns only current, authorized records as summaries, in the §5 order, with open-conflict candidates marked. A type/tag-only search returns exactly what it returns in v0.3. | O6, S6, S7 |

### 3.5 Schemas

No schema in `schemas/*.schema.json` changes in this PR. Proposed changes once the standards text lands:

| Schema change | From |
|---|---|
| Keep `common.schema.json#/$defs/artifactId` (any non-empty string) for every record field and every reference input. Narrowing it fails 44 existing example checks (tested on a scratch copy). | §1: **no change** |
| Add `$defs/assignedArtifactId` = `^art_[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$`. | A8.2 |
| `mak4i_create` and `mak4i_supersede` output: `artifact_id` uses `assignedArtifactId`. A create retry never returns a pre-upgrade record (S4), so create output is always a generated identifier. | A8, S4 |
| `mak4i_create.input`: remove `artifact_id` (closed inputs then reject it). | O1 |
| `mak4i_create.input`: add `idempotency_key` (string, 8–200 characters, same as resolutions). | O4 |
| `mak4i_create.input`: add the competing-record option, e.g. `allow_competing: boolean`, default `false` (name to confirm). | O3 |
| `mak4i_create.output`: **no change** for retries. A replay is not marked (S3), so the output stays exactly `project-record.schema.json`. | O4, S3 |
| `error.schema.json` and MAK-0008 §9: new codes `subject_exists` and `idempotency_key_reused`. The validator requires the error table and the enum to change together. `artifact_exists` stays in the enum, with the row marked "not produced by `mak4i_create` since this revision". | O1, O3, O4 |
| `error.schema.json`: an optional `details` object, so `subject_exists` can carry current identifiers for readers. Additive. | O3 |
| `mak4i_search`: inputs `text`, `subject_key`, `limit`, `detail` (`summary` / `full`). Output items `oneOf` a summary record (new `$defs`, with optional `conflict_id`) or a full record. The v0.3 output for type/tag-only searches stays valid unchanged (S6). | O6, S6, S7 |
| `x-mak4i-schema-version` and SPEC.md MAJOR.MINOR bump. | release step |

## 4. Acceptance examples

### 4.1 Decision table

In these examples `art_…` stands for a fresh server-assigned identifier. Dates and suffixes in legacy IDs are what earlier clients chose, and are kept unchanged.

| # | Case | Expected result |
|---|---|---|
| 1 | Create through the new contract. | Server returns a fresh `art_…` ID with `lineage_id` equal to it, `version = "1.0"`, `status = active`, and `created_at = updated_at` set by the server. |
| 2 | Supersede legacy head `release-plan-v2-v2-v2` (version 4.0, lineage `release-plan`). | Successor `art_A`, `version = "5.0"`, `lineage_id = "release-plan"`, `supersedes = "release-plan-v2-v2-v2"`. The old head becomes `superseded` with `superseded_by = "art_A"`. Its ID, content and `created_at` are unchanged. |
| 3 | Supersede the legacy dated head `pipeline-doe-20261030`. | Successor `art_B`. No identifier ending in `-20261031` (or any other derived value) is produced. Dates stay in content, title or tags as written, and the write time is in `created_at`. |
| 4 | Supersede `art_A` (from case 2) again. | Successor `art_C`, `version = "6.0"`, same lineage, `supersedes = "art_A"`. |
| 5 | `mak4i_history` of lineage `release-plan` after cases 2 and 4. | Returns, in `version` order, `release-plan`, `release-plan-v2`, `release-plan-v2-v2`, `release-plan-v2-v2-v2`, `art_A`, `art_C`, each exactly as stored. `mak4i_get_current` returns only `art_C`. |
| 6 | `mak4i_supersede` with `old_id` = `release-plan-v2-v2-v2` or `art_A` after case 4. | `artifact_not_active`. Nothing is written and no fork is created. |
| 7 | `mak4i_supersede` with `old_id = "release-plan-v7"` (guessed from the old naming scheme). | Treated as any unknown identifier (`not_found`, or `access_denied` without read access). The server never maps it to a head by transforming it. |
| 8 | Conflict on subject `primary-cache` with candidates `cache-red` (legacy) and `art_D` (generated); `merge` into `cache-red`. | New version `art_E` with `supersedes = "cache-red"`, `lineage_id = "cache-red"`, `merged_from = ["art_D", "cache-red"]` and `resolution_id` set. The resolution record lists `successor_artifact_id = "art_E"` and `resulting_heads` → `art_E`. `art_D` is `withdrawn`. Both original IDs are unchanged. |
| 9 | `separate_subjects` where legacy candidate `db-choice-20261012` gets a new key. | Its successor gets a fresh `art_…` ID with the same lineage. A candidate that keeps its key is `unchanged` and gets no new ID. |
| 10 | `select_winner`. | No new version and no new ID. Losers become `withdrawn` under their existing IDs. |
| 11 | A supersession or resolution crashes after the old head was marked superseded (or the pending record was written) but before the successor was stored. | Recovery or an identical retry writes the successor under the identifier already recorded. No second successor and no other new ID appear. |
| 12 | Writes that are refused (`stale_head`, `artifact_not_active`, `subject_key_change`, `subject_exists`, `validation_error`, `access_denied`). | No version is persisted and no identifier is visible. A later successful write never reuses an identifier that was ever assigned. |
| 13 | A legacy record created by an older client was named `art_9b1…` by hand. | It stays valid. The server never assigns that identifier to another version (A8.3). |
| 14 | Read or write outside project authority with a valid identifier. | Existing authorization applies. Holding an identifier does not grant access, and a denial does not reveal that it exists. |
| 15 | A legacy client sends `mak4i_create` with `artifact_id`. | `validation_error`, reason `server_assigned_id`, with a message saying to omit it and read `artifact_id` from the result. Nothing is written. Its legacy IDs still work for lookup and history. |
| 16 | Create on subject `(cache_decision, primary-cache)`, whose current head is `art_F`. Caller has `write` and `read`. | `subject_exists`, nothing written, `details.current_artifact_ids = ["art_F"]`. The caller supersedes `art_F` instead. |
| 17 | Same as case 16, but the caller has `write` only. | `subject_exists`, nothing written, no identifiers, titles or content. The subject's existence is disclosed, as in MAK-0004 D-007. |
| 18 | Same subject as case 16, created with `allow_competing: true` by a caller with `write` and `read`. | Succeeds and forms a conflict with `art_F` (today's §A3.6 behavior). The caller gains no `resolve`; choosing the winner stays with resolvers. |
| 18a | Same as case 18, but the caller has `write` only. | `access_denied`, nothing written, and no identifier, title or content of `art_F`. |
| 19 | Create on a subject that is already in an open conflict (two or more heads). | `subject_exists`. `details` lists only the readable candidates, plus `hidden_count`. |
| 20 | Create on a subject whose only lineage released its key (`released_subject_key` set), or whose lineage was withdrawn. | Succeeds. The subject is free. |
| 21 | The same create (same principal, `idempotency_key`, parameters) is sent twice because a response was lost. | The second call returns the original record, with the same `artifact_id` and nothing new written, even though the subject is now occupied by that record. The key is checked before the subject. |
| 21a | As case 21, but the original record has since been superseded. | Still returns the version the original create persisted, with its original `artifact_id`, under current authorization. Nothing is written, and the response carries no replay marker. |
| 21b | As case 21, but the retry arrives more than 7 days after the original create. | The key is no longer matched. The create is checked as a new request: on the now occupied subject it fails `subject_exists`, with the current identifiers only for a reader. |
| 21c | As case 21, with the same tags in a different order. | Same request: returns the original record. |
| 22 | The same principal reuses an `idempotency_key` with a different title, content or tag set. | `idempotency_key_reused`, nothing written. |
| 23 | A different principal uses the same `idempotency_key` string. | Treated as a different request. Keys are scoped to the principal. |
| 24 | 8 concurrent identical requests with one key. | Exactly one record. All 8 calls return it. |
| 25 | 8 concurrent *different* ordinary creates (different keys or none) on one free subject. | Exactly one succeeds. 7 fail `subject_exists`. No competing record is persisted, and no conflict appears. |
| 26 | A create races with a `separate_subjects` resolution that assigns the same free key. | Exactly one claim wins. Create first → the resolution fails `subject_collision`; resolution first → the create fails `subject_exists`. The loser writes nothing; one head. |
| 26b | A create races with a supersession that releases the occupied key. | Order decides. Release first → both succeed and the created version is the one head. Create first → the create fails `subject_exists` and writes nothing, the release succeeds, and the key is free. Never two heads. |
| 27 | Records without `subject_key`. | Never refused for occupancy. Retries are protected only by `idempotency_key`. |
| 28 | `mak4i_search` with `text: "Accel"` and no tags. | Returns current, authorized records whose title, subject key, tags or content match, as summaries ranked per §5 (O6). Unreadable projects and other organizations are never searched. |
| 29 | `mak4i_search` with `subject_key: "primary-cache"` while that subject is in an open conflict. | The exact normalized match, ranked first. Each readable candidate's summary carries the `conflict_id`, so a client does not take one candidate as settled. Hidden candidates are not listed. |
| 30 | `mak4i_search` with only `artifact_type` and `tags` (as v0.3 clients send it). | Exactly the v0.3 result: full records, the existing limit behavior, and no `conflict_id` field. |
| 31 | A create after the upgrade whose `idempotency_key` happens to match nothing, on a subject held by a pre-upgrade record. | No replay (no pre-upgrade keys exist). The ordinary subject check applies: `subject_exists`, with the legacy identifier for a reader. |

### 4.2 Example records added in this PR

These validate under the current v0.3 schemas, which shows that the identity rules need no narrowing of the shared ID format:

- [`mak4i_supersede.output.valid-generated-successor-of-legacy-head.json`](../schemas/examples/mcp-tools/mak4i_supersede.output.valid-generated-successor-of-legacy-head.json) (case 2)
- [`mak4i_history.output.valid-mixed-legacy-and-generated.json`](../schemas/examples/mcp-tools/mak4i_history.output.valid-mixed-legacy-and-generated.json) (cases 2, 4 and 5, shortened)
- [`valid-merge-generated-successor.json`](../schemas/examples/resolution-record/valid-merge-generated-successor.json) (case 8)

Examples for O1–O6 were added with the v0.4 schema changes (`mak4i_create`, `mak4i_search` and `error` examples).

## 5. Owner direction 2026-11-10 (O1–O6) and proposed text

| | Direction |
|---|---|
| **O1** Legacy create sends `artifact_id` | Reject it with a clear upgrade message under the new contract. Document what happens to existing clients before switching them over. Legacy IDs still work for lookups and history. |
| **O2** New lineage ID | The first record's `art_<uuid>` is the stable lineage ID. No `lin_` namespace. |
| **O3** Subject already exists | Reject by default. Return the current record ID only if the caller can read it. Allow a competing record only when it is explicitly requested and authorized. |
| **O4** Retry key | `idempotency_key` is optional on create. The same caller, key and request return the original result. Reusing the key with a different request returns an error. |
| **O5** Simultaneous creates | Enforce O3 atomically: two ordinary creates for the same subject yield one success and one conflict response, without persisting a competing record. Compare implementation options; the contract does not mandate a lock. |
| **O6** Search defaults | Exact `subject_key` lookup and text search. Default to current, authorized records with short summaries, rank exact subject matches first, use a stable tie-breaker, and keep full content available through retrieval. |

*Note: the O5 text received was cut off mid-sentence ("…without persisting a competing recode compare implementation options…"). It is read here as above. Please confirm.*

### 5.1 O1: MAK-0008

> **§10.2 addition.** `mak4i_create` has no `artifact_id` input. A request that supplies one MUST be rejected with `validation_error` and reason `server_assigned_id`, and nothing is written. The message SHOULD tell the client to omit the argument and read `artifact_id` from the result. Legacy identifiers remain valid in every read and reference input (MAK-0005 §A8.5).

- §9.2: add `server_assigned_id` as the second defined `reason` (on `validation_error`).
- §9 table: the `artifact_exists` row reads "Not produced by `mak4i_create` since this revision. The code stays reserved (§9.5)."
- Backward / Forward Compatibility: "A v0.3 client that sends `artifact_id` on create is rejected. Clients that read the live tool schema (MCP `tools/list`) adapt without change. Scripts, CLIs and SDKs that pass an ID must drop it."
- "Document before switching over": no per-request protocol negotiation exists, so the switch happens at the server upgrade. Before an installation is upgraded, the Reference release notes and upgrade guide list the affected clients and the change: the CLI create command, SDK calls, and stored scripts. Production switches only at an owner-approved upgrade.

### 5.2 O2: MAK-0005 §A3.1

No text change: "`lineage_id = artifact_id`". With A8 it becomes the first `art_` identifier.

### 5.3 O3: MAK-0005 new §A5.6 and MAK-0004 §A3.6 amendment

> **A5.6 Occupied subjects.** A subject `(artifact_type, normalized subject_key)` is *occupied* while at least one lineage has a current head carrying that key (MAK-0004 §A3.1), including the candidates of an open or resolving conflict. A lineage that released the key (A5.4), or whose head was withdrawn, does not occupy it. A create naming an occupied subject MUST fail with `subject_exists` and write nothing, unless the request asks for a competing record (A5.7). If the caller holds `read` on the project, the error's `details.current_artifact_ids` lists the current heads of the subject in `artifact_id` order, and `details.hidden_count` counts any heads it cannot read. A caller without `read` receives neither: the subject's occupancy is disclosed, but not its identity (MAK-0004 D-007, MAK-0006 §5.1). A create without a `subject_key` is never refused for occupancy.
>
> **A5.7 Competing records.** A create MAY ask for a competing record (`allow_competing: true`). Such a request requires `write` and `read` on the project. Then the create succeeds on an occupied subject and creates or extends a conflict exactly as MAK-0004 §A3.6 describes. A caller without `read` fails with `access_denied`, writes nothing, and receives no identifier, title or content of the current heads. Contributing a competing record confers no `resolve` permission: choosing among candidates remains a resolution (MAK-0004 §A7.1). On a free subject, `allow_competing` has no effect.

- MAK-0004 §A3.6, replace the last two sentences: "A create that names an occupied subject is refused (MAK-0005 §A5.6), unless it asks for a competing record (§A5.7). A competing record then adds a candidate, creating or extending the conflict. Supersessions are never refused merely because they keep a candidate in conflict."
- MAK-0008 §9: new row `subject_exists`: "A create named an occupied subject (MAK-0005 §A5.6); nothing was written. Supersede the current record, or request a competing record. Retry: No."
- MAK-0008 §13.9: no longer "guidance only" for subjects. A client SHOULD still search first (O6). On `subject_exists` it SHOULD supersede the returned head rather than ask for a competing record, unless the user intends a competing decision.

### 5.4 O4: MAK-0005 new §A8.8 and MAK-0008 §13.7

> **A8.8 Create retries.** A create MAY carry an `idempotency_key` (8–200 characters). Keys are scoped to (organization, project, authenticated principal). The first create with a key binds the key to the request parameters and the resulting record. A later create with the same key and identical parameters MUST return that record and write nothing, whatever has happened to the subject since. With different parameters it MUST fail with `idempotency_key_reused` and write nothing. Concurrent requests with one key MUST produce at most one record. The key is checked before subject occupancy (A5.6).
>
> A replay returns the version the original create persisted, with its original `artifact_id`, as currently stored and under the caller's current authorization. It persists no new version and assigns no identifier (A8.4). The response is not marked as a replay.
>
> A key is retained for 7 days from the original successful create. A replay does not extend that window. After it expires, a create with that key is evaluated as a new request, including the occupancy check of A5.6. Records created before this revision have no key, so a create is never answered as a replay with a pre-upgrade record.

- "Identical parameters" means the create input other than `idempotency_key`: type, title, content, rationale, tags compared as a set (order and duplicates ignored), the normalized subject key, and `allow_competing`. Text fields are compared exactly. Any other change, including a different tag set, is a different request.
- MAK-0008 §13.7: "A client SHOULD send an `idempotency_key` on `mak4i_create`, and MUST reuse the same key and parameters when retrying after an unknown outcome." This matches the existing resolution rule.
- MAK-0008 §9: new row `idempotency_key_reused`: "The key was already used by this principal for a different create; nothing was written. Retry: No."

### 5.5 O5: MAK-0004 §A8.5, replaced

> **A8.5 Simultaneous writes.** The occupancy check of MAK-0005 §A5.6 and the create MUST take effect as one atomic step with respect to every other write that can occupy or free the subject: creates, supersessions that release a key, and resolutions that assign keys (§A7.5) or withdraw heads. Of any number of concurrent ordinary creates on one free subject, exactly one succeeds and the others fail with `subject_exists`, persisting nothing. Competing creates (MAK-0005 §A5.7) are not serialized against each other, so all of them succeed and form a conflict. The mechanism is implementation-defined. Concurrent supersessions of one head follow MAK-0005 §A4.2.

- CONFORMANCE: a concurrency criterion with N parallel ordinary creates (case 25). An implementation states the stores and deployment shapes it claims it for, e.g. multi-instance.

### 5.6 O6: MAK-0008 §10.1, §10.5a, §10.6

> **`mak4i_search` lookup.** Optional inputs:
> - `text`: case-insensitive; a record matches when every whitespace-separated term occurs in its title, subject key, tags or content.
> - `subject_key`: exact match on the normalized key (MAK-0005 §A5.2).
> - `limit`: default 20, maximum 100.
> - `detail`: `summary` (default) or `full`.
>
> All filters combine with AND. The default `status = "active"` and the authorization rules are unchanged (§10.6). Only projects the caller can `read` are searched.
>
> **Lookup mode.** A search that gives `text` or `subject_key` (with or without type, tag or status filters) is a lookup. The ranking, summaries, `limit` default and conflict marking below apply to lookups. A search with neither keeps its v0.3 behavior: full records, the existing order and limit, and no new fields. `detail` and `limit`, when given explicitly, are honored in either mode.
>
> **Ranking**, in order:
> 1. exact `subject_key` match;
> 2. a `text` match in the title;
> 3. a match in the subject key or tags;
> 4. a match in the content only.
>
> Ties are broken by `updated_at` (newest first), then by `artifact_id` in ascending order.
>
> **A summary** carries `artifact_id`, `lineage_id`, `artifact_type`, `title`, `subject_key`, `tags`, `status`, `version`, `updated_at` and a `snippet` of at most 200 characters of the matching content. Clients retrieve full content with `mak4i_get_current` or `mak4i_history`, or with `detail: "full"`. Matching is deterministic text comparison only; no semantic matching.
>
> **Conflicts.** In a lookup, a record that is a candidate of an open or resolving conflict carries that conflict's `conflict_id`. A client MUST NOT treat such a record as the settled answer for its subject (MAK-0004 §A6.1); it reads the conflict with `mak4i_get_conflict`. Candidates the caller cannot read are not returned (MAK-0004 §A6.4). The search `read` requirement equals the one for `mak4i_get_conflict`, so every caller who sees a marked record may read its conflict.

- Type/tag-only searches are unchanged (S6), so the search change is additive for existing clients.

## 6. Narrower questions: owner answers 2026-11-11

| | Question | Owner answer | Written into |
|---|---|---|---|
| **S1** | Who may request a competing record? | `read` + `write` and an explicit request. `resolve` stays separate: contributing a competing record does not let the caller choose the winner. Without `read`, reject without exposing the existing record's identifier or content. | A5.7; cases 18, 18a |
| **S2** | Retention of create retry keys | 7 days from the original successful create. A retry after expiry is a new request and goes through the subject check. A replay does not extend the window. | A8.8; case 21b |
| **S3** | Mark a replay in the result? | No new field in P1. Return the original create result with its original identifier, under current authorization. A replay creates no revision. | A8.8; §3.5; case 21a |
| **S4** | Can a retry return a pre-upgrade record? | Not as a replay: no stored key matches, and there is no backfill. The ordinary subject check can still find a pre-upgrade record and return its identifier to a reader. | A8.8; §3.5; case 31 |
| **S5** | Does tag order matter? | No. A real change to the tags or any other field is a key-reuse error. | A8.8; cases 21c, 22 |
| **S6** | Which searches get summaries and the 20-result default? | Only searches with `text` or exact `subject_key`, also when combined with type or tag filters. Type/tag-only searches keep their response shape and limit behavior. | §5.6 "Lookup mode"; case 30 |
| **S7** | Mark open conflicts in search? | Yes, in the new summary response, when the caller may see the conflict. Do not disclose hidden records or change the legacy search response. | §5.6 "Conflicts"; case 29 |
| **S8** | O5 wording: confirm the reading of the truncated sentence (§5) | Confirmed as written in §5. | MAK-0004 §A8.5 |

Details filled in by Claude Code, for review:
- **S3:** a replay returns the original version as it is stored now, so `status` may read `superseded` when the record has moved on. The original response is not stored separately.
- **S6:** `limit` and `detail` given explicitly also apply to type/tag-only searches. That is additive, since no v0.3 client sends them.
- **S7:** the marker is the existing `conflict_id`. Search already requires `read`, the same as `mak4i_get_conflict`, so every caller who sees the marker may open the conflict.

## 7. O5: Reference implementation options (comparison, no code)

The Reference has two artifact stores, LocalJSON (one server per installation, but CLI commands run alongside it) and GCS (several Cloud Run instances). Every deployment also has the control-plane SQL database: SQLite locally, Postgres in production. It already holds resolution records and the change feed, with pending/verify reconciliation at start-up.

| Option | How | For | Against | Effort |
|---|---|---|---|---|
| **A. Subject claim in the artifact store** | One claim object per `(org, project, type, key)`, written with the store's existing create-if-absent (`put_new`: LocalJSON lock, GCS `if_generation_match=0`) and taken over with compare-and-set (`put_if_match`). The claim names its lineage. A claim is valid only while that lineage's current head still carries the key, so a release, a withdrawal or a crash before the record write leaves a stale claim that the next create takes over by CAS. Legacy subjects without a claim are checked by scanning current heads before the claim is written. | Same primitives and tests as records, so LocalJSON/GCS parity holds. No migration. No release bookkeeping, because staleness is checked against the records. | A second object type in the store, which queries must skip. Resolutions that assign keys must claim through the same path. | ~1.5 days incl. multi-process tests |
| **B. Unique row in the control-plane DB** | A `subject_claims` table with a unique `(org, project, type, key)` constraint. The claim is inserted in state pending, the record is written, then the claim is committed, with start-up reconciliation like the change feed. | The database enforces uniqueness. A pattern the Reference already uses. | Two systems must agree, so the crash window needs reconciliation. Schema migration on Postgres and SQLite. | ~2 days |
| **C. Process or file lock around check-and-create** | A `FileLock` or in-process mutex per project. | Smallest change. | Not valid for GCS with several instances. LocalJSON only. | ~0.5 day, LocalJSON only |

Recommendation: **A**. It is atomic on both stores through primitives they already rely on, and it needs no cross-system reconciliation. LocalJSON's cross-process compare-and-set is tested in `test_store_compare_and_set_admits_exactly_one_writer_across_processes`. GCS uses generation preconditions, which are tested today only against the fake client, so a test against a real bucket belongs in the P1 acceptance run. B is the fallback if a claim object in the store is unwanted. C does not meet O5 for GCS.

Revised effort for P1 with O1–O6 as directed: about 6.5–7.5 working days, including protocol text, schemas, vectors and Reference. O5 adds about 1.5 days to the Nov 5 estimate.

**Owner review 2026-11-11 (commit 6ca6b9b):** the real-GCS concurrency test is a **release gate** for the Reference implementation. It must show (a) independent creates for one subject persist exactly one record (P23) and (b) every valid retry of one request returns that same persisted record (P24). The 6.5–7.5 days above is an estimate; readiness is decided by the GCS result, not the estimate. The same review corrected the create-vs-release race rule (MAK-0004 §A8.5, C28/C29; cases 26 and 26b above).

## 8. Compatibility and rollout notes

- The supersede side needs no tool-schema change: §10.5a already makes successor IDs opaque. A client that *predicted* successor names (`x-v3`) was already non-conforming and now visibly breaks.
- Breaking changes for clients, all in one protocol release and listed in the upgrade notes:
  - create without `artifact_id` (O1);
  - occupied subjects are refused (O3/O5).
- Search changes are additive: v0.3 type/tag-only searches return what they return today (S6).
- Legacy data needs no migration. Mixed lineages are normal and permanent. Existing open conflicts are untouched and are resolved as today.
- Reference runtime changes are out of scope for this PR. Server-generated IDs ship in the Reference together with P1 search-before-create and duplicate handling (talvikai/mak4i-reference#66).

Routine field updates without a full supersede, general lineage withdrawal (#4) and cross-type linking are outside this slice.
