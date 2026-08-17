# Reconstruct Product Intent From an Existing Product

Use this workflow when a product exists but its current intent is missing,
incomplete, or inconsistent. Reconstruct the product before you propose major
changes.

## 1. Declare the target

Confirm one target baseline:

- `as_implemented`: reproduce the current product, including accepted quirks;
- `intended_current`: record the product that authorities intend now;
- `target_next`: record the next planned version.

Also confirm the release boundary, source environments, known exclusions, and
accountable authorities. Do not combine different baselines in one active model.

## 2. Inventory evidence

Identify the sources that can show product behavior:

- running products and feature flags;
- product documents, decisions, roadmaps, and tickets;
- research, support cases, analytics, and incident history;
- design boards, prototypes, screenshots, and recordings;
- routes, screens, components, tests, data, APIs, events, and integrations;
- operational procedures, monitoring, release notes, and migrations;
- stakeholder knowledge.

Record the source, version or environment, inspected scope, observed claims,
and limits in `governance/evidence.yaml`. Treat each source as evidence, not as
automatic intent.

## 3. Observe actor experiences

For each in-scope actor and capability:

1. record entry points, preconditions, and starting state;
2. follow the main path and alternate paths;
3. inspect loading, empty, invalid, denied, unavailable, failure, and recovery
   states;
4. inspect responsive, keyboard, accessibility, and account-state behavior;
5. note data changes, external effects, notifications, and background work;
6. record what happens on retry, timeout, cancellation, duplicate action, and
   concurrent action when these cases apply.

Label each finding `observed`. Do not infer an unseen branch from a repeated
pattern.

## 4. Reconstruct the product model

Build the same thirteen structures used for a new product. Start with actors,
scope, capabilities, and lifecycle journeys. Then create detailed flows,
screens, behavior, data, architecture, boundary records, sequence diagrams,
quality constraints, and acceptance scenarios.

Keep four layers separate:

| Layer | Meaning |
|---|---|
| observed | a source directly shows it |
| inferred | evidence suggests it, but no authority confirmed it |
| proposed | a recommended target choice |
| confirmed | the accountable authority approved it |

Use `references/product-artifact-practices.md` for diagram selection and design
board organization. Preserve links from each reconstructed record to its
evidence.

## 5. Find gaps and conflicts

Compare runtime behavior, code, tests, documents, designs, and stakeholder
statements. Record:

- missing branches, states, permissions, and failure behavior;
- different behavior across environments or product surfaces;
- apparent defects that can be accepted behavior or implementation drift;
- dead, hidden, or feature-flagged capabilities;
- competing rules, concepts, data models, and screen designs;
- implicit limits, timing, ordering, retries, and concurrency behavior;
- missing security, privacy, accessibility, operational, and quality choices;
- facts that have no accountable authority.

Create `Q-*` records for gaps and `CON-*` records for conflicts. Group them by
authority and affected capability.

## 6. Resolve intent with authorities

Show the observed model and the exact conflict before you ask a question. Ask
whether the behavior is target intent, a defect, a legacy constraint, a future
proposal, or out of scope.

Route decisions to the correct authority:

- product: users, outcomes, scope, priorities, capabilities, and behavior;
- design: information architecture, screens, states, components, content, and
  accessibility details;
- technical and data: responsibility boundaries, data, interfaces, sequences,
  security, operations, and measurable constraints;
- specialist authorities: legal, privacy, compliance, operations, or domain
  rules.

Record each confirmed choice as `DEC-*`. Do not ask engineering to decide
product behavior unless that domain was explicitly delegated.

## 7. Canonicalize and hand off

Move only confirmed items into active target intent. For each active item:

- assign a stable ID and accountable authority;
- link the confirmation decision and supporting evidence;
- link affected product, experience, behavior, data, technical, quality, and
  acceptance records;
- mark conflicts or old intent as superseded without deleting the evidence;
- keep unresolved items blocked or proposed.

Apply the handoff gates. If a build-affecting question remains, deliver the
package with an authority-routed decision queue and a blocked status. A polished
reconstruction is not confirmed product intent until the authorities approve it.
