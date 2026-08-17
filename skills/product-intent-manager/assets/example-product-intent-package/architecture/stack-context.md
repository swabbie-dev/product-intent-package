# Stack context

The Counter product is delivered as one simple production topology, so
deployment is shown in this context. A separate deployment diagram is not
needed.

```mermaid
flowchart LR
  ACTOR_001["ACTOR-001 User"] --> PIP_COUNTER["PIP-COUNTER Counter product"]

  subgraph ARCH_004["ARCH-004 Production environment"]
    ARCH_001["ARCH-001 Browser web client<br/>Delivered by Vercel<br/>Load, render, and submit counter changes<br/>Own ephemeral interaction state"]
    ARCH_002["ARCH-002 Vercel serverless API<br/>Execute API-001 and API-002<br/>Own request processing"]
    ARCH_003[("ARCH-003 Supabase Postgres<br/>Own DATA-001<br/>Commit atomic counter transitions")]
  end

  PIP_COUNTER -->|provides CAP-001| ARCH_001
  ARCH_001 -->|synchronous HTTPS application/json API-001 and API-002| ARCH_002
  ARCH_002 -->|synchronous transactional SQL| ARCH_003
```

`ARCH-004` contains the confirmed production deployment boundary. Vercel
delivers the web client and runs the serverless API. Supabase Postgres owns the
durable counter record and commits atomic transitions. Security and operational
controls apply to the relevant node or connection; they are not separate peer
services.
