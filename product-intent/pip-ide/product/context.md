# Product map

The PIP IDE is the product boundary. The package graph is canonical. External
systems provide optional evidence or execution links. They do not become
canonical intent without a confirmed decision.

```mermaid
flowchart LR
  ACTOR_001["ACTOR-001 PIP originator"] --> CAP_001["CAP-001 Author and evolve"]
  ACTOR_002["ACTOR-002 Collaborator and reader"] --> CAP_002["CAP-002 Interpret and navigate"]
  ACTOR_001 --> CAP_003["CAP-003 Work with a product agent"]
  ACTOR_004["ACTOR-004 Implementation contributor"] --> CAP_004["CAP-004 Manage implementation tasks"]
  ACTOR_003["ACTOR-003 Product agent"] --> CAP_003
  CAP_001 --> PRODUCT["PIP IDE\ncanonical PIP graph"]
  CAP_002 --> PRODUCT
  CAP_003 --> PRODUCT
  CAP_004 --> PRODUCT
  PRODUCT --> FIGMA["Figma experience source"]
  PRODUCT --> MIRO["Miro semantic canvas source"]
  PRODUCT --> SHEETS["Google Sheet working source"]
  PRODUCT --> LINEAR["Linear task project"]
  PRODUCT --> GITHUB["GitHub monorepo"]
```

The current draft does not define account creation, billing, or hosted
collaboration. Those choices remain in the question ledger.
