# P1 draft: server-assigned record identifiers

Related: [Protocol #15](https://github.com/talvikai/mak4i-protocol/issues/15), [Reference #66](https://github.com/talvikai/mak4i-reference/issues/66).

This review draft captures the approved identity requirements for governed project records. It does not change the current protocol or the current MCP schema. The identity contract and P1 search, duplicate and retry behavior ship together.

## Settled requirements

- The server assigns each newly persisted record version a unique, opaque `art_<uuid>` identifier, including the first version and every successor. An operation that does not persist a new version does not allocate a new record ID.
- Clients consume the returned `artifact_id`. They do not choose a new ID or derive a successor ID from a prior ID. IDs do not encode titles, subjects, dates or version numbers. Use the existing title, subject key, tags, version and timestamp fields for those meanings.
- A successor retains its lineage. Existing lineage IDs, record IDs and history links remain unchanged. A new successor to a legacy head can have a generated ID while its lineage and predecessor still carry legacy IDs.
- Existing IDs remain valid for authorized lookup, history and references under the existing operation rules. This does not permit writing against a stale head. No rename, backfill or rewrite is required.
- Preserve server-managed `created_at` and `updated_at` and their current semantics. No new date field. Business dates such as meeting and target dates remain content or metadata already supported by the record model.

## Contract surfaces to update after review

| Surface | Required change |
|---|---|
| MAK-0005 Part A | Define server allocation for new versions, immutable identifiers and continuity across legacy-to-generated transitions. |
| MAK-0008 and MCP tool schemas | Specify how new clients request creates without choosing an ID, how older create requests are handled, and how tools return and consume opaque IDs. |
| Record, event and history schemas | Continue accepting valid legacy IDs in record responses and references; enforce generated IDs on the new write path. Do not narrow the shared read/reference ID format to UUIDs. |
| Reference | Share allocation logic across all write paths that persist a new project-record version, including conflict resolution where applicable. Preserve the authorization, history and audit behavior of each path. |

## Acceptance examples

| Case | Expected result |
|---|---|
| Create through the new contract | Server returns a fresh opaque ID; existing version and timestamp fields carry their normal values. |
| Supersede a legacy current head with a dated or repeated-version suffix | Successor receives a fresh opaque ID; its lineage stays the same and its predecessor reference is the original ID. |
| Read a mixed legacy/generated lineage | Authorized history includes both forms without rewriting either; current resolves to the new head. |
| Attempt a write against a superseded legacy ID | Existing stale-head handling still applies; no fork is created by interpreting the ID. |
| Resolve a conflict with an operation that creates a record version | The new version receives an opaque ID; existing candidate IDs and provenance remain traceable. |
| Read or write outside project authority | Existing authorization still applies; possession of an ID does not confer access. |

## Decisions still needed for the P1 proposal

1. How the new contract handles a legacy client that submits `artifact_id`: explicit rejection versus a documented transition. In either case the supplied value cannot control a newly generated ID under the new contract.
2. What happens when a create targets an occupied subject, and how an intentional competing record is requested.
3. How retries are recognized and what guarantee applies to simultaneous creates for the same subject. A retry key deduplicates repeated requests, not distinct concurrent requests. If the contract guarantees one winner for reject-by-default, that check and create must be atomic. Define and test the chosen guarantee before release.
4. Whether new lineages continue using the first record's ID, as MAK-0005 currently specifies, or get a separate ID. No existing lineage is rewritten.
5. Exact search, ranking and response defaults, compatibility plan, implementation scope and acceptance review.

Routine field updates without a full supersede, general lineage withdrawal, and cross-type linking are outside this identity slice.
