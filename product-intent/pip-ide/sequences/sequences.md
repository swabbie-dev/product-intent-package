# Runtime sequences

The sequences are proposed coordination rules. They make graph writes, approval
gates, and integration failures observable.

## Save an author edit

```mermaid
sequenceDiagram
  participant H as Human
  participant V as ARCH-004 View adapter
  participant G as ARCH-003 Graph service
  participant P as Package validator
  participant S as ARCH-007 Storage boundary
  participant O as Audit writer
  H->>V: edit artifact
  V->>G: PATCH with expected graph version
  G->>P: validate YAML and stable IDs
  P-->>G: pass or field errors
  alt validation fails
    G-->>V: validation error; no write
    V-->>H: preserve input and show error
  else validation passes
    G->>S: compare expected graph version
    alt graph conflict
      S-->>G: conflict
      G-->>V: 409 and conflicting records
      V-->>H: merge or cancel choice
    else current version
      G->>S: persist artifact and increment graph version
      G->>O: append audit event
      G-->>V: changed artifact and new version
      V-->>H: refresh linked views
    end
  end
```

## Review and apply an agent proposal

```mermaid
sequenceDiagram
  participant H as Human reviewer
  participant C as ARCH-005 Agent context and chat
  participant G as ARCH-003 Graph service
  participant R as SCREEN-008 Proposal review
  participant A as Approval gate
  participant O as Audit writer
  H->>C: ask for help with package context
  C->>G: read selected stable IDs and evidence
  G-->>C: canonical records
  C->>R: show proposed changes and affected IDs
  H->>R: review proposal
  R->>A: approve, reject, or leave pending
  alt reject or leave pending
    A->>O: record review result
    A-->>R: proposal remains non-canonical
  else approve
    A->>G: apply proposal with decision record
    alt apply fails
      G-->>A: failure
      A->>O: record apply failure
      A-->>R: keep proposal for retry
    else apply succeeds
      G->>O: record changed stable IDs
      G-->>R: refreshed canonical graph
    end
  end
```

## Integration read failure

```mermaid
sequenceDiagram
  participant H as Human
  participant V as ARCH-004 View adapter
  participant I as ARCH-006 Integration adapter
  participant X as External system
  participant G as ARCH-003 Graph service
  H->>V: open linked external source
  V->>I: request source reference
  I->>X: authenticated request
  alt source available
    X-->>I: source data
    I-->>V: source data and capture limits
    V->>G: keep local evidence reference
  else timeout or denied
    X-->>I: failure
    I-->>V: unavailable state and retry option
    V->>G: preserve local package and evidence limit
    V-->>H: show source limitation
  end
```
