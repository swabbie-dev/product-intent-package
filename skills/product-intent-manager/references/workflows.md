# Workflows

Use the workflow that matches the request. In every mode, maintain only the
artifacts needed for this product and keep tasks, analysis, implementation
evidence, and review results outside the PIP.

## Create

1. Copy the three-file template from `assets/product-intent-template/`.
2. In `product.yaml`, set format `7.0.0`, product name, release, outcome,
   boundary, actors, capabilities, exclusions, measures, and optional product-
   wide DCL.
3. Put simple observable acceptance on each capability. Copy
   `assets/acceptance-template.yaml` only when multiple scenarios, material
   failure paths, cross-capability behavior, or quality outcomes need a separate
   owner.
4. Draft the physical product boundary in `architecture/stack-context.md` and
   actor-visible paths in `experience/user-flows.md`.
5. Add state, data, sequence, rule, contract, journey, screen, quality, or
   deployment artifacts only when each adds distinct meaning.
6. Add concise current rationale in the diagram file that owns every non-
   obvious choice.
7. Apply the skill-level checks in
   [PIP Use and Alignment Checks](change-and-handoff.md). Do not store their
   result or add status, readiness, signoff, or handoff content to the PIP.

For a small or single-product-leader team, omit governance. Copy
`assets/governance-template.yaml` only when several product leaders or delegated
authorities genuinely need scope, precedence, or supersession to coordinate
decisions.

## Reconstruct

Use reconstruction when a product exists but its intent is missing, incomplete,
or inconsistent. Do not use the canonical PIP as the research workspace.

1. Create an isolated PIP fork and separate working notes.
2. Identify the product and release being reconstructed, the product leader,
   source environments, and known boundary. Do not blend several
   implementations into one implied end state.
3. Inspect only useful evidence: running surfaces, documents, research, designs,
   routes, behavior, tests, data, contracts, integrations, operations, incidents,
   and migrations.
4. In the working notes, distinguish direct observations, inferences,
   contradictions, recommendations, and source limitations.
5. Reconstruct from the outside inward: actors and visible flows, capabilities
   and acceptance, physical stack, then only the state, data, sequence, rule,
   contract, quality, or journey detail needed to resolve product meaning.
6. Ask the product leader whether each consequential behavior is intended, a
   defect, a legacy constraint, a different future product, or out of scope.
7. Express the resulting coherent end state in the fork without evidence
   labels, questions, alternatives, or proposal fields.
8. Adopt the fork through normal product-leader and Git review. Until then, the
   canonical PIP remains unchanged.

Before assigning DCL, establish current user interactions, whether users wait,
failure consequences, acceptable interruption and recovery, credible load,
risk, and operating needs. Do not infer DCL from company stage or implementation
complexity.

## Complete

For an incomplete canonical package:

1. Read the three core files and existing optional artifacts.
2. Check whether a reader can identify the release outcome, boundary, actors,
   capabilities, visible experience, physical ownership, observable acceptance,
   and material constraints.
3. Follow direct links and inspect obvious semantic dependents; do not build an
   exhaustive graph.
4. Add or repair only the facts and artifacts needed to close a real ambiguity.
5. Move simple acceptance inline; retain a separate file only when it improves
   clarity.
6. Add or refresh current rationale without preserving obsolete history.
7. Remove empty, duplicative, implementation-only, status, readiness, review,
   and other ceremonial content after preserving current intent in its owner.
8. Apply the skill-level checks without creating a PIP check record.

If completion exposes a product choice, keep the canonical PIP unchanged for
that choice and resolve it outside the package. Use a PIP fork when a concrete
alternative needs review.

## Update

If the product leader's request already gives an unambiguous new end state,
update the owning canonical facts and affected dependents through the team's
normal Git workflow. If the change is still a recommendation, alternative, or
unresolved choice, create an isolated PIP fork instead.

1. Identify the owning fact, affected actors and capabilities, and release.
2. Review direct links plus obvious semantic dependents.
3. Update the owner, then affected flows, behavior, data, architecture,
   sequences, constraints, and acceptance.
4. Refresh each affected diagram's current rationale so it contains all and
   only the reasons for the new current design.
5. Preserve stable cross-file IDs when meaning is unchanged. Add or retire IDs
   only when meaning is added, split, replaced, or removed.
6. Apply the skill-level checks. Let Git preserve the change history.

Do not place both old and new intent in the canonical PIP, add a proposal lane,
or increment per-artifact versions for an ordinary change.

## Implement or audit against a PIP

Use this workflow only when implementation or audit is explicitly governed by
a PIP:

1. Record the task-start canonical PIP Git revision and release in the existing
   task or working notes, not in the PIP.
2. Treat code, migrations, tests, tickets, logs, and runtime behavior as
   implementation evidence. They do not change product intent.
3. Compare planned or observed product-significant behavior, schema, policy,
   queries, and design with the task-start PIP and any later direct product-
   leader instruction.
4. Inspect existing implementation owners before adding code. Follow sequence
   anchors marked `reuse unchanged` or `modify existing`, and verify input
   provenance.
5. Follow exact linked mockups. Use compatible example or export code when
   available, without silently changing surfaces, components, states, or
   interactions.
6. Proceed with ordinary internal choices that stay inside current behavior and
   material constraints.
7. Report implementation deviations in the task or audit result. Fix the
   implementation toward the PIP when authorized. Do not edit the canonical PIP
   merely to document what the implementation currently does.
8. If the team wants the implementation difference to become product intent,
   create a coherent PIP fork for product-leader review. Adopt it only after the
   product decision.

When useful, compare the PIP's default or overridden target DCL with an observed
implementation DCL in the audit notes. Never persist the implementation level
or comparison in the PIP.

## Simplify or migrate an older package

For a format-6 or similarly heavy package:

1. Identify the current product facts and acceptance outcomes before removing
   machinery. Keep evidence, proposals, open questions, implementation findings,
   and history in working notes if they still matter operationally.
2. Move release, outcome, boundary, actors, capabilities, simple acceptance,
   exclusions, measures, and optional default DCL into `product.yaml`.
3. Remove package and item statuses, readiness labels, signatures, confirmation
   metadata, handoff records, implementation observations, proposal lanes,
   source catalogs, and routine decision history from the canonical PIP.
4. Remove governance for a single-product-leader team. In a real multi-
   authority team, retain only scope, precedence, and supersession context.
5. Move simple acceptance inline. Keep `acceptance.yaml` only when its scenarios
   remain easier to understand separately.
6. Consolidate context/component/container views into stack context, screen maps
   into user flows, and conceptual/persisted relationships into one data-model
   view when those facts remain needed.
7. Replace scoped target/PIP/implementation DCL comparisons with one optional
   product default and narrow current-intent overrides. Move implementation
   comparisons to audit notes.
8. Add concise current rationale to each diagram owner and remove historical
   narration.
9. Remove artifact indexes, trace graphs, coverage matrices, change logs,
   readiness ledgers, discretion registries, empty placeholders, package hashes,
   and duplicated metadata.
10. Preserve meaningful cross-file IDs, direct links, and product behavior.
    Check the result proportionally.

Do not chase parity with the old file count. A representation-only migration
must not silently change product meaning.
