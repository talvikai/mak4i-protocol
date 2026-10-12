# MAK4I Artifact Index

Sample MAK-0001 artifacts (Distributable Artifact packaging metadata) kept in this
repository as examples. Every file validates against
[`schemas/artifact.schema.json`](schemas/artifact.schema.json). The validator checks that
each file name matches its `id` and `version`.

Last updated: 2026-10-12

---

## Summary

| Directory | Count |
|------|-------|
| code | 1 |
| context | 1 |
| document | 1 |
| prompt | 1 |
| reasoning | 2 |
| workflow | 7 |
| **Total** | **13** |

Directories group the samples by kind. They are not the MAK-0001 `type`
(`procedural` / `semantic` / `episodic`), which each file declares.

Reuse and token-savings records are kept in
[docs/background/MAK4I_SAVINGS_LOG.md](docs/background/MAK4I_SAVINGS_LOG.md), a non-normative
background document.

---

## Artifacts

### multitenant-slug-auth-pattern v1.0.1
**File:** `artifacts/code/multitenant-slug-auth-pattern-v1.0.1.json`  
**Type:** procedural  
**Size estimate:** ~600 tokens  
**What it is:** Multi-tenant slug authentication pattern for SaaS: managed auth, request middleware, role-based routing.

### example-app-stack-context v1.0.1
**File:** `artifacts/context/example-app-stack-context-v1.0.1.json`  
**Type:** semantic  
**Size estimate:** ~1500 tokens  
**What it is:** Stack context for an example appointment-scheduling SaaS, so sessions don't re-explain the architecture.

### claude-code-fix-instructions-template v1.0.1
**File:** `artifacts/document/claude-code-fix-instructions-template-v1.0.1.json`  
**Type:** procedural  
**Size estimate:** ~300 tokens  
**What it is:** Template for AI coding-agent fix instructions: triage format, priority classification, code examples, commit order, testing checklist.

### appointment-parser-prompt v1.0.1
**File:** `artifacts/prompt/appointment-parser-prompt-v1.0.1.json`  
**Type:** procedural  
**Size estimate:** ~250 tokens  
**What it is:** Prompt for parsing appointments from natural language and photos of appointment cards.

### cloud-run-429-diagnosis v1.0.1
**File:** `artifacts/reasoning/cloud-run-429-diagnosis-v1.0.1.json`  
**Type:** procedural  
**Size estimate:** ~350 tokens  
**What it is:** Diagnosis pattern for HTTP 429 errors on a serverless container platform: concurrency limits, instance bounds, rate limiting.

### issue-triage-framework v1.0.1
**File:** `artifacts/reasoning/issue-triage-framework-v1.0.1.json`  
**Type:** procedural  
**Size estimate:** ~400 tokens  
**What it is:** Reasoning framework for triaging issues into P0–P3: impact assessment, root-cause analysis, fix ordering.

### gcp-wildcard-cert-godaddy v1.0.1
**File:** `artifacts/workflow/gcp-wildcard-cert-godaddy-v1.0.1.json`  
**Type:** procedural  
**Size estimate:** ~500 tokens  
**What it is:** Step-by-step workflow for wildcard TLS certificates on a cloud load balancer with an external DNS provider.

### mak4i-check-before-create v1.0.1
**File:** `artifacts/workflow/mak4i-check-before-create-v1.0.1.json`  
**Type:** procedural  
**Size estimate:** ~100 tokens  
**What it is:** Check-before-create workflow: look for an existing artifact before building anything new; reuse, adapt or store.

### mak4i-operating-system v1.0.1
**File:** `artifacts/workflow/mak4i-operating-system-v1.0.1.json`  
**Type:** procedural  
**Size estimate:** ~300 tokens  
**What it is:** Master workflow that defines when the other workflows trigger in a session.

### mak4i-repo-zip-packager v1.0.1
**File:** `artifacts/workflow/mak4i-repo-zip-packager-v1.0.1.json`  
**Type:** procedural  
**Size estimate:** ~300 tokens  
**What it is:** End-of-session workflow that syncs artifacts and packages the repository as a ZIP.

### mak4i-savings-log-update v1.0.1
**File:** `artifacts/workflow/mak4i-savings-log-update-v1.0.1.json`  
**Type:** procedural  
**Size estimate:** ~50 tokens  
**What it is:** End-of-session workflow for recording honest reuse and token-savings estimates.

### mak4i-session-end v1.0.1
**File:** `artifacts/workflow/mak4i-session-end-v1.0.1.json`  
**Type:** procedural  
**Size estimate:** ~200 tokens  
**What it is:** Daily session-end workflow: capture new artifacts, update the index and savings log, package and push.

### mak4i-session-start v1.0.1
**File:** `artifacts/workflow/mak4i-session-start-v1.0.1.json`  
**Type:** procedural  
**Size estimate:** ~5000 tokens  
**What it is:** Daily session-start workflow: load the relevant artifacts before work begins.

---

## The sample session workflows

Five of the workflow samples describe one way to use MAK4I in a daily AI
session. They are examples of **procedural knowledge**, not first-class
"skills" (skills as a protocol object are approved future scope; see
[ROADMAP.md](ROADMAP.md#approved-future-protocol-scope)).

| # | Step | Trigger | Artifact |
|---|------|---------|----------|
| 1 | Session start | First message | mak4i-session-start |
| 2 | Check before create | Before any creation | mak4i-check-before-create |
| 3 | Store new artifact | After building anything new | mak4i-session-end |
| 4 | Session end and log | Session wrapping up | mak4i-session-end + mak4i-savings-log-update |
| * | Master workflow | Always | mak4i-operating-system |
