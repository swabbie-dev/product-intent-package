# Stack context

`ARCH-001` through `ARCH-004` provide `CAP-001` for Counter 1.0.

```mermaid
flowchart LR
  ACTOR_001["ACTOR-001 User"] -->|reads and increments| ARCH_001
  subgraph ARCH_004["ARCH-004 Production environment"]
    ARCH_001["ARCH-001 Browser application<br/>Delivered by Vercel<br/>Shows value and recovery states"]
    ARCH_002["ARCH-002 Serverless API<br/>Runs on Vercel<br/>Coordinates reads and atomic increments"]
    ARCH_003[("ARCH-003 Supabase Postgres<br/>Owns DATA-001")]
    ARCH_001 -->|API-001 increment / API-002 current value| ARCH_002
    ARCH_002 -->|reads and commits| ARCH_003
  end
```

`SEQ-001` and `SEQ-002` show the consequential communication among these nodes.

## Current rationale

- The browser owns only interaction state because durable state in the client
  would make reload and unknown-outcome recovery unreliable.
- The serverless API owns reads and increments because the browser must not be
  authoritative for validation or mutation of the shared value.
- Supabase Postgres owns `DATA-001` because atomic increments and a durable
  source of truth prevent lost updates and allow reconciliation after a lost
  response.
- Vercel hosts the browser and API so the complete user-facing path can be
  deployed together, while Supabase separately provides durable database state.
- Backups and rollback-safe data handling are necessary because application
  deployment or rollback must not reset the product's persisted counter.
