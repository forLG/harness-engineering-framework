# Status And Placeholder Language

Status: completed.

## Goal

Define and enforce a small language convention for `Status:`, `PROJECT_PLACEHOLDER(...)`, `FRAMEWORK_TODO(...)`, and legacy placeholder words across the harness framework.

## Completed Work

- Added `docs/product-specs/language-conventions.md` as the canonical convention.
- Linked the convention from `README.md` and `docs/GUARDRAILS.md`.
- Normalized existing `Status:` values to the approved vocabulary.
- Updated `tools/entropy_control.py` to ignore Markdown code examples during legacy placeholder scans.
- Added entropy control checks for non-standard `Status:` values.
- Kept intentional `PROJECT_PLACEHOLDER(...)` and `FRAMEWORK_TODO(...)` markers out of placeholder debt.

## Verification

Completed on 2026-05-02:

```bash
python tools\entropy_control.py --report --update-quality-score
python tools\validate_harness_structure.py
python -m py_compile tools\entropy_control.py
python tools\run_evals.py --suite smoke
python -m json.tool evals\benchmarks\product-template\benchmark.template.json
python -m json.tool evals\benchmarks\product-template\task.template.json
```

Results:

- Entropy control passed with zero findings and refreshed `docs/QUALITY_SCORE.md` to 100 overall.
- Structural validation passed.
- Smoke evals passed.
- Product benchmark templates remained valid JSON.
