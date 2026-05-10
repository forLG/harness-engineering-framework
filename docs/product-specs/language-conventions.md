# Language Conventions

Status: implemented.

This project uses a small controlled vocabulary for lifecycle state, project placeholders, and framework work. The goal is to make docs easy for humans and agents to read.

## Status

Use `Status:` to describe the lifecycle state of a document, section, plan, generated file, or task. Put it near the top of the document or directly under the section heading it describes.

Allowed values:

- `Status: scaffold.`
- `Status: project-specific.`
- `Status: implemented.`
- `Status: generated.`
- `Status: active.`
- `Status: completed.`
- `Status: blocked.`
- `Status: deprecated.`

Do not use `Status: placeholder`. Placeholder is content state, not lifecycle state.

## Project Placeholders

Use `PROJECT_PLACEHOLDER(<key>): <what to fill>` for facts the universal framework cannot know until it is applied to a real repository.

Use this for target-project facts such as source layers, build commands, service ports, environment variables, secret handling, UI verification, product eval tasks, ownership boundaries, deployment rules, and product-specific guardrails.

Place the placeholder exactly where the future project fact belongs:

```md
## Example

- `PROJECT_PLACEHOLDER(ports): list local service ports, conflict policy, and reserved ranges.`
```

`PROJECT_PLACEHOLDER(...)` is intentional scaffold content. Replace it with project-specific facts when those facts become known.

## Framework Work

Use `FRAMEWORK_TODO(<key>): <work to do>` for known work on the harness framework itself.

Prefer placing framework work in `PLANS.md` or `docs/exec-plans/active/`. Use inline `FRAMEWORK_TODO(...)` only when the note must stay next to the affected rule or behavior.

## Legacy Words

Avoid bare `TODO`, `TBD`, `Status: placeholder`, and `Fill later` in docs. Use `PROJECT_PLACEHOLDER(...)` or `FRAMEWORK_TODO(...)` so future cleanup is intentional.

Completed execution plans may describe historical cleanup work, but active docs should use the controlled vocabulary above.
