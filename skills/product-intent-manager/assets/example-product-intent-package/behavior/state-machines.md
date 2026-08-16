```mermaid
stateDiagram-v2
  state "SM-001 Counter interaction" as SM_001 {
    [*] --> Ready
    Ready --> Submitting: increment
    Submitting --> Ready: success
    Submitting --> Error: failure
    Error --> Submitting: retry
    Error --> Ready: dismiss
  }
```
