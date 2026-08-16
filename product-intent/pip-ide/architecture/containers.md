# Container model

The container split is proposed. It keeps view rendering separate from graph
mutation and external side effects.

```mermaid
flowchart TB
  SHELL["ARCH-002 Purpose-built shell"]
  GRAPH["ARCH-003 Canonical graph service"]
  VIEW["ARCH-004 View adapters"]
  AGENT["ARCH-005 Product-agent gateway"]
  INTEGRATION["ARCH-006 Integration adapters"]
  STORE["ARCH-007 Workspace storage boundary"]
  SHELL --> VIEW
  VIEW --> GRAPH
  SHELL --> AGENT
  AGENT --> GRAPH
  GRAPH --> STORE
  SHELL --> INTEGRATION
  INTEGRATION --> GRAPH
  VIEW --> INTEGRATION
```

`ARCH-007` is a boundary, not a chosen database. Local versus hosted storage
is an open question.
