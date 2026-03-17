"""Create a custom mesh object using Blender's data API.

Adapt this template instead of reaching for bpy.ops-based primitive creation.
"""

import bpy


def get_or_create_collection(collection_name: str) -> bpy.types.Collection:
    scene_root = bpy.context.scene.collection
    collection = bpy.data.collections.get(collection_name)
    if collection is None:
        collection = bpy.data.collections.new(collection_name)
        scene_root.children.link(collection)
    elif scene_root.children.get(collection.name) is None:
        scene_root.children.link(collection)
    return collection


def create_mesh_object(
    object_name: str,
    mesh_name: str,
    collection_name: str,
    vertices,
    edges,
    faces,
    location=(0.0, 0.0, 0.0),
):
    collection = get_or_create_collection(collection_name)

    mesh = bpy.data.meshes.new(mesh_name)
    mesh.from_pydata(vertices, edges, faces)
    mesh.validate(verbose=True)
    mesh.update()

    obj = bpy.data.objects.new(object_name, mesh)
    collection.objects.link(obj)
    obj.location = location
    return obj


def build_pyramid():
    vertices = [
        (-1.0, -1.0, 0.0),
        (1.0, -1.0, 0.0),
        (1.0, 1.0, 0.0),
        (-1.0, 1.0, 0.0),
        (0.0, 0.0, 1.5),
    ]
    edges = []
    faces = [
        (0, 1, 2, 3),
        (0, 1, 4),
        (1, 2, 4),
        (2, 3, 4),
        (3, 0, 4),
    ]
    return create_mesh_object(
        object_name="Pyramid",
        mesh_name="PyramidMesh",
        collection_name="Generated",
        vertices=vertices,
        edges=edges,
        faces=faces,
        location=(0.0, 0.0, 0.0),
    )


if __name__ == "__main__":
    print(f"Running in Blender {bpy.app.version_string}")
    obj = build_pyramid()
    print(f"Created object: {obj.name}")
