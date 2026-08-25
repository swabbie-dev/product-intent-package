# User flows

Show actor actions, choices, navigation, and visible product outcomes. Use one
focused flow per actor goal, including consequential failure and recovery
paths. This view owns the user-visible path, not internal execution.

Link system work to its `SEQ-*`, `SM-*`, or rule record. Do not draw service
calls, database reads, authorization checks, or query mechanics here.

Visually group actions and states by consequential user-visible surface. Label
each boundary with `SURFACE · Name`, or `SCREEN-* · Name` when another artifact
references it. These boundaries form the mockup inventory; individual flow
nodes do not each require a mockup. A project may consistently distinguish
surface types with labels such as `VIEW`, `COMPONENT`, `DIALOG`, and `EXTERNAL`.

For each surface governed by an authority-confirmed mockup, add the exact frame
or node, version or branch when available, intent status, and any companion
example or export-code reference. The confirmed mockup is the implementation
target, not a visual attachment. Do not add, remove, merge, split, or materially
alter its views, components, or states without accountable product or design
approval. Keep unconfirmed mockups labeled as evidence or proposals.

Use labeled edges for navigation choices and visible permission, availability,
or validation outcomes. Use a diamond only for a question visibly presented to
the actor. When several conditions route to different surfaces, use one compact
rectangular condition node. Keep runtime selection logic in a rule, decision
table, or sequence.

```mermaid
flowchart TD
  %% Label the flow with its FLOW-* ID. Use ACTOR-* and SCREEN-* IDs where
  %% In reconstruction, label non-confirmed claims with status and source.
  %% applicable, and phrase each node as an actor action or visible product
  %% response. Reserve diamonds for questions visibly presented to the actor.
  %% Use labeled subgraphs to bound user-visible surfaces and their states.
```
