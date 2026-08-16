# PIP IDE shell mockup

`MOCK-001` is a proposed wireframe for `SCREEN-001` and the first view surfaces.
It is a working model, not a confirmed visual design. The supplied Figma file is
the design source: [IP IDE Experience](https://www.figma.com/design/NMUiwN7LaOsPrsQO3KPP4W/IP-IDE-Experience?node-id=4-17).

```mermaid
flowchart TB
  MOCK_001["MOCK-001 PIP IDE shell"]
  subgraph SHELL["SCREEN-001 Workspace shell"]
    NAV["COMP-002 Artifact navigator"]
    VIEWS["COMP-003 View switcher"]
    CANVAS["SCREEN-002 Experience board\nor SCREEN-003 Semantic canvas"]
    INSPECT["SCREEN-004 Structured record view"]
    CHAT["SCREEN-007 Product-agent chat"]
    STATUS["COMP-008 Validation status"]
  end
  MOCK_001 --> SHELL
  NAV --> VIEWS
  VIEWS --> CANVAS
  VIEWS --> INSPECT
  CHAT --> REVIEW["SCREEN-008 Proposal review\nCOMP-004 + COMP-005"]
  STATUS --> SAVE["FLOW-001 Save or recover"]
  CANVAS --> FLOW_002["FLOW-002 Interpret and navigate"]
  INSPECT --> FLOW_001["FLOW-001 Capture and evolve intent"]
```
