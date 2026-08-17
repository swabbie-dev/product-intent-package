```mermaid
sequenceDiagram
  participant U as ACTOR-001 User
  participant W as ARCH-001 Web client
  participant A as ARCH-002 Counter API
  participant D as ARCH-003 Database
  Note over U,D: SEQ-001 Increment counter
  U->>W: press increment
  Note over U,W: SM-001 Ready to Submitting; no durable change
  W->>A: API-001 POST /counter/increment
  A->>D: atomic DATA-001 increment
  alt commit succeeds and response arrives
    D-->>A: committed new value
    A-->>W: new value
    W-->>U: SM-001 Submitting to Ready; render value
  else failure before commit
    D-->>A: no mutation
    A-->>W: 503 retry allowed
    W-->>U: SM-001 Submitting to SubmitError; show retry state
  else commit result does not arrive
    D-->>A: committed new value
    A--xW: response is lost or times out
    W-->>U: SM-001 Submitting to UnknownOutcome; block increment
    Note over U,D: Reconcile through SEQ-002; do not resend API-001
  end
```

```mermaid
sequenceDiagram
  participant U as ACTOR-001 User
  participant W as ARCH-001 Web client
  participant A as ARCH-002 Counter API
  participant D as ARCH-003 Database
  Note over U,D: SEQ-002 Load or reconcile counter
  U->>W: open screen or retry load
  W->>A: API-002 GET /counter
  A->>D: read DATA-001 current value
  alt read succeeds
    D-->>A: current value
    A-->>W: current value
    W-->>U: SM-001 Loading to Ready; render value
  else read fails
    D-->>A: read unavailable
    A-->>W: 503 retry allowed
    W-->>U: SM-001 Loading to LoadError; show retry state
  end
```
