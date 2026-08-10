# MAK4I Savings Log

## Summary (as of August 7, 2026)

| Metric | Value |
|--------|-------|
| Running total tokens saved | 38,400 |
| Sessions logged | 27 (through Jul 9, 2026) + 2 (Aug 7, 2026) |

*Note: the per-project breakdown below (Schedovia/AIOps/MAK4I/Appt Reminder,
27 sessions, 25,100 tokens) reflects the state as of July 9, 2026, before
that day's detailed session log (see below) added a further 13,300 tokens,
bringing the running total to 38,400. The per-project table has not been
recalculated to reflect the full 38,400 — treat the 38,400 figure as the
current authoritative running total, and the per-project table as a
snapshot that predates it.*

| Project | Sessions | Tokens saved (as of Jul 9 snapshot) |
|---------|----------|-------------|
| Schedovia | 8 | 8,650 |
| AIOps | 1 | 1,200 |
| MAK4I | 16 | 13,800 |
| Appt Reminder | 2 | 1,450 |
| **Total (Jul 9 snapshot)** | **27** | **25,100** |

## Session Log

| Date | Project | Artifact | Type | Tokens saved | Notes |
|------|---------|----------|------|-------------|-------|
| 2026-06-23 | Schedovia | wd-docx-framework v1.0 | document | 1,200 | First use |
| 2026-06-25 | MAK4I | All 9 artifacts registered | multiple | 5,100 | Registration session |
| 2026-07-09 | MAK4I | mak4i-repo-zip-packager v1.0 | workflow | 300 | Repo pushed to GitHub |
| 2026-07-09 | MAK4I | wd-docx-framework v1.0 | document | 1,200 | Trademark doc generated |
| 2026-07-09 | Schedovia | schedovia-stack-context v1.0 | context | 1,500 | Long session — multiple docs |
| 2026-08-07 | MAK4I | New docx generator (not wd-docx-framework) | document | 0 | Checked artifact index first — wd-docx-framework v1.0.0 catalogued but underlying code unavailable in this session (likely built in a prior, separate session). Built new generator rather than reusing. Logged as new build, not reuse, per check-before-create discipline. Generated MAK4I_Pre_Public_Repo_Checklist.docx. |
| 2026-08-07 | MAK4I | wd-docx-framework v1.1.0 (rebuild) | framework | 0 | Framework rebuilt from its documented interface and added to the repo at frameworks/wd-docx-framework/, since the original source wasn't available. Tested end-to-end (docx + PDF). 0 tokens saved this session — this closes the gap so future sessions can genuinely reuse it. Checklist doc regenerated through the real framework to confirm it works. |

## Milestones

| Milestone | Target | Achieved |
|-----------|--------|---------|
| First session logged | Jun 2026 | ✓ Jun 23, 2026 |
| 9 artifacts registered | Jul 2026 | ✓ Jun 25, 2026 |
| 25,000 tokens saved | Aug 2026 | ✓ Jun 25, 2026 |
| MAK4I repo live on GitHub | Jul 2026 | ✓ Jul 9, 2026 |
| 50,000 tokens saved | Aug 2026 | — |
| Hosted registry live | Feb 2027 | — |
| Automated tracking | Feb 2027 | — |

## Known Gap — 2026-08-07 (resolved same day)

The `wd-docx-framework-v1.0.0.json` artifact entry described a reusable Node.js
docx/PDF generation framework, but the underlying source code was not present
in this working environment. Prior log entries (2026-06-25, 2026-07-09)
recorded reuse of this framework — those entries reflect what happened in
those sessions, which may have had the code available.

Resolved same session: the framework was rebuilt from its documented interface
and committed to this repo at `frameworks/wd-docx-framework/` (v1.1.0), tested
end-to-end for both docx and PDF output. Future sessions in this repo can now
genuinely reuse it rather than rebuilding it again.

---

## Session Log — July 27, 2026 (session compacted)

### Session summary
**Date:** July 9, 2026
**Tracks:** Schedovia + MAK4I + Talvik setup + Reminder App
**Duration:** Full day session (longest session to date)

### Artifacts REUSED this session

| Artifact | Times used | Tokens saved |
|----------|-----------|-------------|
| wd-docx-framework | 6 | 7,200 |
| schedovia-stack-context | 1 | 1,500 |
| issue-triage-framework | 2 | 800 |
| claude-code-fix-instructions-template | 5 | 1,500 |
| mak4i-repo-zip-packager | 4 | 1,200 |
| appointment-parser-prompt | 1 | 250 |
| cloud-run-429-diagnosis | 1 | 350 |
| gcp-wildcard-cert-godaddy | 1 | 500 |
| **Session reuse total** | | **13,300 tokens** |

### Artifacts NEW this session

| Artifact ID | Type | Future savings/use |
|-------------|------|-------------------|
| mak4i-session-start | workflow | ~5,000 |
| mak4i-session-end | workflow | ~200 |
| mak4i-check-before-create | workflow | ~100 |
| mak4i-savings-log-update | workflow | ~50 |
| mak4i-operating-system | workflow | ~300 |
| SKILLS.md | document | N/A (documentation) |
| CONTRIBUTING.md | document | N/A (documentation) |
| VISION.md (rewrite) | document | ~800 (context) |
| PROBLEM.md (rewrite) | document | ~900 (context) |

### Documents produced this session

| Document | Type |
|----------|------|
| Schedovia_Why_Switch_v2.pptx | Pilot presentation |
| Schedovia_Competitive_Comparison.docx | Research doc |
| Schedovia_Competitive_Positioning.docx | Pilot reference |
| Trademark_Consultation_Askew_IP.docx | Attorney prep |
| Weekend_GCP_Tasks_July4_v1.0.docx | GCP deployment |
| ReminderApp_Weekend_Build_v1.0.docx | Build requirements |

### Savings summary

| | Tokens |
|---|--------|
| Reused this session | 13,300 |
| Previous running total | 25,100 |
| **New running total** | **38,400** |
| New artifacts stored | 5 workflow skills |
| Projected future savings per session | ~5,650 additional |

### Notes
- MAK4I operating system fully defined this session
- Four core daily skills created and stored
- Skills trigger map defined in SKILLS.md
- Session end skill was NOT automatic — ran manually
- Action required: paste mak4i-operating-system into
  Claude Project Instructions before next session
