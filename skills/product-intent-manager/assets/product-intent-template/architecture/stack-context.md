# Stack context

Show the product in the context of its actors, external systems, physical
services, deployment environments, and consequential dependencies. For a
simple product, include deployment in this diagram. Add a separate
`architecture/deployment.md` only when deployment topology is too complex to
read in this context.

```mermaid
flowchart LR
  %% ACTOR_001["ACTOR-001 User"] --> PRODUCT["Product boundary"]
  %% PRODUCT --> ARCH_001["ARCH-001 Web application\nProvider or runtime\nResponsibilities\nOwned state"]
  %% ARCH_001 --> ARCH_002["ARCH-002 Worker or API\nProvider or runtime\nResponsibilities\nOwned state"]
  %% ARCH_002 --> ARCH_003[("ARCH-003 Data store\nProvider or runtime\nOwns DATA-001")]
  %% Label every connection with direction, protocol or transport, data or message meaning, and sync or async mode.
  %% Put security controls on the applicable node, connection, or trust zone.
```

Use confirmed provider or runtime facts. Mark unknown placement proposed or
blocked, or link a confirmed bounded-discretion record. Keep logical `API-*`,
`EVT-*`, `DATA-*`, and capability records in their registries; reference them
from relevant nodes and edges instead of drawing them as peer services.
