# JOURNEY-001: Increment and observe the counter

| Journey ID | Type | Actor | Scope | Target view | Intent status | Status | Trigger | Outcome | Recurrence | Authority | Decision | Version |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `JOURNEY-001` | `job_task` | `ACTOR-001` | Counter task | `intended_current` | `confirmed` | `confirmed` | Open Counter screen | Increase and observe value | Repeat until complete | `AUTH-OWNER` | `DEC-006` | 2 |

The actor can repeat the task or leave after an accepted increment. `JOURNEY-001` is the macro map; detailed behavior remains in the linked artifacts.

```mermaid
flowchart LR
  P1["JOURNEY-001.phase-01 Begin task"] --> P2["JOURNEY-001.phase-02 Increment"]
  P2 -->|success| P3["JOURNEY-001.phase-03 Observe result"]
  P2 -->|failure| P3
  P3 -->|repeat| P2
  P3 -->|leave| P4["JOURNEY-001.phase-04 Repeat or exit"]
```

| Phase | Actor goal | Actor action | Product response | State/data | Exceptions and recovery | Linked artifacts |
| --- | --- | --- | --- | --- | --- | --- |
| Begin task | See the current value | Open the Counter screen | Read and display the persisted value | `SM-001`, `DATA-001`, `API-002` | `[DECISION]` Show retry when load fails | `FLOW-001`, `SCREEN-001`, `SEQ-002`, `ACC-004` |
| Increment | Request one increment | Press the control once | Send one request and show submitting | `SM-001`, `API-001` | `[DECISION]` Retry a confirmed pre-commit failure; reconcile an unknown outcome | `RULE-001`, `SEQ-001`, `ACC-002`, `ACC-005` |
| Observe result | Confirm the change | Read the value | Display the committed or reconciled value | `DATA-001`, `SM-001`, `API-002` | `[DECISION]` Reconcile, retry safely, or leave | `FLOW-001`, `RULE-001`, `SEQ-002`, `ACC-001`, `ACC-005` |
| Repeat or exit | Repeat or stop safely | Press again or leave | Start the next cycle or end with no extra mutation | `DATA-001`, `SM-001` | `[DECISION]` Leaving ends the task without a request | `FLOW-001`, `ACC-001` |

Evidence: `[EVIDENCE]` The fixture defines one actor, one Counter screen, one
increment capability, and one persisted counter value. Authority: `[DECISION]`
`DEC-001` confirms the core task. `DEC-006` confirms load, placement, and
unknown-outcome recovery.
