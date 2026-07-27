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

---

## Pre-Launch Checklist — August 31, 2026

All tasks required before flipping the repo to public.

### Week 1 — July 28 to August 3 (Legal Foundation)

```
□ Call Andrew Bosin — 201-446-9643 (VM left July 27)
□ Decide: incorporate first or file trademark personally
□ Schedovia pilot calls — Brenda's LLC, Massage 44, Hoosier Barbershop
□ Confirm Reminder App running on GCP Cloud Run
□ Confirm A2P SMS approved — test with real phone
```

### Week 2 — August 4 to 10 (Incorporation + Filing)

```
Legal:
□ Incorporate Talvik, Inc. as Delaware C-Corp
  → Stripe Atlas ($500) or Clerky ($799)
□ File 83(b) election within 30 days — DO NOT MISS
□ File trademark intent-to-use: TALVIK (word mark)
  → Classes 9 + 42
□ File trademark intent-to-use: MAK4I (word mark)
  → If Andrew recommends
□ Transfer GitHub org to Talvik, Inc. formally
□ Set up CLA Assistant on mak4i-protocol repo
□ Inter-company agreement: WD Technology ↔ Talvik
  → License + versioned API contract

MAK4I Repo:
□ Complete Claude 101 certificate → add to LinkedIn ← ALMOST DONE
□ Complete MCP course → add to LinkedIn
□ Update README with incorporation status
□ Add "Talvik, Inc." as legal owner throughout docs
```

### Week 3 — August 11 to 17 (Content + Community)

```
Repo:
□ Final review: README, PROBLEM, VISION, SPEC, CONTRIBUTING
□ MAK-0001 content review — ensure it's launch-ready
□ Add CHANGELOG.md (even if just v0.1 entry)
□ Set up GitHub Discussions for RFC proposals
□ Add GitHub issue templates:
    Bug report
    MAK standard proposal
    Artifact contribution
□ Add GitHub PR template

Content:
□ Write Dev.to launch article:
  "What is MAK4I and why we built it"
  Include WD Tech production data (25,100+ tokens)
□ Write X/Twitter launch thread (10-12 posts)
□ Write LinkedIn announcement for Talvik page
□ Build token savings calculator as Claude Artifact
  → Add share URL to README
□ Record a short Loom demo (optional but powerful)

Technical:
□ Create simple landing page on talvik.ai
  → What MAK4I is
  → Link to GitHub repo
  → Link to Dev.to article
  → hello@talvik.ai contact
□ Set up Google Workspace for talvik.ai email
  → hello@talvik.ai
  → Use this for GitHub, legal, and outreach
```

### Week 4 — August 18 to 24 (Pre-Launch Review)

```
Review:
□ Share repo with 2-3 developer friends for honest feedback
□ Check all links in README work correctly
□ Verify MAK-0001 renders correctly on GitHub
□ Verify all artifact JSON files are valid
□ Final spell-check all markdown files

Social:
□ Write ProductHunt submission
  → Tagline, description, gallery images
  → Schedule for SEPARATE day after GitHub launch
  → Best days: Monday to Thursday
□ Prepare Bluesky launch post @talvikai
□ Prepare Dev.to article formatted and ready to publish
□ Draft Hacker News Show HN post
  → "Show HN: MAK4I — open protocol for portable AI memory"

Technical:
□ Confirm talvik.ai landing page live
□ Set up Plausible or GoatCounter analytics
  → Free, privacy-focused
  → Measure repo traffic after launch
□ Add repo topics on GitHub:
  artificial-intelligence, llm, memory, protocol,
  open-source, claude, chatgpt, developer-tools
□ Pin mak4i-protocol repo in talvikai org
```

### Week 5 — August 25 to 31 (Launch)

```
Aug 25-30:
□ Final repo polish
□ Schedule all social posts for Aug 31
□ Brief Schedovia pilots about MAK4I
  → "We use this internally — it's what powers
     our AI development. Going public Aug 31."

August 31 — Launch Day:
□ Flip repo to PUBLIC on GitHub
□ Post X/Twitter launch thread @talvikai
□ Publish Dev.to article @talvikai
□ Submit to Hacker News (Show HN)
□ Post on LinkedIn — Talvik company page
□ Post on Bluesky @talvikai
□ Post on ProductHunt — wait 2-3 days after GitHub
□ Monitor GitHub for early stars and issues
□ Respond to every comment and issue same day

Post-Launch Week (Sep 1-7):
□ ProductHunt launch (Mon-Thu)
□ Reddit posts:
  r/MachineLearning
  r/artificial
  r/LocalLLaMA
  r/programming
□ Follow up on Hacker News comments
□ Thank early GitHub stargazers personally
□ Write first GitHub Discussion post:
  "What MAK standard should we write next?"
```

---

## Launch Success Metrics

```
Week 1 after launch targets:
  GitHub stars:      50+
  Dev.to reactions:  100+
  HN upvotes:        50+ (front page = 100+)
  GitHub issues:     5+ (community engagement)
  
Month 1 targets:
  GitHub stars:      200+
  Community members: 20+ active
  MAK standard PRs:  2+
  External artifacts: 1+
```
