# MAK4I Conformance

**Status:** Draft  
**Version:** 0.1  
**Created:** July 2026  

---

## What is MAK4I Certified?

An implementation is **MAK4I Certified** when it fully conforms
to the MAK4I protocol specification and passes the
MAK4I Conformance Test Suite.

```
MAK4I Certified ✓
```

This badge signals that an artifact, SDK, registry, or client
correctly implements the MAK4I protocol.

Similar to:
- OpenAPI → Swagger Validator
- Kubernetes → CNCF Conformance Tests
- HTTP → W3C validation

---

## Certification Levels

| Level | What is certified | Requirements |
|-------|------------------|-------------|
| **Artifact** | A single memory artifact | Passes MAK-0001 schema validation |
| **SDK** | A language SDK | Implements inject, publish, list, sync |
| **Registry** | A MAK4I registry | Implements Registry API (MAK-0007) |
| **Client** | A MAK4I client | Implements full injection flow (MAK-0002) |

---

## Conformance Test Suite

> Status: Planned for Phase 2 (October 2026)

The MAK4I Conformance Test Suite will include:

### Artifact Tests
- [ ] Schema validation (MAK-0001)
- [ ] Required fields present
- [ ] Version format valid (semver)
- [ ] Type enum valid
- [ ] ID format valid

### Injection Tests
- [ ] Artifact loads correctly
- [ ] Dependencies resolved
- [ ] Context assembled correctly
- [ ] Injected into AI session successfully

### Registry Tests
- [ ] Artifact publish
- [ ] Artifact fetch by ID
- [ ] Artifact version resolution
- [ ] Access control enforcement

---

## How to Get Certified

> Process to be defined in Phase 3 (December 2026)

1. Implement the MAK4I protocol
2. Run the conformance test suite against your implementation
3. Submit results via GitHub PR
4. Receive MAK4I Certified badge

---

## Reference Implementation

The Talvik reference implementation will serve as the
canonical conformance baseline.

Repository: [github.com/talvikai/mak4i-protocol](https://github.com/talvikai/mak4i-protocol)

---

*© 2026 Talvik, Inc.*
