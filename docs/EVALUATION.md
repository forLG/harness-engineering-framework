# Evaluation

Status: smoke loop implemented.

The evaluation loop is split into a framework-generic runner and project- or product-specific benchmark content. The runner checks whether the harness can assemble prompts, preserve artifacts, run validators, and report regressions. Benchmark task files define the work surface being tested.

## Runner

Use the smoke suite before merging harness changes:

```bash
python tools/run_evals.py --suite smoke
```

List available benchmarks:

```bash
python tools/run_evals.py --list
```

The runner writes result JSON files into `evals/results/`. These files are ignored by default because they are machine-specific; force-add one only when it explains an important decision or regression.

By default, the runner compares the selected suite against a versioned baseline in `evals/baselines/<suite>.json`. Update the baseline only after a known-good run:

```bash
python tools/run_evals.py --suite smoke --update-baseline
```

Skip baseline comparison for exploratory local checks:

```bash
python tools/run_evals.py --suite smoke --no-baseline
```

## Benchmark Tasks

Store benchmark definitions in `evals/benchmarks/<benchmark-id>/`.

Preview-mode benchmarks should include:

- `benchmark.json`.
- A queued task JSON file referenced by `task_file`.
- Expected acceptance criteria.
- Validation commands.
- Expected final status.
- Required artifact checks.

Command-mode benchmarks may omit `task_file` and run deterministic local checks such as validators.

`benchmark.json` fields:

```json
{
  "id": "prompt-preview",
  "suite": "smoke",
  "mode": "preview",
  "description": "Verify prompt assembly and artifact capture.",
  "task_file": "task.json",
  "harness_command": "{python} tools/harness_loop.py --once",
  "commands": ["{python} tools/validate_harness_structure.py"],
  "required_artifacts": ["summary.json"],
  "max_latency_seconds": 30,
  "regression_policy": "fail_on_status_regression"
}
```

The initial smoke suite contains:

- `prompt-preview`: stages a benchmark task, runs the harness loop in preview mode, and checks role prompt/output artifacts.
- `structure-validation`: runs the structural and guardrail validator.

Use `{python}` in benchmark commands when the command should run under the same Python interpreter that launched `tools/run_evals.py`.

## Product Suites

Phase-three product evals are intentionally project-specific. The framework provides a template in `evals/benchmarks/product-template/`, but it does not ship runnable product benchmarks.

To add product evals after this scaffold is applied to a real project:

1. Copy `evals/benchmarks/product-template/` to `evals/benchmarks/<product-benchmark-id>/`.
2. Rename `benchmark.template.json` to `benchmark.json`.
3. Rename `task.template.json` to `task.json`.
4. Replace every `TODO` with target-project facts.
5. Run the product suite without a baseline while calibrating it:

```bash
python tools/run_evals.py --suite product-smoke --no-baseline
```

After a known-good pass, create the product baseline:

```bash
python tools/run_evals.py --suite product-smoke --update-baseline
```

Product execute-mode suites should define sandbox, approval, cost, latency, rollback, and CI expectations before they become required checks.

## Results

Store eval outputs in `evals/results/`.

Each result should record:

- Task id.
- Commit or version.
- Model or agent configuration.
- Cost.
- Latency.
- Pass or fail status.
- Notes and artifacts.

Harness-loop runs should reference `artifacts/runs/<run-id>/summary.json`.

## Baselines

Store suite baselines in `evals/baselines/`.

Baselines are tracked because they are the repository's known-good contract. They intentionally record stable fields only:

- Benchmark id.
- Benchmark mode.
- Expected status.
- Command pass status and return code.

Baselines do not record timestamps, run ids, artifact directories, stdout, stderr, or latency.

## Regression Policy

Status: baseline comparison implemented.

The eval runner exits nonzero when any selected benchmark fails or when the current result regresses from the tracked baseline. This makes regressions visible before merge in local checks or CI.

Before this framework is used autonomously, the smoke suite should pass:

```bash
python tools/run_evals.py --suite smoke
```

The smoke suite intentionally uses preview mode so it does not require Codex availability, credentials, network access, or permission prompts. Product-specific suites can add execute-mode benchmarks later once the target project has stable sandbox and cost controls.

`regression_policy` currently supports:

- `fail_on_status_regression`: fail when a benchmark was passing in the baseline and no longer passes.
- `none`: run the benchmark but skip baseline comparison.
