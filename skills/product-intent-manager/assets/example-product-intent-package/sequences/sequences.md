# Sequences

## SEQ-001 Increment once

This sequence applies `RULE-001` to `DATA-001` during `FLOW-001`.

```mermaid
sequenceDiagram
  participant U as ACTOR-001 User
  participant B as ARCH-001 Browser application
  participant S as ARCH-002 Serverless API
  participant D as ARCH-003 Supabase Postgres

  U->>B: Press Increment
  B->>S: API-001 Request one increment
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

## SEQ-002 Load or reconcile the current value

This sequence reads `DATA-001` for initial load, read retry, or reconciliation
during `FLOW-001`.

```mermaid
sequenceDiagram
  participant U as ACTOR-001 User
  participant B as ARCH-001 Browser application
  participant S as ARCH-002 Serverless API
  participant D as ARCH-003 Supabase Postgres

  U->>B: Open Counter or choose Retry
  Note over B,D: Also used automatically after an unknown increment outcome
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
