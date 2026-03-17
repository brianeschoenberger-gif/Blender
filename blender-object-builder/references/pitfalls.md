# Blender Pitfalls

Use this file when Blender scripting work risks drifting into UI assumptions or unsafe data handling.

## Operator and Context Pitfalls

- Prefer `bpy.data` patterns over `bpy.ops`.
- Expect operators to fail when `poll()` requirements are not met.
- Avoid assuming the current area, region, mode, active object, or selection is usable.
- Use `bpy.context.temp_override(...)` when an operator truly requires a specific context.

## Mode Discipline

- Exit `EDIT` mode before modifying mesh datablocks through the object/data API.
- Avoid mixing edit-mode mesh access and object-mode mesh writes without an explicit transition.
- Restore mode deliberately only when the workflow requires it.

## Internal Data and Stale References

- Treat Blender datablocks as owned by Blender, not by Python variables.
- Stop using references after `remove()`, replacement, undo/redo-sensitive flows, or destructive rebuilds.
- Re-fetch objects, meshes, and collections by name or datablock lookup after destructive operations.

## Crash and Threading Notes

- Keep Blender API work on the main thread.
- Avoid background threads that touch `bpy`, data blocks, or the scene graph.
- Fail fast and clearly instead of trying to "recover" from invalid context or stale references.

## Version and Environment Checks

- Check whether Blender is installed before emitting shell commands.
- Capture `bpy.app.version` early when writing scripts meant for automation or reuse.
- Fail clearly when a required API assumption depends on a Blender version that is unknown in the current environment.
- When running scripts from Blender's Text Editor, do not assume `__file__` resolves to the project root. Bootstrap imports by locating the script folder or another on-disk project marker before importing sibling modules.
- Guard Blender API features that vary by version with capability checks such as `hasattr(...)` instead of assuming properties like material transparency or shadow settings exist under the same names.
- For Blender 5.x materials, prefer `surface_render_method` when controlling transparency behavior; treat `blend_method` as a compatibility fallback rather than the primary setting.
- When rerunning modular scripts from Blender's Text Editor, explicitly reload local modules with `importlib.reload(...)` before importing helpers; Blender can otherwise keep stale package modules in memory across runs.

## Read Next

- Read [patterns.md](patterns.md) for safe default recipes after identifying the relevant pitfall.
- Read [sources.md](sources.md) for the official Blender docs behind these rules.
