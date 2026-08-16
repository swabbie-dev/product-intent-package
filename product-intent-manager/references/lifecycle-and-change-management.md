# Product Intent Lifecycle and Change Management

## Operating modes

### Create

Use the greenfield workflow to build a package from an idea.

### Complete

For an existing package:

1. validate structure;
2. inventory all active, missing, stale, proposed, and blocked artifacts;
3. verify authority assignments and target baseline;
4. audit all twelve structures and coverage lenses;
5. generate an authority-routed decision queue;
6. resolve, update, trace, run draft validation, stamp the content hash, approve that hash, and run final validation.

Do not trust an existing `build_ready` label without rerunning validation and checking its approval/version.

### Iterate

For every requested change:

1. capture the request as evidence, not immediate canonical intent;
2. identify decision domain and accountable authority;
3. define the changed observable outcome and target version;
4. obtain confirmation or valid delegation;
5. record a new `DEC-*` and superseded decisions;
6. run impact analysis;
7. mark all affected active artifacts stale;
8. update each affected structure;
9. update acceptance and traceability;
10. reconfirm cross-domain consequences;
11. run draft validation, stamp the content hash, obtain approval for that hash, run final validation, and issue the new package version.

Use:

```bash
python scripts/impact_analysis.py <package-directory> <CHANGED-ID> [<CHANGED-ID> ...] --reverse
```

The script reports candidates; the agent must review semantic effects that graph links may not capture.

## Change classes

| Class | Examples | Minimum review |
|---|---|---|
| editorial | label or rationale with no semantic change | artifact owner; verify ID links unchanged |
| presentation | visual styling within confirmed design bounds | design authority; accessibility and regression review |
| behavioral | flow, rule, state, permission, notification, copy with legal meaning | product/domain/design; acceptance update |
| data | schema, retention, deletion, migration, export | product/domain/technical/privacy; migration and recovery update |
| contract | API/event/integration shape or semantics | technical and affected product authorities; compatibility update |
| architectural | responsibility, trust, deployment, storage, async boundary | technical/security/operations; sequences and quality update |
| scope | capability added, removed, deferred, or reprioritized | product/release authority; full traceability impact |
| quality | SLO, security, accessibility, compatibility, cost ceiling | product tradeoff owner plus technical/operations authority |

## Staleness

Any artifact affected by a changed decision becomes `stale: true` until reviewed. Do not merely update the obvious file.

Typical propagation:

```text
Capability or rule change
  -> domain/flow/screen/state
  -> data/architecture/contracts/sequences
  -> quality constraints
  -> acceptance scenarios
  -> traceability and handoff readiness
```

A stale artifact cannot be part of a build-ready graph.

## Versioning

- Increment package version for every approved change set.
- Record target product version separately from package version.
- Preserve superseded decisions and artifacts in history.
- Record changed IDs, reason, authority, decision, and affected IDs in `governance/change-log.json`.
- Recompute readiness and package hash.

## Drift control

When implementation changes outside the package:

1. capture the implementation change as evidence;
2. determine whether it is a defect, authorized implementation discretion, or undocumented product change;
3. if product intent changed, route it through authority confirmation and package versioning;
4. if implementation drifted, keep package intent unchanged and create a remediation task;
5. never silently rewrite the package to match the code.

## Decision hygiene

- Newer decisions supersede older ones explicitly.
- A proposal never supersedes a confirmed decision.
- Cross-domain consequences require the affected authorities.
- Rejected proposals remain in decision history when useful, but do not pollute active structures.
- “No change” is itself a decision when evidence reveals a conflict.

## Iteration output

Every iteration produces:

- new package version;
- change log;
- impact set;
- stale-to-confirmed review record;
- updated acceptance and traceability;
- validation report;
- final approval for the new target version or a blocked-change report.
