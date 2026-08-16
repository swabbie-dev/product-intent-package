# Component boundaries

Each component owns one responsibility in the proposed graph. No component may
write canonical intent through a view adapter without the graph service rules.

```mermaid
flowchart TB
  NAV["Artifact navigation"] --> RESOLVER["Stable-ID resolver"]
  BOARD["Experience board adapter"] --> RESOLVER
  CANVAS["Semantic canvas adapter"] --> RESOLVER
  RECORD["Structured record adapter"] --> RESOLVER
  TABLE["Data table adapter"] --> RESOLVER
  TASKS["Task overlay adapter"] --> RESOLVER
  RESOLVER --> GRAPH["ARCH-003 Canonical graph service"]
  VALIDATOR["Package validator"] --> GRAPH
  APPROVAL["Approval gate"] --> GRAPH
  CHAT["Agent context and chat"] --> APPROVAL
  ADAPTERS["ARCH-006 Integration adapter boundary"] --> GRAPH
  AUDIT["Audit writer"] --> GRAPH
```

The descriptive subcomponent labels stay inside the registered `ARCH-003`,
`ARCH-004`, and `ARCH-005` boundaries.
