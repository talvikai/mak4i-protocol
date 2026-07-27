# MAK4I Skills

Skills are repeatable processes that run automatically based on context triggers.
Once the MAK4I Operating System is loaded, these skills fire without being asked.

---

## The Four Core Skills

### Skill 1 — Session Start
**Artifact:** `mak4i-session-start`
**Triggers when:** First message of any Claude session

```
What happens automatically:
  → Upload mak4i-protocol.zip (you do this)
  → Claude loads ARTIFACT_INDEX.md
  → Claude loads schedovia-stack-context
  → Claude loads SESSION_STARTER.md
  → Claude confirms what's loaded
  → Claude asks which track today
  → Work begins with full context
  
Time: ~2-3 minutes
Tokens saved: ~5,000 per session
```

---

### Skill 2 — Check Before Create
**Artifact:** `mak4i-check-before-create`
**Triggers when:** Any request to create, write, build, or generate anything

```
What happens automatically:
  → STOP before building
  → Search ARTIFACT_INDEX for similar work
  
  If FOUND (exact match):
    → Load and reuse existing artifact
    → Record tokens saved
    → Continue with work
  
  If FOUND (partial match):
    → Load and adapt existing artifact
    → Note what changed
    → Record approximate tokens saved
  
  If NOT FOUND:
    → Confirm with user
    → Build from scratch
    → Trigger Skill 3 immediately after

Time: ~1 minute overhead
Tokens saved: Full token_estimate of reused artifact
```

---

### Skill 3 — Store New Artifact
**Artifact:** `mak4i-session-end` (artifact capture portion)
**Triggers when:** Something valuable was built from scratch for the first time

```
What happens automatically:
  → Immediately after completing new output
  → Claude prompts: "Store this as a MAK4I artifact?"
  → If yes:
      → Assign artifact ID (kebab-case)
      → Determine type: procedural | semantic | episodic
      → Estimate honest token_savings per future use
      → Create JSON file (MAK-0001 schema)
      → Place in correct artifacts/ subdirectory
      → Update ARTIFACT_INDEX.md
  → Record as NEW in session tally

Time: ~3-5 minutes
Tokens saved this session: 0
Tokens saved per future use: [token_estimate]
```

---

### Skill 4 — Session End + Savings Log
**Artifact:** `mak4i-session-end` + `mak4i-savings-log-update`
**Triggers when:** Session is ending (user signals or work wraps up)

```
Signals that session is ending:
  "we are done"
  "that's all for today"
  "push to github"
  "package the repo"
  "wrap up"

What happens automatically:
  → List all new artifacts from this session
  → Confirm all new artifacts stored and indexed
  → Update SESSION_STARTER.md if needed
  → Write savings log entry:
      Date, track, artifacts reused/adapted/new
      Tokens saved today, running total
  → Package mak4i-protocol.zip
  → Remind user to push to GitHub

Time: ~5-10 minutes
Result: Zero session work lost. Repo updated. Evidence logged.
```

---

## The Trigger Map

```
SESSION START
    ↓
    Skill 1: Load all artifacts
    ↓
    Work begins with full context

FOR EVERY PIECE OF WORK
    ↓
    Skill 2: Check before create
    ↓
    ┌─────────────────────────────────────┐
    │ Found exact?  → Reuse → Log saving  │
    │ Found partial? → Adapt → Log saving │
    │ Not found?    → Build new           │
    │                    ↓               │
    │               Skill 3: Store it    │
    └─────────────────────────────────────┘

SESSION END
    ↓
    Skill 4: Log savings + Package + Push
```

---

## How to Make Skills Automatic

**Best method — Claude.ai Project Instructions:**

```
1. Go to your Claude.ai Project (Schedovia or MAK4I)
2. Click Project Settings → Instructions
3. Paste the content of mak4i-operating-system artifact
4. Save

Now every conversation in that Project automatically:
  → Applies Skill 1 at session start
  → Applies Skill 2 before creating anything
  → Applies Skill 3 after creating anything new
  → Applies Skill 4 when session ends

Set it once. Never think about it again.
```

**Alternative — session start message:**

```
Upload mak4i-protocol.zip and say:
"Load the MAK4I operating system for this session.
 Apply all skills automatically based on triggers."
```

---

## Skill Artifact Index

| Artifact ID | Trigger | What it does |
|-------------|---------|-------------|
| mak4i-operating-system | Always | Master skill — defines all triggers |
| mak4i-session-start | Session begins | Load context, confirm artifacts |
| mak4i-check-before-create | Before any creation | Check index, reuse or build new |
| mak4i-session-end | Session ends | Capture artifacts, update index, package |
| mak4i-savings-log-update | Session ends | Write token savings to log |

---

## The Compound Effect

```
These skills compound over time:

Month 1:   11 artifacts. Every session saves ~900 tokens.
Month 3:   25 artifacts. Every session saves ~2,000 tokens.
Month 6:   50 artifacts. Every session saves ~4,000 tokens.
Month 12:  100+ artifacts. Every session saves ~8,000+ tokens.

The more you run the skills, the more artifacts accumulate.
The more artifacts accumulate, the more each session saves.
The more each session saves, the stronger the pre-seed story.

This is MAK4I working as designed.
```

---

*© 2026 Talvik, Inc. — talvik.ai*
