# User flows

## FLOW-001 Read and increment the counter

The flow takes place on `SCREEN-001 Counter screen`. Increment actions use
`SEQ-001`; initial loads, retries, and unknown-outcome reconciliation use
`SEQ-002`. Visible outcomes obey `RULE-001`.

**Exact local design target:**
[`SCREEN-001 Counter screen`](mockups/screen-001-counter.md#screen-001-counter-screen)

```mermaid
flowchart TD
  START(["ACTOR-001 opens Counter"])

  subgraph SCREEN_001["SCREEN-001 · Counter screen"]
    LOADING["Show loading"] -->|open progress loads| READY["Show current value, target, and Increment"]
    LOADING -->|completed progress loads| COMPLETE["Show target reached without Increment"]
    LOADING -->|load fails| LOAD_ERROR["Show load failure and Retry"]
    LOAD_ERROR -->|Retry| LOADING

    READY -->|Press Increment| SUBMITTING["Show increment in progress"]
    SUBMITTING -->|progress confirmed below target| READY
    SUBMITTING -->|target reached| COMPLETE
    SUBMITTING -->|failure confirmed| RETRY["Show unchanged value and Retry"]
    RETRY -->|Retry| SUBMITTING
    RETRY -->|Dismiss| READY
    SUBMITTING -->|outcome unknown| RECONCILE["Show reconciling and prevent another increment"]
    RECONCILE -->|progress reconciled| READY
    RECONCILE -->|completion reconciled| COMPLETE
    RECONCILE -->|not applied or read failed| RETRY
  end

  START --> LOADING
```

The flow owns actor actions and visible outcomes. Runtime calls and commit
behavior belong to the linked sequences and `RULE-001`.

## Current rationale

- One responsive, centered screen is sufficient because the product has one
  user goal and no secondary navigation or account surfaces. Its exact local
  target is linked above so the surface inventory is not mistaken for layout.
- Loading, ready, error, submitting, and reconciling remain visibly distinct
  because each state gives the user different available actions and certainty
  about the persisted value.
- The reconciling state blocks another increment because the prior request may
  already have committed; another request could create an unintended duplicate.
- Retry is offered after a known unchanged result or a failed read because those
  operations are safe to repeat.
- Completion removes Increment because the fixed target is the terminal product
  outcome and changing or resetting it is outside this release.
- A native keyboard-operable button and announced state changes are necessary
  for assistive-technology use. Animation is unnecessary for understanding the
  state changes.
