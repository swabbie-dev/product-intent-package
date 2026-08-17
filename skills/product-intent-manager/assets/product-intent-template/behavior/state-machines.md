```mermaid
stateDiagram-v2
  %% Define SM-* state machines. Include triggers, guards, side effects, failures, and terminal states.
```

For each state machine that crosses physical services, replace this guidance
with a transition-allocation table:

| Transition | Initiator | Durable authority | Executor | Observers | Failure and recovery |
| --- | --- | --- | --- | --- | --- |
| `SM-*.transition-*` — state A to state B | actor or `ARCH-*` that requests the change | `ARCH-*` and `DATA-*` where the change becomes valid, or `none` for local state | `ARCH-*` that performs the work | actors and services that read or display it | linked `SM-*`, `RULE-*`, `SEQ-*`, or `ACC-*` recovery path |
