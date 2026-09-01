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

The flow owns actor actions and visible outcomes. Runtime calls and commit
behavior belong to the linked sequences and `RULE-001`.

## Current rationale

- One responsive, centered screen is sufficient because the product has one
  user goal and no secondary navigation or account surfaces.
- Loading, ready, error, submitting, and reconciling remain visibly distinct
  because each state gives the user different available actions and certainty
  about the persisted value.
- The reconciling state blocks another increment because the prior request may
  already have committed; another request could create an unintended duplicate.
- Retry is offered after a known unchanged result or a failed read because those
  operations are safe to repeat.
- A native keyboard-operable button and announced state changes are necessary
  for assistive-technology use. Animation is unnecessary for understanding the
  state changes.
