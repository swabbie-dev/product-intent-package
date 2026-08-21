# User flows

Use one subgraph per `FLOW-*`. Include the `SCREEN-*` nodes that the flow
enters, the mockups or components that matter, and alternate, failure,
cancellation, and recovery paths. Treat system work as a black box between the
actor action and visible product response. Link consequential work to `SEQ-*`,
`SM-*`, or `RULE-*`; do not draw service calls, database reads, authorization
checks, or query mechanics here.

```mermaid
flowchart TD
  %% FLOW_001["FLOW-001 Example flow"] --> SCREEN_001["SCREEN-001 Example screen"]
  %% SCREEN_001 -.->|design reference| MOCK_001["MOCK-001 Approved mockup"]
  %% SCREEN_001 --> CAP_001["CAP-001 Product capability"]
```
