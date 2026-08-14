# MAK4I and MCP

*This is the single authoritative explanation of how MAK4I relates to the
Model Context Protocol. [README.md](README.md), [VISION.md](VISION.md),
and [ARCHITECTURE.md](ARCHITECTURE.md) reference this document rather than
repeating the explanation.*

---

## Is MAK4I Competing with MCP?

No. They solve different problems, at different layers.

```
MCP defines:    How AI models connect to external tools and data
                (the transport and communication layer)

MAK4I defines:  What AI knowledge IS and how it's stored
                (the content and memory layer)

They work together:
  MAK4I Registry → exposed as MCP server
  AI tools connect to MAK4I via MCP
  MAK4I artifacts flow through MCP to the AI

MCP without MAK4I:  a connection with nothing persistent to transfer
MAK4I without MCP:  knowledge stored with no standard delivery method
Together:           persistent, portable AI memory delivered anywhere
```

**The USB-C analogy:**

```
MCP   = the USB-C standard (how devices connect)
MAK4I = the files on the drive (what gets transferred)

You need both.
MCP without MAK4I: a connection with nothing to transfer
MAK4I without MCP: content with no standard way to deliver it
```

Phase 5 of the MAK4I roadmap builds MAK4I as a native MCP server. After
that, any MCP-compatible tool automatically gains access to the MAK4I
registry without additional integration work. See
[ROADMAP.md](ROADMAP.md) for phase timing.

---

## The Anthropic/MCP — Talvik/MAK4I Parallel

| | Anthropic + MCP | Talvik + MAK4I |
|---|---|---|
| Created | MCP protocol | MAK4I protocol |
| License | Apache 2.0 (open) | MIT (open) |
| Directly commercialize the protocol? | No | No |
| How they benefit | Claude API revenue grows as MCP drives more Claude usage | MAK4I Registry revenue grows as protocol adoption grows |
| What's paid | Claude API + Claude.ai subscriptions | Hosted Registry, Enterprise, Cloud API |
| Model-dependent? | Yes — MCP benefits Anthropic mainly when Claude is used | No — MAK4I earns revenue regardless of which AI model is used |
| Governance | Linux Foundation (Anthropic donated MCP to the Agentic AI Foundation, Dec 2025) | Talvik owned (community steering committee planned) |

### The Key Difference

```
Anthropic with MCP:
  MCP makes Claude more useful
  Anthropic earns money from Claude — not from MCP
  If someone uses MCP with a different model instead of Claude
  → Anthropic gets nothing from that usage

Talvik with MAK4I:
  MAK4I is model-agnostic by design
  Talvik earns money from the Registry — not from any AI model
  If someone uses MAK4I with a different model instead of Claude
  → Talvik still earns Registry revenue

This makes Talvik's model more durable than Anthropic's MCP model.
MAK4I captures value from the memory layer
regardless of which AI model sits on top.
```

---

## The Closer Parallel — Git and GitHub

```
Git (protocol):
  Linus Torvalds created it
  Open source, free forever
  Linux Foundation governs it
  No direct commercialization of Git itself

GitHub (platform):
  Microsoft built the hosted platform on top
  Free for public repos
  Paid for private repos, teams, enterprise
  $7.5B acquisition by Microsoft in 2018

MAK4I (protocol):      Git equivalent
  Talvik created it
  Open source, MIT licensed, free forever
  Talvik governs it (community steering coming)

Talvik Registry (platform):   GitHub equivalent
  Talvik builds the hosted platform on top
  Free community tier
  Paid Pro, Team, Enterprise tiers
  The protocol drives adoption
  The platform captures the value
```

---

## Why Keeping the Protocol Open Is Rational

```
If MAK4I had a paid protocol:
  → Developers avoid it
  → Less adoption
  → Less registry revenue
  → Talvik fails

If MAK4I is free forever:
  → Developers adopt it freely
  → More adoption
  → More registry users
  → More enterprise customers
  → Talvik wins

The protocol being open is not a weakness.
It is the growth engine for the commercial platform.

This is why Git is free and GitHub is worth billions.
This is why Linux is free and Red Hat sold for $34B.
This is why Kubernetes is free and GKE generates
hundreds of millions for Google annually.

MAK4I will follow the same pattern.
```

---

## What Prevents a Fork from Competing?

A legitimate question: if MAK4I is open source,
can someone fork it and build a competing registry?

Yes. And that is fine.

```
A fork of MAK4I has:
  The protocol code ✓

A fork of MAK4I does NOT have:
  The community artifacts ✗
  The production evidence ✗
  The enterprise trust built over time ✗
  The first-mover brand recognition ✗
  The MAK4I Certified conformance ecosystem ✗

GitHub won not because it owned Git
but because it built the best platform,
the largest community, and the most trust.

Talvik wins the same way.
```
