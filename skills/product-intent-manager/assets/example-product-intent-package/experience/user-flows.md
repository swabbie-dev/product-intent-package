# User flows

## FLOW-001 Read and increment the counter

The flow takes place on `SCREEN-001 Counter screen`. Increment actions use
`SEQ-001`; initial loads, retries, and unknown-outcome reconciliation use
`SEQ-002`. Visible outcomes obey `RULE-001`.

```mermaid
flowchart TD
  START(["ACTOR-001 opens Counter"]) --> LOADING["Show loading"]
  LOADING --> LOAD_RESULT{"Visible load result"}
  LOAD_RESULT -->|current value| READY["Show current value and Increment"]
  LOAD_RESULT -->|failed| LOAD_ERROR["Show load failure and Retry"]
  LOAD_ERROR -->|Retry| LOADING

  READY -->|Press Increment| SUBMITTING["Show increment in progress"]
  SUBMITTING --> RESULT{"Visible increment result"}
  RESULT -->|new value| READY
  RESULT -->|confirmed failure| RETRY["Show unchanged value and Retry"]
  RETRY -->|Retry| SUBMITTING
  RETRY -->|Dismiss| READY
  RESULT -->|outcome unknown| RECONCILE["Show reconciling and prevent another increment"]
  RECONCILE --> LOADING
```

The screen is a responsive, single centered column. Increment is a native,
keyboard-operable button, and loading, ready, error, submitting, and reconciling
state changes are announced to assistive technology. The screen uses no
animation.

The flow owns actor actions and visible outcomes. Runtime calls and commit
behavior belong to the linked sequences and `RULE-001`.
