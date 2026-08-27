# Understanding MAK4I

> A plain-language introduction to MAK4I, MAK specifications, and how
> the Phase 1 standards work together.

**Status:** Working Guide\
**Audience:** Developers, contributors, implementers, and anyone
evaluating MAK4I\
**Scope:** Explanatory documentation. This document is not a normative
MAK specification.

------------------------------------------------------------------------

## 1. MAK4I in Plain English

MAK4I is an open protocol intended to let useful AI context, decisions,
knowledge, history, and artifacts remain **portable and understandable
across AI tools and implementations**.

The goal is not to require organizations to store their information in
Talvik infrastructure. A MAK4I-compatible implementation should be able
to store artifacts:

-   locally,
-   on-premises,
-   in customer-controlled cloud infrastructure,
-   in third-party compatible systems, or
-   in a managed service,

while preserving the meaning required for interoperability.

### The continuity problem

AI systems often work well inside the context they currently have. The
problem appears when work continues later, moves to another session, or
moves to another AI tool.

For example, imagine that during **Session 3** an architecture decision
is made:

``` text
Architecture Decision
Database: PostgreSQL
Reason: Operational requirements
Status: Active
```

By **Session 8**, perhaps in a different AI tool, the user should not
have to reconstruct that decision manually.

The new AI should be able to receive enough relevant context to
understand:

-   PostgreSQL is the approved database,
-   why PostgreSQL was selected,
-   that the decision is still active, and
-   whether anything has changed since that decision was made.

MAK4I is intended to provide the interoperable foundation for
preserving, resolving, and supplying that knowledge.

The objective is not simply to save chat history.

The objective is **knowledge continuity**.

------------------------------------------------------------------------

## 2. What Is a MAK Specification?

A MAK specification is a **protocol contract**.

It describes what independent MAK4I-compatible systems must understand
or do so that they can interoperate consistently.

A specification is **not** the source code that implements MAK4I. It is
also not a particular database design, cloud architecture, SDK, AI
model, or Talvik product.

### REST API analogy

For developers familiar with REST APIs, it helps to distinguish three
concepts:

**Schema**\
Defines the structure of data.

**Payload**\
An actual instance of that data.

**Specification**\
Defines the structure **and the meaning and behavior associated with
it**.

For example, a JSON payload might contain:

``` json
{
  "status": "clarification_required",
  "artifacts": ["artifact-123", "artifact-456"]
}
```

The payload alone does not tell an independent implementation:

-   what `clarification_required` means,
-   when that status MUST be produced,
-   what qualifies as a conflict,
-   whether automatic resolution is allowed,
-   what the consumer should do next, or
-   what information must be preserved for auditability.

Those rules belong in the specification.

### What a MAK specification should define

Depending on the standard, a MAK specification may define:

-   concepts and terminology,
-   required data or metadata,
-   required behavior,
-   prohibited behavior,
-   recommended behavior,
-   optional behavior,
-   processing rules,
-   failure conditions,
-   ambiguity handling,
-   conflict handling,
-   version and lifecycle semantics,
-   interoperability requirements,
-   security boundaries,
-   edge cases,
-   conformance requirements.

Normative terms such as **MUST**, **MUST NOT**, **SHOULD**, **SHOULD
NOT**, and **MAY** are used when the specification needs to state
interoperability requirements.

The goal is that two independent engineers should be able to implement
the standard without needing private knowledge of Talvik's
implementation.

------------------------------------------------------------------------

## 3. What a Specification Should Not Be

A MAK standard should not unnecessarily dictate implementation
technology.

For example:

> **Specification:** A conforming implementation MUST preserve artifact
> identity across compatible systems.

That can be a protocol requirement.

But:

> **Implementation:** Talvik stores artifact records in PostgreSQL.

is an implementation decision.

MAK4I should not require technologies such as:

-   PostgreSQL,
-   Redis,
-   vector databases,
-   embeddings,
-   a specific cloud provider,
-   a specific programming language,
-   a specific AI model,
-   MCP,
-   or Talvik-hosted infrastructure,

unless interoperability genuinely requires that choice.

This separation is important because MAK4I is intended to be a protocol
rather than a Talvik-only product format.

One organization might implement MAK4I in Python and store artifacts in
GCP. Another might implement it in Java and store artifacts on-premises.
A third might build an AI consumer without using Talvik infrastructure
at all.

If they follow the MAK specifications, they should still be able to
understand the same MAK4I information consistently.

------------------------------------------------------------------------

## 4. The Five Phase 1 MAK Standards

The Phase 1 standards divide the core interoperability problem into
separate responsibilities.

  -----------------------------------------------------------------------
  Standard                Core question           Primary responsibility
  ----------------------- ----------------------- -----------------------
  **MAK-0001 --- Artifact **What is an            Defines the common
  Metadata Schema**       artifact?**             metadata and
                                                  representation needed
                                                  to identify and
                                                  describe a MAK4I
                                                  artifact.

  **MAK-0002 --- Context  **What context should   Defines how relevant
  Injection               the AI receive?**       project state,
  Specification**                                 decisions, rationale,
                                                  history, and other
                                                  resolved context are
                                                  supplied to an AI
                                                  consumer.

  **MAK-0003 --- Memory / **Which artifacts       Defines how available
  Artifact Resolution**   apply?**                artifacts are evaluated
                                                  for eligibility,
                                                  relevance, and
                                                  applicability to the
                                                  current request or
                                                  task.

  **MAK-0004 --- Conflict **What happens when     Defines what
  Resolution              applicable artifacts    constitutes a conflict
  Specification**         disagree?**             and how a conforming
                                                  implementation
                                                  resolves, escalates, or
                                                  requests clarification
                                                  for it.

  **MAK-0005 ---          **Which version or      Defines artifact
  Versioning &            state applies?**        evolution, lineage,
  Compatibility                                   lifecycle,
  Specification**                                 supersession, history,
                                                  and compatibility.
  -----------------------------------------------------------------------

These standards are separate because each addresses a different
interoperability problem.

They are also related. MAK-0003 cannot reliably evaluate artifacts if
their metadata has no common meaning. MAK-0004 needs to understand the
applicable artifacts it is comparing. MAK-0005 provides lifecycle and
version information that can affect resolution and conflict handling.
MAK-0002 needs the resulting knowledge in order to give an AI useful
context.

The standards therefore form a system rather than five isolated
documents.

------------------------------------------------------------------------

## 5. One Scenario Across All Five Standards

Consider a project that has accumulated hundreds or thousands of pieces
of AI-related knowledge.

A user opens a new AI session and asks:

> **Add a customer-preferences service to this project.**

Existing knowledge might include:

-   the current database,
-   the cloud environment,
-   API standards,
-   organization security policies,
-   architecture decisions,
-   rationale behind those decisions,
-   historical project states,
-   prior AI session notes,
-   rejected approaches,
-   and newer information that supersedes older information.

The AI should not receive all of it blindly.

MAK4I needs to determine what the information means, what applies,
whether anything disagrees, which state is current, and what the AI
actually needs.

### MAK-0001 --- Describe the artifacts

Before MAK4I can operate on project knowledge, artifacts need a common
interoperable representation.

Conceptually, an artifact might carry information such as:

``` text
Artifact
  ├── ID
  ├── Type
  ├── Version
  ├── Scope
  ├── Source / provenance
  ├── Temporal information
  └── Content / payload reference
```

MAK-0001 defines the common foundation needed for other MAK standards to
interpret those artifacts consistently.

### MAK-0003 --- Determine what applies

The project may contain 10,000 artifacts, but the current task should
not receive all 10,000.

MAK-0003 determines which artifacts are eligible, relevant, and
applicable.

For the customer-preferences service, the applicable set might include:

``` text
✓ Current project architecture
✓ Active database decision
✓ Organization security policy
✓ API development standard
✓ Relevant production requirements
✓ Relevant historical rationale

✗ Unrelated billing-project architecture
✗ HR policy
✗ Unrelated session history
```

The standard should define interoperable resolution behavior without
requiring every implementation to use the same search technology.

### MAK-0004 --- Handle disagreement

Suppose MAK-0003 identifies two applicable artifacts:

``` text
Session note:
"Maybe use MongoDB."

Approved architecture decision:
"PostgreSQL is the approved database."
```

Both may be relevant, but they disagree.

MAK-0004 defines whether the disagreement constitutes a conflict and
what a conforming implementation must do.

Depending on the eventual normative rules, the outcome may involve:

-   safe automatic resolution,
-   clarification,
-   an authorized decision or override,
-   or escalation.

The implementation should not silently choose whichever statement it
happens to retrieve first.

### MAK-0005 --- Preserve evolution and history

Knowledge changes over time.

For example:

``` text
v1  Database = MySQL        [historical]
v2  Database = PostgreSQL   [superseded]
v3  Database = AlloyDB      [current]
```

MAK4I should preserve history without treating every historical state as
current.

MAK-0005 defines how versions relate, how lifecycle state is
represented, how supersession works, and how compatibility/history are
understood.

This is also why information from an older session does not
automatically become irrelevant simply because newer sessions exist. A
decision made in Session 3 may still be active in Session 8.

### MAK-0002 --- Give the AI usable context

After relevant information has been identified and its conflicts,
versions, and lifecycle meaning have been understood, the AI still needs
usable context.

Conceptually, the resulting context could communicate:

``` text
PROJECT
Customer Platform

CURRENT STATE
Database: PostgreSQL
Cloud: GCP

ACTIVE DECISION
PostgreSQL is the approved database.

RATIONALE
Selected because of operational requirements.

CURRENT TASK
Add customer-preferences service.

RELEVANT HISTORY / CHANGES
Only the historical information useful to this task.
```

The important point is that the new AI does not merely receive the word
`PostgreSQL`.

It receives enough meaning to understand:

``` text
✓ PostgreSQL is the approved database
✓ Why it was selected
✓ The decision is still active
```

### Conceptual relationship

``` text
AVAILABLE MAK4I ARTIFACTS
          │
          ▼
      MAK-0001
 Common artifact meaning
          │
          ▼
      MAK-0003  ◄── Current task/request
 Which artifacts apply?
          │
          ▼
      MAK-0004
 What if applicable artifacts conflict?
          │
          ▼
      MAK-0005
 Version / lifecycle / lineage
          │
          ▼
      MAK-0002
 Assemble and inject usable context
          │
          ▼
       AI CONSUMER
          │
          ▼
 Continue work with relevant prior knowledge
```

This diagram is a **conceptual explanation**, not necessarily a
mandatory runtime execution order. For example, MAK-0005 lifecycle and
version information may participate during resolution and conflict
handling.

The standards must ultimately be reconciled so that their
responsibilities are clear and they do not duplicate or contradict one
another.

------------------------------------------------------------------------

## The Interoperability Test

A useful test for every MAK specification is:

> **Could an engineer who has never spoken with Talvik implement this
> behavior correctly by reading the MAK standards?**

Imagine:

-   Company A implements MAK4I in Java and stores artifacts in AWS.
-   Company B implements MAK4I in Python and stores artifacts
    on-premises.
-   Company C builds an AI consumer that does not use Talvik
    infrastructure.

If all three can agree on artifact meaning, applicability, conflict
behavior, version/history semantics, and context delivery, MAK4I is
functioning as an interoperable protocol.

If they must inspect Talvik's source code to discover the intended
behavior, the specification is not complete enough.

------------------------------------------------------------------------

*This document is explanatory and does not replace the normative MAK
specifications. Where this guide and an accepted MAK specification
differ, the accepted specification governs.*
