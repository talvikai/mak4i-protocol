# MAK4I and MCP

*This is the overview of how MAK4I relates to the Model Context Protocol;
the normative binding is [MAK-0008](standards/MAK-0008.md). [README.md](README.md), [VISION.md](VISION.md),
and [ARCHITECTURE.md](ARCHITECTURE.md) reference this document rather than
repeating the explanation.*

---

## Is MAK4I Competing with MCP?

No. They solve different problems, at different layers.

```
MCP defines:    How AI models connect to external tools and data
                (the transport and communication layer)

MAK4I defines:  How reusable AI context is represented, governed,
                versioned, discovered and reused
                (the artifact and interoperability layer)

They work together:
  MAK4I → exposed as an MCP server
  AI clients connect to MAK4I via MCP
  MAK4I artifacts flow through MCP to the AI

MCP without MAK4I:  a connection with no reusable artifact model or
                    reuse discipline on top of it
MAK4I without MCP:  governed knowledge with no standard way to reach
                    every AI client (the CLI works locally; a REST API
                    and other bindings are future scope)
Together:           reusable, governed AI context delivered to any
                    MCP-capable client
```

**The USB-C analogy:**

```
MCP   = the USB-C standard (how devices connect)
MAK4I = how the work being transferred is represented, so it's
        reusable on arrival — not just delivered

You need both.
MCP without MAK4I: a connection with no shared model for what's reused
                   on the other end
MAK4I without MCP: an artifact model with no standard way to deliver it
                   to every connected tool
```

## How MAK4I binds to MCP

The binding is normative: [MAK-0008](standards/MAK-0008.md) defines:
- the transports (stdio, Streamable HTTP);
- authentication: bearer credentials, and an OAuth 2.1 authorization
  service pinned to the MCP 2025-11-25 authorization revision;
- the tool catalog (`mak4i_whoami` … `mak4i_resolve_conflict`);
- the error model;
- the client requirements (§13) that SDKs and agents follow.

The reference implementation is reachable through MCP today. Native
registry-level MCP, so any MCP-compatible tool reaches a hosted MAK4I
registry without extra integration, is approved future scope
([ROADMAP.md](ROADMAP.md#approved-future-protocol-scope)).

The business rationale for keeping the protocol open is background
material: [docs/background/OPEN_PROTOCOL_STRATEGY.md](docs/background/OPEN_PROTOCOL_STRATEGY.md).


---
