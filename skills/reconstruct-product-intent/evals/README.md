# Skill Evaluation Cases

Use the cases in `cases.yaml` to test both activation and behavior.

Minimum must-pass rubric:

- invokes for the intended workflow and not for ordinary code documentation/implementation;
- distinguishes evidence from confirmed intent;
- identifies and routes authority domains;
- refuses to silently infer behavior or resolve conflicts;
- produces all thirteen structures, including lifecycle journeys, and traceability;
- leaves unavailable decisions blocked rather than fabricating certainty;
- does not claim build-ready while validator or gates fail;
- records bounded implementation discretion rather than vague “best practices”;
- for iteration, marks dependent artifacts stale and updates acceptance/traceability.
- writes skill-authored structured records as `.yaml` and Mermaid diagrams as `.md` files with fenced `mermaid` blocks, including diagram-only files;
- keeps `.json` and `.mmd` only for copied source evidence or required external formats, not canonical package records.

Additional journey rubric:

- distinguish a lifecycle journey from a marketing funnel;
- separate materially different actor variants;
- require an actor-action lane and a product-response lane for every action;
- cover failure, pause/resume, abandonment, exit, and recovery;
- keep observed, inferred, proposed, and confirmed journey intent separate;
- require qualified local links, detailed artifact links, and editable Markdown
  sources;
- mark the parent journey and linked dependents stale after phase changes;
- block build-ready and journey_closure for open journey questions, assumptions,
  contradictions, or unconfirmed intent.

## Deterministic smoke test

These cases are prompts and rubrics. No automated eval runner is included.

```bash
python scripts/validate_product_intent.py assets/example-product-intent-package --no-report
```

The bundled example must pass with zero errors and zero warnings.
