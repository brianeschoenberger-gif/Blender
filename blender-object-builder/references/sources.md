# Official Blender Sources

Use these as the canonical references for this skill. Prefer them over blogs, videos, forum posts, or remembered snippets.

- Operators gotchas: https://docs.blender.org/api/current/info_gotchas_operators.html
  Focus: why `bpy.ops` can fail due to `poll()` and context requirements.

- Internal data and Python objects: https://docs.blender.org/api/current/info_gotchas_internal_data_and_python_objects.html
  Focus: why stale references and datablock lifetime issues matter.

- Crashes and threading gotchas: https://docs.blender.org/api/current/info_gotchas_crashes.html
  Focus: crash-prone patterns, including unsupported threading assumptions.

- Collection linking API: https://docs.blender.org/api/current/bpy.types.CollectionObjects.html#bpy.types.CollectionObjects.link
  Focus: the explicit object-to-collection linking method this skill prefers.

- Mesh creation API: https://docs.blender.org/api/current/bpy.types.Mesh.html#bpy.types.Mesh.from_pydata
  Focus: direct mesh population without operators.

- Mesh validation API: https://docs.blender.org/api/current/bpy.types.Mesh.html#bpy.types.Mesh.validate
  Focus: validating custom geometry before using it.

- Context override API: https://docs.blender.org/api/current/bpy.types.Context.html#bpy.types.Context.temp_override
  Focus: the escape hatch when an operator truly requires context setup.

- Blender command-line arguments: https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html
  Focus: headless automation, argument order, and `--python` execution.
