# Product Intent Agent Skills

Two standalone Agent Skills implement an authority-confirmed, clarification-free product specification workflow.

## 1. `reconstruct-product-intent`

Converts an existing software project into a Product Intent Package by inspecting code, databases, tests, documents, tickets, designs, media, runtime behavior, analytics, and operations, then interviewing the correct product, design, technical, and specialist authorities to resolve missing or contradictory intent.

It explicitly separates:

- observed implementation;
- agent interpretation;
- proposed target behavior;
- authority-confirmed target intent.

## 2. `product-intent-manager`

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
- `evals/` — activation and behavior cases plus a deterministic smoke test.

Each skill is self-contained. Shared standards are duplicated intentionally so either directory can be installed or uploaded independently.

## Package file format

Use each skill's `references/product-intent-package-standard.md` as the source of truth for package formats. Store skill-authored structured records as `.yaml` files. Store Mermaid diagrams as Markdown `.md` files with fenced `mermaid` blocks, including diagram-only files. Do not add canonical `.json` or `.mmd` files; preserve copied source evidence and required external media types in their required formats.

The current Product Intent Package format is 2.0.0.

## Smoke tests

```bash
python reconstruct-product-intent/scripts/validate_product_intent.py \
  reconstruct-product-intent/assets/example-product-intent-package --no-report

python product-intent-manager/scripts/validate_product_intent.py \
  product-intent-manager/assets/example-product-intent-package --no-report
```

Both commands must return zero errors and zero warnings.
