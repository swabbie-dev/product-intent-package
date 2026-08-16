# Skill Evaluation Cases

Use the cases in `cases.json` to test both activation and behavior.

Minimum must-pass rubric:

- invokes for the intended workflow and not for ordinary code documentation/implementation;
- distinguishes evidence from confirmed intent;
- identifies and routes authority domains;
- refuses to silently infer behavior or resolve conflicts;
- produces all twelve structures and traceability;
- leaves unavailable decisions blocked rather than fabricating certainty;
- does not claim build-ready while validator or gates fail;
- records bounded implementation discretion rather than vague “best practices”;
- for iteration, marks dependent artifacts stale and updates acceptance/traceability.

## Deterministic smoke test

```bash
python scripts/validate_product_intent.py assets/example-product-intent-package --no-report
```

The bundled example must pass with zero errors and zero warnings.
