# Observability

Status: scaffold.

The active harness loop stores its normal role prompts, role outputs, and run summaries under
`artifacts/runs/<run-id>/`. The locations below are reserved evidence buckets. They may contain
only `.gitkeep` until a real project or task has logs, traces, screenshots, or standalone
validation/review output worth preserving outside the run directory.

## Logs

- Location: `artifacts/logs/`
- Current use: reserved.
- Format: `PROJECT_PLACEHOLDER(log-format): define log format, naming, and minimum fields for the target project.`
- Retention: keep logs that explain a decision, regression, or human escalation.

## Traces

- Location: `artifacts/traces/`
- Current use: reserved.
- Format: `PROJECT_PLACEHOLDER(trace-format): define trace format, timeline schema, and correlation identifiers for the target project.`
- Retention: keep traces that explain behavior across agent steps, tools, services, or UI flows.

## Screenshots and UI Artifacts

- Location: `artifacts/screenshots/`
- Current use: reserved.
- Browser tooling: `PROJECT_PLACEHOLDER(browser-tooling): define Playwright, browser, device, or screenshot tooling used by the target project.`
- Required viewports: `PROJECT_PLACEHOLDER(required-viewports): define required desktop, tablet, mobile, and accessibility verification surfaces.`

## Review and Validation Evidence

- Review artifact location: `artifacts/reviews/`
- Validation artifact location: `artifacts/validation/`
- Current use: reserved. The current supervisor writes reviewer and validator outputs to
  `artifacts/runs/<run-id>/`; use these standalone directories only when evidence should be
  shared across runs or preserved separately from a single task run.

## Local Reproducibility

Document how to reproduce a task run, including environment setup, services, ports, seed data, and commands.

- `PROJECT_PLACEHOLDER(local-reproduction): list the commands and setup data needed to replay a failed or important run in the target project.`

## Maintenance Artifacts

- Location: `artifacts/maintenance/`
- JSON report: `<timestamp>-entropy-control.json`
- Markdown report: `<timestamp>-entropy-control.md`
- Latest pointer: `latest-entropy-report.json`

Entropy reports preserve the findings that led to cleanup tasks, quality score updates, or human escalation.
