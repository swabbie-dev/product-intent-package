# User flows

## FLOW-001 Read and increment the counter

The flow takes place on `SCREEN-001 Counter screen`. Increment actions use
`SEQ-001`; initial loads, retries, and unknown-outcome reconciliation use
`SEQ-002`. Visible outcomes obey `RULE-001`.

```mermaid
flowchart TD
  START(["ACTOR-001 opens Counter"])

  subgraph SCREEN_001["SCREEN-001 · Counter screen"]
    LOADING["Show loading"] -->|current value loads| READY["Show current value and Increment"]
    LOADING -->|load fails| LOAD_ERROR["Show load failure and Retry"]
    LOAD_ERROR -->|Retry| LOADING

    READY -->|Press Increment| SUBMITTING["Show increment in progress"]
    SUBMITTING -->|new value confirmed| READY
    SUBMITTING -->|failure confirmed| RETRY["Show unchanged value and Retry"]
    RETRY -->|Retry| SUBMITTING
    RETRY -->|Dismiss| READY
    SUBMITTING -->|outcome unknown| RECONCILE["Show reconciling and prevent another increment"]
    RECONCILE --> LOADING
  end

  START --> LOADING
```

The screen is a responsive, single centered column. Increment is a native,
keyboard-operable button, and loading, ready, error, submitting, and reconciling
state changes are announced to assistive technology. The screen uses no
animation.

The flow owns actor actions and visible outcomes. Runtime calls and commit
behavior belong to the linked sequences and `RULE-001`.
