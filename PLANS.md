# Plans

Status: lightweight scaffold.

This file is the planning index. Keep active execution detail in `docs/exec-plans/active/` and completed plans in `docs/exec-plans/completed/`.

For the generic framework, this document tracks framework work. When copied into a real project, replace the scaffold roadmap with project-grounded milestones.

## Current Framework Roadmap

### Milestone 1: Lightweight Harness Skeleton

Status: implemented.

Goal: provide a concise Codex harness that is useful in normal human-supervised development.

Acceptance criteria:

- `AGENTS.md` is short and points to focused docs.
- `ARCHITECTURE.md` describes project shape, boundaries, state, and approval surfaces.
- `docs/` contains setup, runtime, validation, guardrail, observability, and security docs.
- `docs/exec-plans/` supports substantial in-progress work without a machine task queue.
- `tools/validate_harness_structure.py` verifies the required lightweight paths.

### Milestone 2: Project Application Workflow

Status: implemented.

Goal: make the scaffold easy to apply to a real project without inventing facts.

Acceptance criteria:

- `.skills/apply-harness-framework/SKILL.md` directs Codex to inspect first, fill from evidence, and leave precise placeholders.
- `README.md` describes adoption passes that match the lightweight structure.
- The framework makes interactive Codex plus human review the default path.

## Applied Project Plan Template

Use this section only after copying the framework into a target repository. Replace these entries with facts discovered from that project.

### Milestone 1: Project Harness Orientation

Status: project-specific.

Goal: `PROJECT_PLACEHOLDER(first-project-milestone-goal): define the first realistic milestone for applying the harness to this repository.`

Acceptance criteria:

- `PROJECT_PLACEHOLDER(project-orientation): AGENTS.md, ARCHITECTURE.md, and docs/ENVIRONMENT.md reflect the target repository's actual structure, setup, and validation commands.`
- `PROJECT_PLACEHOLDER(project-validation): the target project's normal validation commands are documented and at least one safe command has been run.`
- `PROJECT_PLACEHOLDER(project-evidence): useful setup, validation, or failure evidence is preserved under artifacts/ only when it explains a decision.`
