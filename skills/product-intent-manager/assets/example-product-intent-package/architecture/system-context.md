```mermaid
flowchart LR
  ACTOR_001["ACTOR-001 User"] --> ARCH_001["ARCH-001 Web client"]
  ARCH_001 --> ARCH_002["ARCH-002 Counter API"]
  ARCH_002 --> ARCH_003["ARCH-003 Counter database"]
```
