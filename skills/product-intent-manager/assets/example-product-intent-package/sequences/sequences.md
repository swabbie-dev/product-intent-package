# Sequences

## SEQ-001 Increment once

This sequence applies `RULE-001` to `DATA-001` during `FLOW-001`.

**DCL:** 4 (product default)

```mermaid
sequenceDiagram
  participant U as ACTOR-001 User
  participant B as ARCH-001 Browser application
  participant S as ARCH-002 Serverless API
  participant D as ARCH-003 Supabase Postgres

  U->>B: Press Increment
  Note over U,B: trigger <- user action on SCREEN-001
  B->>S: API-001 Request one increment
  Note over B,S: increment amount <- product constant 1
  S->>D: Attempt atomic DATA-001 increment
  alt Increment is accepted and result arrives
    D-->>S: Committed new value
    S-->>B: New value
    B-->>U: Display new value
  else Failure is confirmed before commit
    D-->>S: No mutation
    S-->>B: Confirmed failure
    B-->>U: Show unchanged value and Retry
  else Client cannot determine the outcome
    Note over S,D: The increment may or may not have committed
    S--xB: No conclusive result
    B-->>U: Show reconciling and prevent another increment
    Note over B,D: Continue with SEQ-002 before accepting another increment
  end
```

### Current rationale

- The API requests one atomic database increment because a client-side read-
  then-write could lose concurrent accepted increments.
- A failure known to occur before commit may offer Retry because the value is
  known to be unchanged.
- An unknown outcome does not automatically retry because the first request may
  already have committed; `SEQ-002` must re-read durable state before another
  increment is allowed.

## SEQ-002 Load or reconcile the current value

This sequence reads `DATA-001` for initial load, read retry, or reconciliation
during `FLOW-001`.

**DCL:** 4 (product default)

```mermaid
sequenceDiagram
  participant U as ACTOR-001 User
  participant B as ARCH-001 Browser application
  participant S as ARCH-002 Serverless API
  participant D as ARCH-003 Supabase Postgres

  U->>B: Open Counter or choose Retry
  Note over U,B: trigger <- user action on SCREEN-001
  Note over B,D: trigger may also be unknown outcome returned by SEQ-001
  B->>S: API-002 Request current value
  S->>D: Read DATA-001
  alt Read succeeds
    D-->>S: Current persisted value
    S-->>B: Current persisted value
    B-->>U: Display value and allow Increment
  else Read fails
    D-->>S: Read failure
    S-->>B: Confirmed failure
    B-->>U: Show Retry and keep Increment unavailable
  end
```

### Current rationale

- Initial load, read retry, and unknown-outcome reconciliation use the same read
  process because each needs the current durable value without mutation.
- Increment remains unavailable after a read failure because the browser cannot
  safely present or mutate a value it has not reconciled with `DATA-001`.
