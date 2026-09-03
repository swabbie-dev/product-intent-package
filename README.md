# Product Intent Package

This repository contains two outward-facing product-management Agent Skills and
the Product Intent Package (PIP) format maintained by one of them.

## Agent skills

[`skills/product-management/`](skills/product-management/) provides concise,
framework-neutral product leadership for shaping plans, reviewing features,
closing material gaps, and asking useful questions of ideators, developers,
customers, and users.

[`skills/product-intent-manager/`](skills/product-intent-manager/) helps a
product agent create, reconstruct, review, simplify, or update a PIP, and helps
an implementer or auditor preserve its current intent when work is explicitly
governed by one. Reconstruction is a mode of the same skill.

The Product Intent skill contains:

- `SKILL.md`, the concise entrypoint;
- `references/`, guidance loaded only when relevant;
- `assets/product-intent-template/`, the three-file default package;
- `assets/acceptance-template.yaml`, optional detailed acceptance;
- `assets/governance-template.yaml`, optional current editing authority;
- `assets/example-product-intent-package/`, a proportional worked example; and
- `evals/cases.yaml`, realistic behavior cases.

## Format 7.0

Format 7 treats the canonical PIP as the product's current intended end state.
It contains no package or item status, readiness label, signature, confirmation
record, implementation observation, proposal lane, handoff record, or review
result. Git records ordinary history. Tasks, conversations, evidence,
implementation findings, and audits stay outside the package.

Implementation tickets in Linear, Notion, ClickUp, GitHub, or another task
system link to the applicable PIP release, revision, and records rather than
restating product behavior or acceptance. Tickets contain implementation scope,
code anchors, order, tips, hazards, blockers, progress, and proportional
verification. They may narrow execution but cannot revise the PIP.
Audits may use tickets to locate the requested scope and evidence, but audit
expected behavior and conformance against the canonical PIP—not ticket prose,
status, or checklists.

The default package has three files:

```text
product.yaml
architecture/stack-context.md
experience/user-flows.md
```

Simple acceptance belongs directly on capabilities in `product.yaml`. Add
`acceptance.yaml` only when several scenarios, material failure paths, cross-
capability behavior, or detailed quality outcomes are clearer separately.

If a different product end state needs review, create an isolated PIP fork in a
branch, worktree, or separate proposal location. Make the fork internally
coherent and keep the canonical package unchanged until a requester whose
editing authority covers the complete change adopts it. Do not mix competing
proposals into canonical intent or add proposal statuses to either package.

Add `governance.yaml` when agents or contributors need a durable way to verify
who may request canonical PIP edits. It may grant a product leader `full`
access and give other product leaders or developers `scoped` or
`proposal_only` access. A scoped editor may not apply only part of a semantic
change when required dependent edits fall outside that scope; a full editor
must make the complete coherent change or it remains in an isolated fork.
Governance stores current editing authority only—not decisions, approvals,
signoffs, requirements, rationale, or history. Git records who committed edits.

Add journeys, screen records, rules, state machines, data models, contracts,
sequences, quality constraints, mockups, or a separate deployment view only
when they add distinct product meaning. Format 7 does not require an artifact
index, coverage matrix, central traceability graph, change log, journey
registry, readiness ledger, or a formal not-applicable decision.

An optional `dcl` mapping in `product.yaml` states the product-wide Development
Complexity Level. It applies everywhere unless a narrow owner has a justified
`dcl_override`. Sequence diagrams should show whether they use the product
default or an override. Implementation DCL comparisons stay in audit or task
notes outside the PIP.

DCL does not decide whether rare or complex edge cases deserve automatic
handling. At any DCL, ask the human product authority whether the intended path
is automation, safe manual review or recovery, visible fallback, or exclusion
before expanding the design or implementation.

Each diagram file includes concise current rationale for its non-obvious design
choices. The rationale explains all active causes, constraints, and material
tradeoffs for the present design; it does not retell product history.

The five diagram responsibilities remain distinct:

- stack context: physical systems, responsibility, state ownership, deployment,
  and connections;
- user flow: actor actions, user-visible surfaces, visible outcomes, and
  recovery—the inventory of what needs mockups;
- state machine: valid lifecycle states and high-level process interaction;
- data model/ERD: concepts, persisted records, relationships, and product-
  significant constraints; and
- sequence: detailed ordered runtime logic, input provenance, code reuse,
  retries, fallbacks, and recovery for one consequential process.

State machines and user flows intentionally omit sequence-level detail.
Deployment normally belongs in stack context and becomes separate only when its
topology is too complex to remain readable.

Structured records use YAML (`.yaml`). Mermaid sources use fenced `mermaid`
blocks in Markdown (`.md`), including diagram-only files. Copied external
sources keep their required formats.

See the
[package standard](skills/product-intent-manager/references/product-intent-package-standard.md)
for the authoritative format.
