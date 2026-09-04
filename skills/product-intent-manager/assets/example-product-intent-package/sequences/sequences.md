# Sequences

## SEQ-001 Increment once

This sequence applies `RULE-001` to `DATA-001` and `DATA-002` during
`FLOW-001`.

**DCL:** 4 (product default)

```mermaid
sequenceDiagram
  participant U as ACTOR-001 User
  participant B as ARCH-001 Browser application
  participant S as ARCH-002 Serverless API
  participant D as ARCH-003 Supabase Postgres

  U->>B: Press Increment or Retry
  Note over U,B: trigger <- user action on SCREEN-001
  alt New action or retry after a confirmed precommit failure
    B->>B: Generate and retain request_key for this attempt
    Note over B: request_key <- browser-generated UUID
  else Retry after reconciliation confirmed no receipt
    Note over B: request_key <- retained input from the original SEQ-001 attempt
  end
  Note over B: increment amount <- product constant 1
  B->>S: API-001 Increment(request_key)
  S->>D: Begin short transaction and find the increment receipt
  Note right of D: READ · DATA-002 counter_increment_receipt<br/>ACCESS · [U1] counter_increment_request_key<br/>INPUT · request_key <- API-001 parameter
  alt Receipt already exists
    D-->>S: Recorded value_after and state_after
    S-->>B: Return recorded result without mutation
    B-->>U: Display recorded progress or completion
  else Request key is new and counter is open
    S->>D: Atomically increment, complete at target, and record the receipt
    Note right of D: READ/UPDATE · DATA-001 counter<br/>KEY · id <- COUNTER_ID product constant<br/>INSERT · DATA-002 counter_increment_receipt<br/>CONSTRAINT · [U1] request_key uniqueness
    D-->>S: Commit value_after and state_after
    S-->>B: Return committed result
    B-->>U: Display progress or Target reached
  else Counter is already complete
    D-->>S: No mutation
    S-->>B: Return complete counter
    B-->>U: Show Target reached without Increment
  else Failure is confirmed before commit
    D-->>S: Roll back without receipt or counter change
    S-->>B: Confirmed failure
    B-->>U: Show unchanged value and Retry
  else Client cannot determine the outcome
    Note over S,D: The transaction may or may not have committed
    S--xB: No conclusive result
    B-->>U: Show reconciling and prevent a new request
    Note over B,D: Continue with SEQ-002 using the same request_key
  end
```

### Current rationale

- The browser creates one request key for a new action and retains it through
  reconciliation because a network failure must not turn uncertainty into a
  second product action. When reconciliation finds no receipt, Retry uses the
  original key; a known precommit failure may start a new attempt with a new key.
- The API checks `[U1]` before mutation and returns an existing receipt because
  replaying a recorded request is a read, not another increment.
- The counter update, completion transition, and receipt insert share one short
  transaction because partial commit would make progress, state, and replay
  protection disagree.
- A failure known to occur before commit may offer Retry because the value and
  receipt are known to be unchanged.
- An unknown outcome does not create a new request because the first transaction
  may already have committed; `SEQ-002` reconciles the original key.

## SEQ-002 Load or reconcile progress

This sequence loads `DATA-001` initially and resolves an unknown `SEQ-001`
outcome through `DATA-002` during `FLOW-001`.

**DCL:** 4 (product default)

```mermaid
sequenceDiagram
  participant U as ACTOR-001 User
  participant B as ARCH-001 Browser application
  participant S as ARCH-002 Serverless API
  participant D as ARCH-003 Supabase Postgres

  alt Initial load or read retry
    U->>B: Open Counter or choose Retry
    Note over U,B: trigger <- user action on SCREEN-001
    B->>S: API-002 Current progress
    S->>D: Read current value, target, and state
    Note right of D: READ · DATA-001 counter<br/>KEY · id <- COUNTER_ID product constant
  else Unknown increment outcome
    Note over B: request_key <- retained input from SEQ-001
    B->>S: API-002 Reconcile(request_key)
    S->>D: Find the original increment receipt
    Note right of D: READ · DATA-002 counter_increment_receipt<br/>ACCESS · [U1] counter_increment_request_key<br/>INPUT · request_key <- retained SEQ-001 value
  end
  alt Current progress or receipt is found
    D-->>S: Persisted progress and state
    S-->>B: Persisted progress and state
    B-->>U: Display progress or Target reached
  else Receipt is not found after the unknown outcome
    D-->>S: No recorded request
    S-->>B: Confirmed not applied
    B-->>U: Show unchanged progress and Retry
    Note over B: Retry uses the retained request_key
  else Read fails
    D-->>S: Read failure
    S-->>B: Confirmed failure
    B-->>U: Show Retry and keep Increment unavailable
  end
```

### Current rationale

- Initial load and reconciliation share one read process because each must
  return authoritative progress without creating a new product action.
- Reconciliation looks up the original request receipt rather than inferring
  success from the latest counter value because other users may have advanced
  the counter afterward.
- A missing receipt permits Retry only with the retained request key because a
  concurrent original transaction and its retry must still resolve to one
  `[U1]` receipt.
- Increment remains unavailable after a read failure because the browser cannot
  safely present or mutate progress it has not reconciled.
