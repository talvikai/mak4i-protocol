# MAK4I Artifact Index

All registered artifacts across WD Technology Solutions products.
Last updated: July 9, 2026

---

## Summary

| Type | Count | Avg tokens saved/use |
|------|-------|---------------------|
| document | 2 | 750 |
| reasoning | 2 | 375 |
| workflow | 2 | 400 |
| code | 1 | 600 |
| prompt | 1 | 250 |
| context | 1 | 1,500 |
| **Total** | **9** | |

**Total tokens saved (as of June 25, 2026): 25,100+**

---

## Artifacts

### wd-docx-framework v1.0.0
**File:** `artifacts/document/wd-docx-framework-v1.0.0.json`
**Token savings:** ~1,200 per session
**What it is:** Reusable Node.js framework for generating professional DOCX documents. Covers helpers, styles, tables, template, and PDF generator.
**Used in:** Every document generation session

### claude-code-fix-instructions-template v1.0.0
**File:** `artifacts/document/claude-code-fix-instructions-template-v1.0.0.json`
**Token savings:** ~300 per session
**What it is:** Template for Claude Code fix instruction documents. Covers triage format, priority classification, code examples, commit order, testing checklist.
**Used in:** Schedovia fix rounds 1-5

### issue-triage-framework v1.0.0
**File:** `artifacts/reasoning/issue-triage-framework-v1.0.0.json`
**Token savings:** ~400 per session
**What it is:** Reasoning framework for triaging issues into P0/P1/P2/P3. Covers impact assessment, root cause analysis, fix ordering.
**Used in:** Schedovia issue triage

### cloud-run-429-diagnosis v1.0.0
**File:** `artifacts/reasoning/cloud-run-429-diagnosis-v1.0.0.json`
**Token savings:** ~350 per session
**What it is:** Diagnosis pattern for GCP Cloud Run 429 errors. Covers concurrency limits, min/max instances, Redis rate limiting.
**Used in:** Schedovia 429 error investigation

### gcp-wildcard-cert-godaddy v1.0.0
**File:** `artifacts/workflow/gcp-wildcard-cert-godaddy-v1.0.0.json`
**Token savings:** ~500 per session
**What it is:** Step-by-step workflow for wildcard SSL certs on GCP with GoDaddy DNS.
**Used in:** Schedovia SSL fix

### mak4i-repo-zip-packager v1.0.0
**File:** `artifacts/workflow/mak4i-repo-zip-packager-v1.0.0.json`
**Token savings:** ~300 per session
**What it is:** End-of-session workflow to sync artifacts and package the repo ZIP.
**Used in:** Every session that produces new artifacts

### multitenant-slug-auth-pattern v1.0.0
**File:** `artifacts/code/multitenant-slug-auth-pattern-v1.0.0.json`
**Token savings:** ~600 per session
**What it is:** Multi-tenant slug auth pattern for SaaS. Firebase Auth + requireAuth middleware + role-based routing.
**Used in:** Schedovia auth architecture

### appointment-parser-prompt v1.0.0
**File:** `artifacts/prompt/appointment-parser-prompt-v1.0.0.json`
**Token savings:** ~250 per session
**What it is:** Claude prompt for parsing appointments from natural language and MMS photos.
**Used in:** Reminder AI app

### schedovia-stack-context v1.0.0
**File:** `artifacts/context/schedovia-stack-context-v1.0.0.json`
**Token savings:** ~1,500 per session
**What it is:** Full stack context for Schedovia. Eliminates re-explaining architecture, business rules, and patterns.
**Used in:** Every Schedovia development session
