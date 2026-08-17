# Product Intent Package

This repository contains the Product Intent Package standard, one
outward-facing product-management Agent Skill, and the modeled PIP IDE product
package.

## Agent skill

The single skill is
[`skills/product-intent-manager/`](skills/product-intent-manager/). It helps
product teams create, inspect, refine, and manage a Product Intent Package.
Product reconstruction is a subsection of this skill. It uses current product
evidence to build or update the same package.

## Skill contents

- [`SKILL.md`](skills/product-intent-manager/SKILL.md) is the skill entrypoint.
- [`references/`](skills/product-intent-manager/references/) contains the
  package standard and workflow guidance.
- [`assets/product-intent-template/`](skills/product-intent-manager/assets/product-intent-template/)
  is a blank package structure.
- [`assets/example-product-intent-package/`](skills/product-intent-manager/assets/example-product-intent-package/)
  shows a completed package.
- [`evals/`](skills/product-intent-manager/evals/) contains skill activation and
  behavior cases.

## Product Intent Package format

Use the
[package standard](skills/product-intent-manager/references/product-intent-package-standard.md)
as the format authority. The current package format is 3.0.0.

- Store structured records in YAML files (`.yaml`), not JSON files.
- Store Mermaid diagrams in Markdown files (`.md`) with fenced `mermaid` blocks,
  including files that contain only a diagram.
- Keep copied source evidence in its original format when the package records
  it.
- Store lifecycle journey metadata in
  `experience/journeys/index.yaml`. Store each journey source as a Markdown
  file with a fenced Mermaid block or a Markdown lifecycle table.

## PIP IDE product package

The modeled PIP IDE draft is in
[`product-intent/pip-ide/`](product-intent/pip-ide/). It records the product
goal, capabilities, proposed experience and technical models, open authority
questions, traceability, and handoff state.

The team also uses
[Linear](https://linear.app/thereadyroom/project/pip-ide-b3ecbb55ae96/overview),
[Figma](https://www.figma.com/design/NMUiwN7LaOsPrsQO3KPP4W/IP-IDE-Experience?node-id=4-17),
[Miro](https://miro.com/app/board/uXjVHx4xkvQ=/), and
[Google Sheets](https://docs.google.com/spreadsheets/d/1NzMCST9gNxd_3PO645u3TwqNwHfETTsbiTzg6wfQFbI/edit)
as working views and evidence. The package remains the source of product intent.
