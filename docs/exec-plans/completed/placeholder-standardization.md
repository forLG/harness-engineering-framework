# Placeholder Standardization

Status: completed.

## Goal

Unify project-specific placeholder language across the harness framework so adopters can identify exactly what must be filled when the scaffold is applied to a real repository.

## Completed Work

- Added the placeholder convention to `README.md`.
- Standardized project-specific placeholders as `PROJECT_PLACEHOLDER(<key>): <what to fill>`.
- Standardized future framework work as `FRAMEWORK_TODO(<key>): <what remains>`.
- Replaced mixed placeholder language across architecture, environment, runtime, observability, guardrails, evaluation, reliability, security, reference notes, and product benchmark templates.
- Refreshed `docs/QUALITY_SCORE.md` from the entropy report after cleanup.
- Updated `tools/entropy_control.py` so generated quality score notes reference the entropy report id instead of a fragile local artifact path.

## Verification

Completed on 2026-05-02:

```bash
python tools\validate_harness_structure.py
python tools\entropy_control.py --report --update-quality-score
python -m py_compile tools\entropy_control.py
python -m json.tool evals\benchmarks\product-template\benchmark.template.json
python -m json.tool evals\benchmarks\product-template\task.template.json
```

Results:

- Structural validation passed.
- Entropy control passed with no open quality debt.
- Product benchmark templates remained valid JSON.
