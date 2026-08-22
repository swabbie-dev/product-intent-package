# Change and Handoff

## Change discipline

For a material product-intent change:

1. Identify the authoritative fact and the target release.
2. Confirm the changed observable outcome with the accountable authority when
   the request itself is not already an authoritative, unambiguous decision.
3. Follow direct links and review obvious semantic dependents. Mark only items
   that may actually be affected as `stale`.
4. Update the owner first, then affected flows, optional detail, and acceptance.
5. Resolve or expose any contradiction introduced by the change.
6. Reconfirm the affected target scope and update the package status.

Preserve a stable cross-file ID when the meaning is unchanged. If meaning is
split or replaced, retain enough decision context to explain the relationship.
Do not maintain a global dependency graph, per-artifact version counter, or
package hash to automate this judgment.

Use Git for ordinary history. Add a `DEC-*` record only when authority,
rationale, a consequential tradeoff, or supersession must remain visible in the
active package. Do not duplicate every diff in a change log.

## Staleness

`stale` means a prior item should not be relied on until its relationship to a
changed dependency is reviewed. It does not mean every linked artifact must be
rewritten. After review:

- update and reconfirm the item if its meaning changed;
- restore its prior active status if it remains correct; or
- remove or replace it if it no longer belongs in the target.

Keep stale items visible only while they affect current work. Git preserves
superseded ordinary content.

## Four handoff checks

### 1. Scope and authority

Confirm that:

- the target baseline, release boundary, outcome, actors, capabilities,
  exclusions, and measures are understandable and mutually consistent;
- target intent is confirmed by the accountable authority; and
- every unresolved question or conflict that could change the release is either
  resolved or clearly blocks handoff.

Do not require formal disposition of irrelevant possibilities.

### 2. Material behavior and risk

Confirm that the package explains the user-visible and operational behavior
needed for this release, including applicable failure and recovery outcomes,
permissions, meaningful state changes, data relationships, system ownership,
external boundaries, and material quality, security, privacy, compliance, or
operational constraints.

Use optional artifacts where they genuinely clarify these matters. Do not fail
the check because an unnecessary artifact type is absent.

### 3. Acceptance and engineering discretion

Confirm that `acceptance.yaml` contains observable scenarios for the in-scope
capabilities and material constraints. Scenarios should be specific enough to
recognize success or failure without dictating internal construction.

Any unspecified implementation choice remains with engineering by default when
it stays within confirmed behavior and material constraints. Seek another
decision only when a plausible choice could change those outcomes or bounds.

### 4. Consistency and approval

Confirm that:

- remaining direct links resolve and linked artifacts do not contradict their
  owners;
- no `blocked` or `stale` item remains in the approved release scope;
- observed, inferred, and proposed material is not presented as confirmed
  target intent; and
- the accountable product or release authority approves the package target.

Record readiness only in `product.yaml`: set `status: build_ready` and set
`confirmation_decision_id` to the approving decision in `governance.yaml`.
Do not create a separate readiness file or gate ledger.

## Handoff result

Return one of two results:

- **Confirmed handoff:** name the target release, confirmation decision,
  important constraints, optional artifacts used, and remaining engineering
  discretion.
- **Blocked handoff:** name the smallest unresolved questions, their authorities,
  affected outcomes or IDs, and what work can proceed independently.

A package may be useful before it is ready. Do not hide uncertainty to produce
a ready label, and do not delay a ready package because non-observable
engineering decisions remain open.
