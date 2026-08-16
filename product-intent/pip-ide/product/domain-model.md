# Domain model

These are conceptual records. The physical schema is a proposed mapping in the
data structure. A stable ID is immutable. A view can change its layout without
changing the package artifact it represents.

```mermaid
classDiagram
  class DOM_001["DOM-001 Product Intent Package"]
  class DOM_002["DOM-002 Artifact"]
  class DOM_003["DOM-003 Stable ID"]
  class DOM_004["DOM-004 View"]
  class DOM_005["DOM-005 Proposal"]
  class DOM_006["DOM-006 Decision"]
  class DOM_007["DOM-007 Task"]
  class DOM_008["DOM-008 Evidence"]
  class DOM_009["DOM-009 Authority"]
  class DOM_010["DOM-010 Workspace"]
  DOM_010 "1" --> "1..*" DOM_001 : contains
  DOM_001 "1" --> "1..*" DOM_002 : indexes
  DOM_002 "1" --> "1" DOM_003 : identified_by
  DOM_001 "1" --> "1..*" DOM_004 : rendered_as
  DOM_005 "1" --> "1..*" DOM_002 : changes
  DOM_005 "0..*" --> "0..1" DOM_006 : approved_by
  DOM_007 "0..*" --> "0..*" DOM_002 : links_to
  DOM_002 "0..*" --> "0..*" DOM_008 : supported_by
  DOM_006 "1" --> "1" DOM_009 : confirmed_by
  DOM_010 "1" --> "1..*" DOM_009 : grants_access_to
```

Invariants:

- `DOM-001` has one active package version per workspace and target version.
- `DOM-002` keeps its `DOM-003` stable ID across view changes.
- `DOM-005` cannot mutate `DOM-001` until `DOM-006` records the required human approval.
- `DOM-007` may link to an artifact, but task state does not alter that artifact.
- `DOM-008` can explain a proposal. Evidence alone cannot confirm intent.
