# Contributing to MAK4I

Thank you for your interest in contributing to MAK4I — the open protocol for portable AI intelligence.

MAK4I is stewarded by [Talvik, Inc.](https://talvik.ai) and developed in the open.
All contributions are welcome: protocol standards, artifacts, documentation, and feedback.

---

## Ways to Contribute

### 1. Propose a new MAK standard (MAK-XXXX)

MAK standards define the protocol. Anyone can propose one.

**When to propose a MAK standard:**
- You've identified a gap in the protocol that affects portability
- You have a concrete use case that requires a new specification
- You want to formalize a pattern that the community already uses informally

**How to propose:**

1. Open a GitHub Issue with the title: `[MAK-PROPOSAL] Your Title Here`
2. Describe the problem the standard solves
3. Include a draft specification (even a rough one)
4. Talvik reviews, assigns a MAK number, and opens it for community comment
5. After review period, Talvik accepts, revises, or declines with explanation

**MAK standard status flow:**
```
Proposed → Draft → Review → Accepted → Deprecated
```

**Existing standards for reference:**
- [MAK-0001](standards/MAK-0001.md) — Artifact Metadata Schema

---

### 2. Contribute an artifact

Artifacts are the heart of MAK4I. Contributing a high-quality artifact helps the entire community.

**What makes a good artifact:**
- Solves a real, recurring problem (not a one-off)
- Has a clear, specific description
- Includes an honest `token_estimate`
- Is tested against at least one AI platform
- Does not contain sensitive or proprietary information

**How to contribute an artifact:**

1. Create your artifact JSON file following [MAK-0001](standards/MAK-0001.md)
2. Place it in the correct `artifacts/` subdirectory by type:
   ```
   artifacts/
     document/    → templates, frameworks, reference docs
     reasoning/   → diagnostic patterns, decision frameworks
     workflow/    → step-by-step processes, runbooks
     code/        → reusable code patterns, scaffolds
     prompt/      → system prompts, instruction templates
     context/     → project context, stack descriptions
   ```
3. Add an entry to [ARTIFACT_INDEX.md](ARTIFACT_INDEX.md)
4. Open a Pull Request with:
   - The artifact JSON file
   - The ARTIFACT_INDEX.md update
   - A brief description of the problem it solves and tokens saved

**Example artifact PR title:**
```
feat: add terraform-gcp-cloudrun-v1.0.0 artifact (procedural/workflow)
```

---

### 3. Improve the specification

The [SPEC.md](SPEC.md) is a living document. If you find:
- An ambiguity that could cause incompatible implementations
- A missing edge case
- A section that could be clearer

Open a Pull Request with your proposed change and a brief explanation of why.

---

### 4. Report a bug or inconsistency

If you find a bug in:
- The specification (contradictions, unclear rules)
- An existing artifact (wrong schema, outdated content)
- The conformance suite

Open a GitHub Issue with the label `bug` and a clear description of the problem.

**If the bug is a security issue, do not open a public issue — see
[SECURITY.md](SECURITY.md) for how to report it privately instead.**

---

### 5. Share production evidence

MAK4I is built on production evidence, not projections.

If you are using MAK4I in production (even informally), we want to hear:
- How many tokens you're saving per session
- What artifact types you're using most
- What problems you haven't been able to solve yet

Open a GitHub Issue with the label `evidence` or add to the
[SAVINGS_LOG](docs/MAK4I_SAVINGS_LOG.md) via Pull Request.

---

## Pull Request Guidelines

**Branch naming:**
```
feat/your-feature-name
fix/what-youre-fixing
docs/what-youre-documenting
standard/MAK-XXXX-short-name
artifact/artifact-id
```

**Commit message format:**
```
feat: add MAK-0002 context injection specification skeleton
fix: correct token_estimate field validation rule in MAK-0001
docs: add Claude Artifact framing to VISION.md
artifact: add gcp-cloudrun-deploy workflow artifact
standard: open MAK-0003 memory resolution for community review
```

**PR checklist:**
- [ ] Artifact follows MAK-0001 schema (if contributing an artifact)
- [ ] ARTIFACT_INDEX.md updated (if contributing an artifact)
- [ ] Specification change is backward compatible (if editing SPEC.md)
- [ ] No sensitive, proprietary, or personally identifiable information
- [ ] Description explains the problem solved, not just the change made

---

## MAK Standards Process

MAK standards (MAK-XXXX) are how the protocol evolves formally.

### Who can propose
Anyone. No affiliation with Talvik required.

### Review timeline
- **Draft → Review:** 2 weeks community comment period
- **Review → Accepted:** Talvik decision within 1 week after comment period
- **Accepted → Implemented:** Reference implementation follows acceptance

### Naming convention

Standards are numbered sequentially as they're proposed and accepted —
see [SPEC.md](SPEC.md#standards) for the current list (MAK-0001 through
MAK-0007 so far, covering schema, injection, versioning, access control,
and registry topics). There is no reserved numeric range per topic;
numbers are assigned in proposal order, not by category.

### Stewardship
Talvik, Inc. is the steward of the MAK4I protocol. We are committed to:
- Keeping the core protocol open and MIT licensed forever
- Making decisions transparently via GitHub
- Prioritizing backward compatibility
- Building a community steering committee when adoption warrants it

See [GOVERNANCE.md](GOVERNANCE.md) for the full ownership, approval, and
versioning model.

---

## Code of Conduct

MAK4I is an open project. Participants are expected to follow the
[Code of Conduct](CODE_OF_CONDUCT.md). Violations can be reported to
hello@talvik.ai.

---

## Getting Started

```bash
# Clone the repo
git clone https://github.com/talvikai/mak4i-protocol.git
cd mak4i-protocol

# Read the spec
cat SPEC.md

# Browse existing artifacts
ls artifacts/

# Read the first MAK standard
cat standards/MAK-0001.md

# Check the artifact index
cat ARTIFACT_INDEX.md
```

---

## Questions

- **GitHub Discussions:** For protocol questions and proposals
- **GitHub Issues:** For bugs and specific problems
- **Email:** hello@talvik.ai for everything else

---

*© 2026 Talvik, Inc. — MAK4I Protocol is MIT licensed.*
*Contributing to MAK4I does not transfer copyright to Talvik.*
*All contributions remain under the MIT license.*
