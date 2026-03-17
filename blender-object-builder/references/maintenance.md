# Skill Maintenance

Use this file when deciding whether a failure should automatically improve the skill.

## Update the Skill When

- The failure came from a bad default in this skill.
- The skill encouraged an unsafe Blender pattern.
- A reusable Blender gotcha was missing from the current guidance.
- One of the bundled templates needed the same fix the task just required.
- A better official Blender source changes the recommended approach.

## Do Not Update the Skill When

- The problem is only in the user's project code and does not change the reusable Blender guidance.
- The issue is a temporary local environment problem with no general lesson.
- The fix is purely stylistic and does not improve correctness, safety, or repeatability.
- The issue is hypothetical and did not affect the actual task.

## Where to Put the Fix

- Put new hard defaults in `SKILL.md`.
- Put detailed gotchas in `pitfalls.md`.
- Put safe recipes in `patterns.md`.
- Put executable reusable fixes in `scripts/`.
- Put new canonical documentation in `sources.md`.

## Validation

Run `python scripts/validate_skill.py` after any change to this skill.
