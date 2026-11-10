# P1 draft: server-assigned record identifiers

Related: [Protocol #15](https://github.com/talvikai/mak4i-protocol/issues/15), [Reference #66](https://github.com/talvikai/mak4i-reference/issues/66).

This review draft captures the approved identity requirements for governed project records. It does not change the current protocol or the current MCP schema. The identity contract and P1 search, duplicate and retry behavior ship together.

Status: **review draft**. The settled identity rules (§1) and their proposed specification text (§3) are ready for review. The choices listed in §5 are open and are not decided here. Wherever the proposed text depends on one, it is marked **[OPEN Ox]**. Nothing in `standards/` or `schemas/*.schema.json` changes in this PR. The added example records (§4.2) validate against the current v0.3 schemas.

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
| `lineage_id` = `artifact_id` of the lineage's first version | MAK-0005 §A2, §A3.1; CONFORMANCE P1 | Kept for existing lineages. For new lineages the rule depends on **[OPEN O2]**. |
| Server-assigned fields MUST NOT be accepted from writers | MAK-0005 §A2 | `artifact_id` joins that list. How a legacy create that sends one is treated is **[OPEN O1]**. |
| A successor's `artifact_id` is assigned by the server and opaque | MAK-0008 §10.5a | Already the contract for `mak4i_supersede`. The change extends it to create and to resolutions, and adds the format. |
| `mak4i_create` *requires* a caller `artifact_id`; a clash fails with `artifact_exists` | `mcp-tools.schema.json`; MAK-0008 §9; CONFORMANCE P16 | This is the contract change. Its shape depends on **[OPEN O1]**. |
| A merge or separate-subjects resolution supersedes a head with a new version | MAK-0004 §A7.4, §A7.5 | These versions get generated IDs as well (§3.3). |
| A pending resolution is completed, not abandoned, on retry or recovery | MAK-0004 §A8.2 | Generated successor IDs must be fixed before the first durable step (§3.1, A8.4). |
| Concurrent creations claiming one subject all succeed and form a conflict | MAK-0004 §A8.5, §A3.6 | Unchanged by this slice. Changing it is **[OPEN O3/O5]**. |
| Every ID field in every schema is `common.schema.json#/$defs/artifactId` (any non-empty string) | `schemas/` | Must stay that way so legacy IDs keep validating (§3.5). |

## 3. Proposed specification text

The text below is written as it would land in the standards. Section numbers are proposals.

### 3.1 MAK-0005: new §A8 "Record identifiers"

> **A8.1 Assignment.** The server MUST assign a new `artifact_id` to every record version it persists: the first version of a lineage (create), every successor (supersession, §A4), and every version a conflict resolution writes (MAK-0004 §A7.4–§A7.5). A client never chooses, proposes or derives the identifier of a version it is writing.
>
> **A8.2 Format.** A server-assigned identifier is `art_` followed by a UUID in its canonical lowercase hyphenated text form (RFC 9562), for example `art_3f2b9c4e-8d1a-4b7e-9c55-0e6a1f2d7b43`. The identifier is opaque. Its UUID version and bits carry no meaning, and clients MUST NOT parse them. It MUST NOT encode a title, subject key, tag, date, version, predecessor identifier or other record content. The meaning of a version is carried by `title`, `subject_key`, `tags`, `version`, `supersedes` and the timestamps, never by its identifier.
>
> **A8.3 Uniqueness.** An assigned identifier MUST be unique among *all* versions in the project, including legacy versions (A8.5) whose identifiers happen to have the same shape. It is never reused, including after a failed write. The server MUST write a new version only if its identifier is absent (create-if-absent), and on a collision MUST assign another identifier instead of failing the operation.
>
> **A8.4 One identifier per persisted version.** An operation that persists no version assigns no visible identifier. This covers a rejected, failed or aborted write; a `select_winner` resolution; a resolution reservation (MAK-0004 §A8.2 step 2); and **[OPEN O4]** a recognised retry. If a write takes more than one durable step (§A4.5, MAK-0004 §A8.2), the successor identifier MUST be fixed *before* the first durable step that refers to it: the old head's `superseded_by`, or the pending resolution record's `effects[].successor_artifact_id`. A retry or recovery of that write MUST complete with that same identifier, never a newly assigned one, so that no lineage gains two successors.
>
> **A8.5 Legacy identifiers.** Versions persisted before this revision keep their identifiers exactly as stored, in any form the earlier revision allowed. Implementations MUST NOT rename, rewrite, backfill or re-derive them, or the `lineage_id`, `supersedes`, `superseded_by`, `merged_from` and resolution references that point to them. A lineage MAY mix legacy and server-assigned identifiers. Every operation that accepts a record reference MUST accept a legacy identifier wherever it accepted one before: lookup, history, `old_id`, resolution candidates and assignments, and change-feed fields. It MUST NOT require references to match A8.2.
>
> **A8.6 No interpretation of identifiers.** A server MUST resolve a reference only by exact identifier match. It MUST NOT strip, increment or otherwise transform an identifier to find a record, head or lineage. A superseded or withdrawn identifier, legacy or not, stays readable under the read rules, and a write naming it as `old_id` still fails with `artifact_not_active` (§A4.1). Readability never makes a version a writable head.
>
> **A8.7 Time and order.** `created_at` and `updated_at` keep the meaning of §A2 and §A3.3. This revision adds no date field. Order within a lineage is given by `version` and the `supersedes` chain. Order in time is given by the timestamps. Identifiers are not an ordering key. Where a rule sorts by `artifact_id` for determinism (for example conflict candidates, MAK-0004 §A5), the order stays deterministic but is not chronological.

Consequential edits in MAK-0005:

- **§A2 table, `artifact_id` row:** "Server-assigned (A8). Unique within the project; never reused; opaque."
- **§A2, after the table:** `artifact_id` is added to the server-assigned fields that "MUST NOT be accepted from writers". Treatment of an existing client that still sends it is **[OPEN O1]**.
- **§A2, `lineage_id` row, and §A3.1:** "`lineage_id` = `artifact_id` of the lineage's first version" stays true for every existing lineage. For lineages created under this revision it is **[OPEN O2]**: either the same rule (the first version's `art_` ID) or a separately assigned lineage identifier. Either way, A8.5 applies to existing lineages.
- **§A4.3:** append "The successor's `artifact_id` is assigned per A8. It is never derived from `old_id`."
- **Revision history:** a 0.3 row (or 0.4, matching the release) summarising A8.

### 3.2 MAK-0008 (MCP binding)

- **§10.5a, replace the successor bullet with:**
  > Every tool that persists a record version assigns its `artifact_id` on the server (MAK-0005 §A8). Clients read the identifier from the result: the record returned by `mak4i_create` and `mak4i_supersede`, and `effects[].successor_artifact_id` and `resulting_heads` in the resolution record returned by `mak4i_resolve_conflict`. Supplying both a different `subject_key` and `release_subject_key: true` fails with `subject_key_change`, and so does releasing on a lineage that has no key.
- **§10.1 table, `mak4i_create`:** "Create a record (new lineage); the server assigns its identifier."
- **`mak4i_create` input:** the caller `artifact_id` is no longer the identity of the new record. **[OPEN O1]** decides whether the property is removed (closed inputs, §10.2, then reject it with `validation_error`) or kept for a transition. During a transition it is accepted but never used as the new identifier, and the result reports that.
- **§9 error table, `artifact_exists`:** it cannot occur on the new create path. Whether it is kept for a transition or marked as no longer produced is **[OPEN O1]**. The code stays reserved either way (§9.5).
- **§13.7 Writes, add:**
  > A client MUST NOT construct, guess or derive record identifiers. It MUST use the identifier returned by the server for any later reference, MUST NOT parse identifiers (MAK-0005 §A8.2), and MUST NOT order records by identifier.

  How a client retries a create without creating a second record depends on **[OPEN O4]**.
- **§13.9 Check before create:** rewritten together with the search and duplicate decisions **[OPEN O3, O6]**. This slice only removes any wording that suggests a client-chosen ID prevents duplicates.
- **§14 change feed:** no text change. `artifact_id`, `lineage_id` and `previous_artifact_id` carry whatever identifiers the versions have, legacy or generated.

### 3.3 MAK-0004 (conflict resolution)

- **§A7.4 merge, add:** "The new version's `artifact_id` is assigned by the server (MAK-0005 §A8), and is reported as the `successor_artifact_id` of `into_artifact_id` and in `resulting_heads`."
- **§A7.5 separate_subjects, add:** the same for each candidate whose key changes.
- **§A7.3 select_winner:** no change, because it persists no version (MAK-0005 §A8.4).
- **§A8.2 step 1, add:** "The record created in state `pending` fixes the `successor_artifact_id` of every effect that will write a version. Steps 3 and 4, any retry and any recovery use those identifiers (MAK-0005 §A8.4)."
- **§A8.5:** unchanged in this slice. See O3 and O5.

### 3.4 CONFORMANCE.md (proposed criteria; added when the standards text lands)

| Criterion | Depends on |
|---|---|
| Every create, supersession, merge and separate-subjects version gets a new `art_` identifier in the A8.2 form, distinct from every version in the project. | settled |
| A successor of a legacy head gets a generated identifier, keeps `lineage_id`, and has `supersedes` equal to the legacy identifier unchanged. | settled |
| History of a mixed lineage returns every version in `version` order with its stored identifier. No identifier is rewritten. | settled |
| A superseded legacy or generated identifier used as `old_id` fails `artifact_not_active`. A transformed identifier (suffix stripped or incremented) is not resolved. | settled |
| A crash or retry of a multi-step supersession or resolution completes with the successor identifier fixed before the first durable step. No lineage gains two successors. | settled |
| Possessing an identifier confers no access. The existing `access_denied` / `not_found` rules apply unchanged. | settled |
| P1 "lineage_id = artifact_id" | **O2** |
| P16 "create with an existing `artifact_id` fails `artifact_exists`" (replaced or removed) | **O1** |
| Create retry, duplicate-subject and concurrency criteria | **O3, O4, O5** |

### 3.5 Schemas

No schema in `schemas/*.schema.json` changes in this PR. Proposed changes and their dependencies:

| Schema change | Status |
|---|---|
| Keep `common.schema.json#/$defs/artifactId` (any non-empty string) for every record field and every reference input (`old_id`, candidates, `lineage_id`, history). Narrowing it would reject legacy IDs. | settled: **no change** |
| Add `$defs/assignedArtifactId` (`^art_[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$`), for use only where a value is always newly assigned. | proposed, independent of the open choices; spelling to confirm in review |
| Use `assignedArtifactId` for `artifact_id` in the `mak4i_create` and `mak4i_supersede` outputs. Legacy reads keep `artifactId`. | proposed. For `mak4i_create` it also depends on **O1** (a transition that could return a caller-named record) and **O4** (a retry returning a record created before the release). |
| `mak4i_create.input`: drop `artifact_id` from `required` and remove it, or keep it as optional and deprecated. | **O1** |
| `mak4i_create.input`: retry key property (name, length and pattern, for example by analogy to the resolution `idempotency_key` of 8–200 characters). | **O4** |
| `mak4i_create.input`: an explicit way to request an intentional competing record, and the default when the subject is occupied. | **O3** |
| `mak4i_create.output`: an indicator of whether the record was newly created or returned by a recognised retry, and any transition notice. Today the output is exactly `project-record.schema.json`, so either needs a wrapper or a new top-level field. | **O1, O4** |
| `error.schema.json` and MAK-0008 §9: new codes, for example an occupied subject or a reused retry key with different parameters. The validator requires the error table and the enum to change together. | **O3, O4** |
| `lineage_id` for new lineages: no format change if O2 keeps "first version's ID". A separate identifier would still validate as `artifactId`, but A2, A3.1 and CONFORMANCE P1 change. | **O2** |
| `mak4i_search` inputs and outputs (text, exact subject, limit, compact results, ranking). | **O6** |
| `x-mak4i-schema-version` and SPEC.md MAJOR.MINOR bump. | release step |

## 4. Acceptance examples

### 4.1 Decision table

In these examples `art_…` stands for a fresh server-assigned identifier. Dates and suffixes in legacy IDs are what earlier clients chose, and are kept unchanged.

| # | Case | Expected result |
|---|---|---|
| 1 | Create through the new contract. | Server returns a fresh `art_…` ID, `version = "1.0"`, `status = active`, and `created_at = updated_at` set by the server. `lineage_id` follows **O2**. |
| 2 | Supersede legacy head `release-plan-v2-v2-v2` (version 4.0, lineage `release-plan`). | Successor `art_A`, `version = "5.0"`, `lineage_id = "release-plan"`, `supersedes = "release-plan-v2-v2-v2"`. The old head becomes `superseded` with `superseded_by = "art_A"`. Its ID, content and `created_at` are unchanged. |
| 3 | Supersede the legacy dated head `pipeline-doe-20261030`. | Successor `art_B`. No identifier ending in `-20261031` (or any other derived value) is produced. The record's dates stay in content, title or tags as written, and the write time is in `created_at`. |
| 4 | Supersede `art_A` (from case 2) again. | Successor `art_C`, `version = "6.0"`, same lineage, `supersedes = "art_A"`. |
| 5 | `mak4i_history` of lineage `release-plan` after cases 2 and 4. | Returns, in `version` order, `release-plan`, `release-plan-v2`, `release-plan-v2-v2`, `release-plan-v2-v2-v2`, `art_A`, `art_C`, each exactly as stored. `mak4i_get_current` returns only `art_C`. |
| 6 | `mak4i_supersede` with `old_id` = `release-plan-v2-v2-v2` or `art_A` after case 4. | `artifact_not_active`. Nothing is written and no fork is created. |
| 7 | `mak4i_supersede` with `old_id = "release-plan-v7"` (guessed from the old naming scheme). | Treated as any unknown identifier (`not_found`, or `access_denied` without read access). The server never maps it to a head by transforming it. |
| 8 | Conflict on subject `primary-cache` with candidates `cache-red` (legacy) and `art_D` (generated); `merge` into `cache-red`. | New version `art_E` with `supersedes = "cache-red"`, `lineage_id = "cache-red"`, `merged_from = ["art_D", "cache-red"]` and `resolution_id` set. The resolution record lists `successor_artifact_id = "art_E"` and `resulting_heads` → `art_E`. `art_D` is `withdrawn`. Both original IDs are unchanged. |
| 9 | `separate_subjects` where legacy candidate `db-choice-20261012` gets a new key. | Its successor gets a fresh `art_…` ID with the same lineage. A candidate that keeps its key is `unchanged` and gets no new ID. |
| 10 | `select_winner`. | No new version and no new ID. Losers become `withdrawn` under their existing IDs. |
| 11 | A supersession or resolution crashes after the old head was marked superseded (or the pending record was written) but before the successor was stored. | Recovery or an identical retry writes the successor under the identifier already recorded. No second successor and no other new ID appear. |
| 12 | Writes that are refused (`stale_head`, `artifact_not_active`, `subject_key_change`, `validation_error`, `access_denied`). | No version is persisted and no identifier is visible. A later successful write never reuses an identifier that was ever assigned. |
| 13 | A legacy record created by an older client was named `art_9b1…` by hand. | It stays valid. The server never assigns that identifier to another version (A8.3). |
| 14 | Read or write outside project authority with a valid identifier. | Existing authorization applies. Holding an identifier does not grant access, and a denial does not reveal that it exists. |
| 15 | A legacy client sends `mak4i_create` with `artifact_id`. | **[OPEN O1]**. In every option, the supplied value never becomes the identifier of a newly created record. |
| 16 | The same create is sent twice because a response was lost. | **[OPEN O4]** |
| 17 | Two *different* create requests claim the same `(artifact_type, subject_key)` at the same moment. | **[OPEN O3/O5]**. Today: both succeed and form a visible conflict (MAK-0004 §A8.5). |

### 4.2 Example records added in this PR

These validate under the current v0.3 schemas, which shows that the identity rules need no narrowing of the shared ID format:

- [`mak4i_supersede.output.valid-generated-successor-of-legacy-head.json`](../schemas/examples/mcp-tools/mak4i_supersede.output.valid-generated-successor-of-legacy-head.json) (case 2)
- [`mak4i_history.output.valid-mixed-legacy-and-generated.json`](../schemas/examples/mcp-tools/mak4i_history.output.valid-mixed-legacy-and-generated.json) (cases 2, 4 and 5, shortened)
- [`valid-merge-generated-successor.json`](../schemas/examples/resolution-record/valid-merge-generated-successor.json) (case 8)

## 5. Decisions still needed (not decided in this draft)

| | Decision | Options on the table | What it changes |
|---|---|---|---|
| **O1** | A legacy create request that sends `artifact_id` | Reject with `validation_error` (closed inputs), or a documented transition window in which the value is accepted, ignored and reported. In either case it never controls the new ID. | `mak4i_create` input and output schema, the `artifact_exists` row, CONFORMANCE P16, deprecation notes |
| **O2** | ID for a new lineage | `lineage_id` = first version's `art_` ID (current rule), or a separately assigned lineage identifier | MAK-0005 §A2/§A3.1, CONFORMANCE P1, Reference lineage creation |
| **O3** | A create whose `(artifact_type, subject_key)` already has a current head | Default refusal with a pointer to the head, or today's visible conflict. How a client asks for an intentional competing record. | `mak4i_create` input, error codes, MAK-0004 §A3.6/§A8.5, §13.9 |
| **O4** | Retry-key semantics | Key scope (principal, project), lifetime, how a mismatched replay is reported, whether a replay returns the original record and how it is marked, and whether the key affects ID assignment | `mak4i_create` input and output, error codes, MAK-0005 §A8.4, §13.7 |
| **O5** | Guarantee for simultaneous creates on one subject | At most a visible conflict, or exactly one winner (atomic check-and-create on the subject) | MAK-0004 §A8.5, Reference store design, concurrency tests |
| **O6** | Search | Text and exact-subject lookup inputs, ranking, result limits and compact versus full default responses | `mak4i_search` schema, §10.5a/§10.6, §13.9 |

**Retry deduplication and subject concurrency are separate problems (O4 vs O3/O5).** A retry key recognises the *same* request sent again, for example after a lost response, and returns its one result. It does nothing about two *different* requests, from different clients or with different keys or none, that both claim one subject at the same moment. Preventing that needs a subject rule (O3), and to *guarantee* a single winner the check and the create must be one atomic step (O5). A pre-check alone races. The reverse is also true: a subject rule never makes a retry safe for a record without a `subject_key`. The contract has to state both guarantees separately, and the tests have to exercise each one on its own.

Routine field updates without a full supersede, general lineage withdrawal (#4) and cross-type linking are outside this identity slice.

## 6. Compatibility and rollout notes

- The supersede side needs no tool-schema change: §10.5a already makes successor IDs opaque. A client that followed it keeps working. A client that *predicted* successor names (`x-v3`) was already non-conforming and now visibly breaks.
- The create side is the only breaking surface for clients (O1). It ships in the same protocol release as O3–O6, not on its own.
- Legacy data needs no migration. Mixed lineages are normal and permanent.
- Reference runtime changes are out of scope for this PR. Server-generated IDs ship in the Reference together with P1 search-before-create and duplicate handling (talvikai/mak4i-reference#66).
