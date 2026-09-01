# State machines

## SM-001 Counter lifecycle

```mermaid
stateDiagram-v2
  [*] --> Open: Seed below the fixed target
  Open --> Complete: SEQ-001 commits the increment that reaches the target

  note right of Open
    Accepted increments below the target remain Open.
    Their request, replay, and recovery logic belongs to SEQ-001 and SEQ-002.
  end note

  note right of Complete
    Complete is terminal because target changes and reset are excluded.
  end note
```

## Current rationale

- `Open` and `Complete` are separate durable states because they allow different
  product actions: Open permits Increment, while Complete does not.
- Increments below the target are intentionally absent as self-loops because
  they do not change the stable lifecycle state; `SEQ-001` owns their detailed
  request, transaction, replay, and failure logic.
- Completion is terminal because changing or resetting the fixed target is
  outside this release.
