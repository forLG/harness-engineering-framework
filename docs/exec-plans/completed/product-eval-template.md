# Product Eval Template

Status: completed.

## Goal

Add a phase-three evaluation placeholder that shows where product-specific benchmark suites belong without adding fake product behavior to the universal framework.

## Completed Work

- Added `evals/benchmarks/product-template/README.md`.
- Added `benchmark.template.json` and `task.template.json`.
- Documented the product suite workflow in `docs/EVALUATION.md` and `README.md`.
- Added template paths to structural validation.
- Confirmed the template is not discovered as a runnable benchmark.

## Verification

Completed on 2026-04-30:

```bash
D:\Applications\Scoop\apps\anaconda3\2024.06-1\App\python.exe -m py_compile tools\run_evals.py tools\harness_loop.py tools\validate_harness_structure.py tools\validate_guardrails.py
D:\Applications\Scoop\apps\anaconda3\2024.06-1\App\python.exe tools\run_evals.py --list
D:\Applications\Scoop\apps\anaconda3\2024.06-1\App\python.exe tools\run_evals.py --suite smoke
D:\Applications\Scoop\apps\anaconda3\2024.06-1\App\python.exe tools\validate_harness_structure.py
```

Smoke baseline comparison:

- `prompt-preview`: passed.
- `structure-validation`: passed.
- Baseline compared: `evals/baselines/smoke.json`.
