# User flows

Show actor actions, choices, navigation, and visible product outcomes. Use one
focused flow per actor goal, including consequential failure and recovery
paths. This view owns the user-visible path, not internal execution.

Link system work to its `SEQ-*`, `SM-*`, or rule record. Do not draw service
calls, database reads, authorization checks, or query mechanics here.

```mermaid
flowchart TD
  %% Label the flow with its FLOW-* ID. Use ACTOR-* and SCREEN-* IDs where
  %% In reconstruction, label non-confirmed claims with status and source.
  %% applicable, and keep each node phrased as an actor action, decision, or
  %% visible product response.
```
