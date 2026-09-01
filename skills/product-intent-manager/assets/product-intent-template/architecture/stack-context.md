# Stack context

Show the physical product boundary, actors, external systems, deployable
services, owned state, and consequential connections. This view owns runtime
placement and responsibility. Include deployment here unless its topology is
too complex to remain readable.

Do not show screen navigation, message order, entity fields, or detailed state
transitions.

```mermaid
flowchart LR
  %% Add only the physical participants in the current intended product.
  %% Label each node with its ARCH-* ID when cross-referenced, runtime or
  %% provider, responsibilities, and owned state. Label each edge with direction
  %% and interaction meaning.
```

## Current rationale

- State each active reason needed to understand the physical boundaries,
  responsibility placement, provider choice, or deployment shape.
- Use cause-and-effect language and material tradeoffs. Do not recount former
  designs, superseded decisions, dates, or product history.
