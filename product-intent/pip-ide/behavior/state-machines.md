# Behavior state machines

The state machines below are proposed behavior. They show the required approval
gate and the separation between intent and execution. Exact permissions and
concurrency rules remain open questions.

## Artifact lifecycle

```mermaid
stateDiagram-v2
  [*] --> Draft: create artifact
  Draft --> Proposed: submit for review
  Draft --> Draft: edit while local
  Proposed --> Confirmed: authority approves
  Proposed --> Blocked: missing authority or evidence
  Proposed --> Draft: authority requests changes
  Confirmed --> Superseded: confirmed replacement
  Blocked --> Draft: gap is resolved
  Superseded --> [*]
```

`SM-001` transitions require the following guards:

- Draft to Proposed checks structural validation and stable-ID uniqueness.
- Proposed to Confirmed requires the authority for the affected decision domain
  and a `DEC-*` record.
- Proposed to Blocked records the missing evidence, authority, or question.
- Confirmed to Superseded keeps the old ID in history and points to the new ID.

## Product-agent proposal lifecycle

```mermaid
stateDiagram-v2
  [*] --> Prepared: agent drafts proposal
  Prepared --> PendingApproval: proposal includes affected IDs and evidence
  Prepared --> Invalid: missing required change data
  PendingApproval --> Approved: authorized human approves
  PendingApproval --> Rejected: authorized human rejects
  PendingApproval --> PendingApproval: reviewer leaves pending
  Approved --> Applied: canonical graph write succeeds
  Approved --> ApplyFailed: graph write fails
  ApplyFailed --> PendingApproval: retry after review
  Rejected --> [*]
  Invalid --> [*]
  Applied --> [*]
```

`SM-002` never allows the product agent to move a proposal to `Approved` or
`Applied`. A failed apply keeps the proposal and its affected IDs available for
review.
