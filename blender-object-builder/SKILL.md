---
name: blender-object-builder
description: Script-first Blender object creation and scene editing via Python. Use when Codex needs to create or repair Blender Python scripts for meshes or objects, link objects into collections, avoid operator/context pitfalls, validate geometry, or plan headless Blender runs.
---

# Blender Object Builder

Use Blender's Python data API first. Reach for operators only when there is no stable data-API path.

## Default Workflow

1. If a repo-local harness such as `sailboat/automation/run_pipeline.py` or `automation/run_pipeline.py` exists, use it before emitting raw Blender CLI commands.
2. Discover the Blender executable before writing commands. Prefer `BLENDER_EXE`; do not assume `blender` is on `PATH`.
3. Capture the Blender version early and fail clearly when the environment is missing, unknown, or outside the expected range.
4. Prefer direct datablock creation over `bpy.ops`: create meshes with `bpy.data.meshes.new(...)`, populate with `mesh.from_pydata(...)`, validate with `mesh.validate()`, update with `mesh.update()`, create objects with `bpy.data.objects.new(...)`, and link with `collection.objects.link(obj)`.
5. Name the target collection, object, and mesh explicitly. Do not rely on the active collection, selection, cursor, or current view layer state.
6. Normalize mode before mesh edits. Leave `EDIT` mode before modifying mesh datablocks from the object side.
7. Read `report.json` before patching a generator, and use the generated preview image for visual inspection when needed.
8. Explain any operator use, including why the data API is insufficient and what context requirements must be satisfied.
9. Update this skill before finishing when a real, reusable Blender failure is discovered while using it.

## Hard Rules

- Prefer `bpy.data` and explicit collection linking over `bpy.ops.mesh.primitive_*` and similar UI-driven shortcuts.
- Avoid assuming `bpy.context.object`, `bpy.context.active_object`, selected objects, the active collection, or cursor placement.
- Avoid keeping Python references to datablocks after removing or replacing them. Re-resolve them from Blender data after destructive changes.
- Avoid thread-based Blender API work. Treat Blender Python execution as main-thread only.
- Validate custom mesh geometry with `mesh.validate()` and then call `mesh.update()`.
- Restore or preserve state deliberately if a workflow must change mode, selection, or active object.
- Treat reusable failures as maintenance input for this skill, not as one-off trivia to mention and forget.

## Continuous Improvement Loop

When this skill is used and a real Blender-specific failure, omission, or misleading default is encountered, update the skill before finishing unless the user explicitly says not to modify the skill.

Use this loop:

1. Confirm the issue is reusable and belongs to this skill rather than only to the current project.
2. Patch the smallest correct artifact:
   - Update `SKILL.md` for default behavior or hard rules.
   - Update `references/pitfalls.md` for gotchas and failure modes.
   - Update `references/patterns.md` for better default recipes.
   - Update `scripts/*.py` when a reusable template should change.
   - Update `references/sources.md` only when a new official Blender source materially improves the guidance.
3. Validate the skill with `python scripts/validate_skill.py`.
4. Mention the skill update briefly in the final response so the user knows the guardrail improved.

Do not update the skill for purely hypothetical issues, transient local setup problems with no reusable lesson, or bugs unrelated to Blender object-creation workflows.

## Operator Escape Hatch

Use an operator only when a stable data-API path is missing or significantly more fragile.

When an operator is unavoidable:

1. State why the operator is necessary.
2. Satisfy `poll()` requirements deliberately instead of hoping the current UI context works.
3. Prefer `bpy.context.temp_override(...)` when the operator requires a specific area, region, object, or selection context.
4. Minimize and document any temporary state mutation.

Read [references/pitfalls.md](references/pitfalls.md) before using operators.

## Mesh/Object Creation Recipe

Use this order by default:

```python
mesh = bpy.data.meshes.new(mesh_name)
mesh.from_pydata(vertices, edges, faces)
mesh.validate(verbose=True)
mesh.update()

obj = bpy.data.objects.new(object_name, mesh)
collection.objects.link(obj)
obj.location = location
```

Adapt [scripts/create_mesh_object.py](scripts/create_mesh_object.py) for custom meshes and [scripts/create_object_in_collection.py](scripts/create_object_in_collection.py) when collection ownership matters.

## Environment Checks

- Prefer a repo-local automation harness when available, especially for build-render-validate loops.
- Discover Blender before generating CLI commands.
- Prefer `BLENDER_EXE` over assuming PATH-based discovery.
- Use `bpy.app.version` or `bpy.app.version_string` inside Blender scripts to report the runtime version.
- Use `--background`, `--python`, and `--python-exit-code 1` for headless automation.
- Respect Blender CLI argument order. Read [scripts/run_blender_headless.example.txt](scripts/run_blender_headless.example.txt) before emitting commands.
- When a pipeline emits `report.json` and `preview.png`, inspect the report first and use the image only for follow-up visual checks.
- After changing this skill, run [scripts/validate_skill.py](scripts/validate_skill.py).

## References and Templates

- Read [references/pitfalls.md](references/pitfalls.md) for operator/context failures, mode discipline, stale references, and crash/threading notes.
- Read [references/patterns.md](references/patterns.md) for safe creation recipes, transforms, naming, and collection linking patterns.
- Read [references/maintenance.md](references/maintenance.md) when deciding whether a failure should cause a skill update.
- Read [references/sources.md](references/sources.md) for the canonical official Blender sources that anchor this skill.
- Adapt [scripts/create_mesh_object.py](scripts/create_mesh_object.py) for script-first object creation.
- Adapt [scripts/create_object_in_collection.py](scripts/create_object_in_collection.py) for explicit collection ownership.
- Run [scripts/validate_skill.py](scripts/validate_skill.py) after modifying this skill.
