# Stakeholder Reconstruction Interviews

Ask only unresolved questions. Begin from the observed model; do not ask stakeholders to recreate facts the agent can inspect.

## Product originator / owner

Confirm:

- target baseline and version;
- intended users, jobs, outcomes, and success measures;
- release boundary and explicit exclusions;
- capability priorities and product tradeoffs;
- whether observed quirks are defects, accepted behavior, or legacy constraints;
- monetization, entitlement, policy, risk, and acceptance authority;
- domains delegated to PM, design, engineering, legal, or the agent.

## Product manager

For each capability:

- actors, preconditions, trigger, outcome, and completion definition;
- happy, alternate, invalid, permission, cancellation, failure, and recovery paths;
- object states and transitions;
- business rules, priorities, limits, timing, and exceptions;
- notifications, admin/support behavior, analytics, and audit requirements;
- release scope and backward compatibility;
- acceptance examples and edge cases.

Ask explicitly which observed behavior is intentional versus accidental.

## Designer

For each flow/screen/component:

- information hierarchy and navigation;
- all screen states and transitions;
- validation, errors, recovery, confirmation, undo, and destructive actions;
- responsive/device behavior;
- accessibility, keyboard, focus, screen-reader, contrast, and reduced motion;
- design tokens, component variants, content/copy source, and motion;
- discrepancies between mockups and running product;
- which details are approved, proposed, historical, or exploratory.

## Technical lead / architect

Confirm:

- current versus target architecture;
- responsibility and trust boundaries;
- data model, ownership, tenancy, lifecycle, migrations, and privacy classification;
- APIs/events/integrations, versioning, idempotency, errors, retries, and timeouts;
- transactional and async sequences;
- scale, latency, availability, backup, recovery, observability, and operational ownership;
- security controls and known debt;
- which implementation choices are intentionally delegated to the coding orchestrator.

Do not ask engineering to decide product behavior outside its delegated domain.

## Domain, security, privacy, legal, operations

Ask when relevant:

- domain invariants and invalid states;
- regulatory obligations and evidence required;
- threat model, abuse cases, data classification, retention, export, deletion, and audit;
- operational workflows, escalation, incident response, reconciliation, and manual overrides;
- compliance-specific acceptance criteria.

## Conflict interview

When stakeholders disagree:

1. state the exact conflicting claims and evidence IDs;
2. identify the domain authority;
3. explain affected behavior and tradeoff;
4. ask the authority for the target decision;
5. record dissent as context, not competing canonical intent;
6. update and reconfirm cross-domain consequences.
