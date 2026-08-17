# User flows

Use one subgraph per `FLOW-*`. Include the `SCREEN-*` nodes that the flow
enters, the mockups or components that matter, and alternate, failure,
cancellation, and recovery paths.

```mermaid
flowchart TD
  %% FLOW_001["FLOW-001 Example flow"] --> SCREEN_001["SCREEN-001 Example screen"]
  %% SCREEN_001 -.->|design reference| MOCK_001["MOCK-001 Approved mockup"]
  %% SCREEN_001 --> CAP_001["CAP-001 Product capability"]
```
