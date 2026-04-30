# Baseline Regression Implementation

Status: completed.

## Goal

Add a second evaluation phase that compares current benchmark outcomes against a versioned known-good baseline.

## Completed Work

- Added `evals/baselines/` as the tracked baseline location.
- Added `evals/baselines/smoke.json`.
- Made `regression_policy` active in `tools/run_evals.py`.
- Added `--update-baseline` and `--no-baseline` runner modes.
- Added default baseline comparison for normal suite runs.
- Updated evaluation, runtime, README, roadmap, and structural validation docs.

## Verification

Completed on 2026-04-30:

```bash
D:\Applications\Scoop\apps\anaconda3\2024.06-1\App\python.exe -m py_compile tools\run_evals.py tools\harness_loop.py tools\validate_harness_structure.py tools\validate_guardrails.py
D:\Applications\Scoop\apps\anaconda3\2024.06-1\App\python.exe tools\run_evals.py --suite smoke --update-baseline
D:\Applications\Scoop\apps\anaconda3\2024.06-1\App\python.exe tools\run_evals.py --suite smoke
D:\Applications\Scoop\apps\anaconda3\2024.06-1\App\python.exe tools\validate_harness_structure.py
```

Smoke baseline comparison:

- `prompt-preview`: passed.
- `structure-validation`: passed.
- Baseline compared: `evals/baselines/smoke.json`.
