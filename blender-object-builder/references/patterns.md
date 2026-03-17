# Blender Patterns

Use these patterns as defaults for object creation. Expand them only when the task requires it.

## Create a Custom Mesh Object

1. Create a mesh datablock with `bpy.data.meshes.new(mesh_name)`.
2. Populate geometry with `mesh.from_pydata(vertices, edges, faces)`.
3. Validate with `mesh.validate(verbose=True)`.
4. Update with `mesh.update()`.
5. Create an object with `bpy.data.objects.new(object_name, mesh)`.
6. Link the object into a named collection with `collection.objects.link(obj)`.

Adapt [../scripts/create_mesh_object.py](../scripts/create_mesh_object.py).

## Create Primitive-Like Geometry Without Operators

- Build the primitive vertex and face lists directly instead of calling `bpy.ops.mesh.primitive_*`.
- Favor a slightly longer explicit mesh definition over a short operator-dependent script.
- Name the mesh and object separately so later edits can target the correct datablock.

## Link to an Explicit Collection

1. Resolve a collection by name.
2. Create it if it does not exist.
3. Link the collection to the scene tree if needed.
4. Link the new object to that collection explicitly.

Adapt [../scripts/create_object_in_collection.py](../scripts/create_object_in_collection.py).

## Apply Transforms Deliberately

- Set `obj.location`, `obj.rotation_euler`, and `obj.scale` explicitly instead of assuming cursor state.
- Avoid `bpy.ops.object.transform_apply()` unless the task truly requires applied transforms and no simpler data path exists.
- Explain the consequence of applying transforms because it changes object data, not only presentation.

## Name Deliberately

- Use stable object, mesh, and collection names passed in as parameters or constants.
- Avoid relying on Blender's auto-numbered names when a later step must re-find the object.
- Re-resolve by name after destructive operations rather than trusting cached Python references.

## Headless Execution Pattern

- Discover the Blender executable first.
- Keep CLI argument order intentional.
- Include `--python-exit-code 1` so failures propagate to the shell.

Read [../scripts/run_blender_headless.example.txt](../scripts/run_blender_headless.example.txt) before writing commands.
