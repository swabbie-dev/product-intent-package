# Product Intent Package

This monorepo contains the Product Intent Package standard, its agent skills, and the PIP IDE product package.

## PIP IDE product package

The modeled PIP IDE draft is in [`product-intent/pip-ide/`](product-intent/pip-ide/). It is the source of truth for the product goal, confirmed capabilities, proposed experience and technical models, open authority questions, traceability, and handoff state.

Project work also uses:

- [Linear](https://linear.app/thereadyroom/project/pip-ide-b3ecbb55ae96/overview) for the execution overlay;
- [Figma](https://www.figma.com/design/NMUiwN7LaOsPrsQO3KPP4W/IP-IDE-Experience?node-id=4-17) for design proposals;
- [Miro](https://miro.com/app/board/uXjVHx4xkvQ=/) for early system canvases;
- [Google Sheets](https://docs.google.com/spreadsheets/d/1NzMCST9gNxd_3PO645u3TwqNwHfETTsbiTzg6wfQFbI/edit) for early table work.

The PIP remains canonical. External tools provide human-friendly working views and evidence. They do not replace package authority or approval records.

## Agent skills

Two standalone Agent Skills implement an authority-confirmed, clarification-free product specification workflow. Both use Product Intent Package format 3.0.0.

## 1. `skills/reconstruct-product-intent`

Converts an existing software project into a Product Intent Package by inspecting code, databases, tests, documents, tickets, designs, media, runtime behavior, analytics, and operations, then interviewing the correct product, design, technical, and specialist authorities to resolve missing or contradictory intent.

It explicitly separates:

- observed implementation;
- agent interpretation;
- proposed target behavior;
- authority-confirmed target intent.

Both skills model Lifecycle Journey Maps as first-class experience artifacts.
Journey metadata is YAML at
`experience/journeys/index.yaml`. Each editable journey source is
`experience/journeys/JOURNEY-*.md` with a fenced `mermaid` block or a Markdown
lifecycle table. A journey frames detailed flows, screens, rules, state
machines, contracts, sequences, quality constraints, and acceptance scenarios;
it does not replace them. Lifecycle journeys are not marketing funnels unless
the product authority confirms that scope.

## 2. `skills/product-intent-manager`

Creates a Product Intent Package from scratch, completes an existing package, and manages product iterations through decision capture, impact analysis, staleness propagation, reconfirmation, versioning, validation, and handoff approval.

## Included in each skill

- `SKILL.md` — routing boundary and core workflow;
- `references/` — package standard, authority/evidence policy, record schemas, question protocol, handoff gates, and workflow-specific guidance;
- `assets/product-intent-template/` — blank canonical package structure;
- `assets/example-product-intent-package/` — fully populated example that passes validation;
- `requirements.txt` — Python dependency for the bundled scripts;
- `scripts/init_product_intent.py` — initializes a package;
- `scripts/validate_product_intent.py` — validates authorities, IDs, coverage, traceability, decisions, questions, contradictions, staleness, placeholders, discretion, readiness, and hash;
- `scripts/stamp_package_hash.py` — creates a reproducible product-content hash;
- workflow-specific inventory or impact-analysis scripts;
- `evals/` — activation and behavior cases plus rubrics. No automated eval
  runner is included.

Each skill is self-contained. Shared standards are duplicated intentionally so either directory can be installed or uploaded independently.

## Package file format

Use each skill's `references/product-intent-package-standard.md` as the source of truth for package formats. Store skill-authored structured records as `.yaml` files. Store Mermaid diagrams as Markdown `.md` files with fenced `mermaid` blocks, including diagram-only files. Do not add canonical `.json` or `.mmd` files; preserve copied source evidence and required external media types in their required formats.

The current Product Intent Package format is 3.0.0. The format adds lifecycle
journey metadata, actor coverage, qualified local phase/action links, and the
journey_closure readiness gate. The separate modeled PIP IDE package under
`product-intent/pip-ide/` is not migrated by this skill update and has no
invented journeys.

## Skill distributions

The repository distribution convention is deterministic ZIP archives plus
`dist/SHA256SUMS`. This is a repository convention, not an OpenAI standard.
The archives contain only the corresponding self-contained skill directory.

Generate archives from the current committed source tree:

```bash
mkdir -p dist
git archive --format=zip \
  --prefix=reconstruct-product-intent/ \
  --mtime=1980-01-01T00:00:00Z \
  --output=dist/reconstruct-product-intent.zip \
  HEAD:skills/reconstruct-product-intent
git archive --format=zip \
  --prefix=product-intent-manager/ \
  --mtime=1980-01-01T00:00:00Z \
  --output=dist/product-intent-manager.zip \
  HEAD:skills/product-intent-manager
(cd dist && shasum -a 256 reconstruct-product-intent.zip product-intent-manager.zip > SHA256SUMS)
```

Verify checksums and ZIP structure:

```bash
(cd dist && shasum -a 256 -c SHA256SUMS)
unzip -t dist/reconstruct-product-intent.zip
unzip -t dist/product-intent-manager.zip
```

## Smoke tests

```bash
uv run --with-requirements skills/reconstruct-product-intent/requirements.txt \
  python skills/reconstruct-product-intent/scripts/validate_product_intent.py \
  skills/reconstruct-product-intent/assets/example-product-intent-package --no-report

uv run --with-requirements skills/product-intent-manager/requirements.txt \
  python skills/product-intent-manager/scripts/validate_product_intent.py \
  skills/product-intent-manager/assets/example-product-intent-package --no-report
```

Both commands must return zero errors and zero warnings.
