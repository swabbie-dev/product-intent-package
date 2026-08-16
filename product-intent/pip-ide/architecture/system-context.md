# System context

This context is a proposed boundary for the first product. The application
shell owns the canonical graph. External systems are separate trust zones and
must not be treated as available until their access and integration depth are
confirmed.

```mermaid
flowchart LR
  USER["ACTOR-001 / ACTOR-002\nHuman collaborator"] --> SHELL["ARCH-002\nPurpose-built application shell"]
  AGENT["ACTOR-003\nProduct agent"] --> GATE["ARCH-005\nAgent gateway"]
  SHELL --> GRAPH["ARCH-003\nCanonical graph service"]
  GRAPH --> STORE["ARCH-007\nWorkspace storage boundary"]
  SHELL --> ADAPTERS["ARCH-006\nIntegration adapters"]
  ADAPTERS --> FIGMA["Figma"]
  ADAPTERS --> MIRO["Miro"]
  ADAPTERS --> SHEETS["Google Sheets"]
  ADAPTERS --> LINEAR["Linear"]
  ADAPTERS --> GITHUB["GitHub"]
  SHELL -. proposed telemetry .-> OPS["Quality and operations authority"]
  subgraph TRUST_A["User and application trust zone"]
    SHELL
    GRAPH
    GATE
  end
  subgraph TRUST_B["External integration trust zone"]
    ADAPTERS
    FIGMA
    MIRO
    SHEETS
    LINEAR
    GITHUB
  end
```
