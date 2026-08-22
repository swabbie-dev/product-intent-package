# Stack context

`ARCH-001` through `ARCH-004` provide `CAP-001`. `DEC-005` confirms these
physical deployment choices.

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

The browser owns only interaction state. The API owns request processing.
Supabase Postgres is authoritative for the counter value. Production backups
are enabled, and application rollback must preserve `DATA-001`. `SEQ-001` and
`SEQ-002` show the consequential communication among these nodes.
