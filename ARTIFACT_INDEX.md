# MAK4I Artifact Index

All registered artifacts across WD Technology Solutions products.
Last updated: August 2026

---

## Summary

| Type | Count |
|------|-------|
| document | 2 |
| reasoning | 2 |
| workflow | 7 |
| code | 1 |
| prompt | 1 |
| context | 1 |
| **Total** | **14** |

**Total tokens saved: see [docs/MAK4I_SAVINGS_LOG.md](docs/MAK4I_SAVINGS_LOG.md)
for the current, dated running total** — this file catalogs artifacts, not
savings; the two were previously listed together here and drifted out of
sync, which is why savings totals now live only in the log.

---

## Artifacts

### wd-docx-framework v1.1.0
**File:** `artifacts/document/wd-docx-framework-v1.0.0.json`
**Source:** `frameworks/wd-docx-framework/` — tested, working code, not just a description
**Token savings:** ~1,200 per session
**What it is:** Reusable Node.js framework for generating professional DOCX documents. Covers helpers, styles, tables, template, and PDF generator (via LibreOffice).
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

---

## July 9, 2026 Update

Two new daily workflow skills added:

### mak4i-session-start v1.0.0
**File:** `artifacts/workflow/mak4i-session-start-v1.0.0.json`
**Token savings:** ~5,000 per session (context loading eliminated)
**What it is:** The daily session start skill. Step-by-step process for loading all MAK4I artifacts at the start of every Claude session. Eliminates re-explaining context, stack, and history every day.
**Frequency:** Every Claude session

### mak4i-session-end v1.0.0
**File:** `artifacts/workflow/mak4i-session-end-v1.0.0.json`
**Token savings:** ~200 per session (consistency — no missed artifacts)
**What it is:** The daily session end skill. Step-by-step process for capturing new artifacts, updating the index and savings log, packaging the zip, and pushing to GitHub. Ensures no session output is ever lost.
**Frequency:** Every productive Claude session

---

## Updated Summary (as of July 9, 2026)

| Type | Count | Key artifacts |
|------|-------|--------------|
| document | 2 | wd-docx-framework, claude-code-fix-template |
| reasoning | 2 | issue-triage-framework, cloud-run-429-diagnosis |
| workflow | 4 | gcp-wildcard-cert, mak4i-repo-zip-packager, **mak4i-session-start**, **mak4i-session-end** |
| code | 1 | multitenant-slug-auth-pattern |
| prompt | 1 | appointment-parser-prompt |
| context | 1 | schedovia-stack-context |
| **Total** | **11** | |

**Total tokens saved (as of July 9, 2026): 25,100+**
**With daily session-start skill: projected ~5,000 additional tokens saved per day**

---

## July 9, 2026 Update — Core Skills Added

Three new skills added that form the MAK4I daily operating system:

### mak4i-check-before-create v1.0.0
**File:** `artifacts/workflow/mak4i-check-before-create-v1.0.0.json`
**Token savings:** ~100 per session (overhead) + full savings from reuse
**What it is:** The DRY enforcement skill. Before creating ANYTHING, check if it was done before. If found — reuse. If adapted — note what changed. If new — store it. The skill that makes MAK4I self-compounding.
**Trigger:** Before creating any document, code, workflow, or prompt

### mak4i-savings-log-update v1.0.0
**File:** `artifacts/workflow/mak4i-savings-log-update-v1.0.0.json`
**Token savings:** ~50 per session (overhead)
**What it is:** End-of-session skill for recording token savings in SAVINGS_LOG. Tracks reused, adapted, and new artifacts with honest token estimates. This log is the pre-seed evidence for Talvik.
**Trigger:** End of every productive Claude session

---

## The Four Core Daily Skills

These four workflow artifacts form the MAK4I daily operating system:

| Order | Skill | When | What it does |
|-------|-------|------|-------------|
| 1 | mak4i-session-start | Session begins | Load all artifacts — start with context |
| 2 | mak4i-check-before-create | Before any work | Check index → reuse or build new |
| 3 | mak4i-session-end | Session ends | Capture new artifacts, update index |
| 4 | mak4i-savings-log-update | Session ends | Record token savings, update running total |

Skills 3 and 4 can be combined into one end-of-session routine.

---

## Updated Summary (as of July 9, 2026)

| Type | Count |
|------|-------|
| document | 2 |
| reasoning | 2 |
| workflow | 6 |
| code | 1 |
| prompt | 1 |
| context | 1 |
| **Total** | **13** |

---

## July 9, 2026 Final Update — MAK4I Operating System

### mak4i-operating-system v1.0.0
**File:** `artifacts/workflow/mak4i-operating-system-v1.0.0.json`
**Token savings:** ~300 per session (system prompt overhead)
**What it is:** The master skill. Defines WHEN all other skills trigger automatically. Inject into Claude Project Instructions once — all skills fire automatically forever after. No manual triggering needed.
**Trigger:** Always active once injected

SKILLS.md (workflow trigger map) has been moved out of this public repo
and is maintained separately as an internal document.

## Final Summary (as of July 9, 2026)

| Type | Count |
|------|-------|
| document | 2 |
| reasoning | 2 |
| workflow | 7 |
| code | 1 |
| prompt | 1 |
| context | 1 |
| **Total** | **14** |

## The MAK4I Daily Operating System

| # | Skill | Trigger | Artifact |
|---|-------|---------|----------|
| 1 | Session Start | First message | mak4i-session-start |
| 2 | Check Before Create | Before any creation | mak4i-check-before-create |
| 3 | Store New Artifact | After building anything new | mak4i-session-end |
| 4 | Session End + Log | Session wrapping up | mak4i-session-end + mak4i-savings-log-update |
| * | Master OS | Always | mak4i-operating-system |
