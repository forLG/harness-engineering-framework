# Evaluation

Status: initial scaffold.

Define repeatable benchmark tasks, acceptance criteria, and reporting.

## Benchmark Tasks

Store benchmark definitions in `evals/benchmarks/`.

At minimum, a benchmark should include:

- A queued task JSON file.
- Expected acceptance criteria.
- Validation commands.
- Expected final status.
- Required artifact checks.

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

## Regression Policy

Status: placeholder.

Before this framework is used autonomously, add an eval that runs:

```bash
python tools/harness_loop.py --once
python tools/validate_harness_structure.py
```

The first command verifies prompt assembly in preview mode. The second command verifies required harness structure.
