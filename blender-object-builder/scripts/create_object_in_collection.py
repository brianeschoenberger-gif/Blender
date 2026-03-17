"""Create an object and link it to an explicit collection.

Use this template when collection ownership matters more than the geometry itself.
"""

import bpy


def ensure_collection(collection_name: str) -> bpy.types.Collection:
    scene_root = bpy.context.scene.collection
    collection = bpy.data.collections.get(collection_name)
    if collection is None:
        collection = bpy.data.collections.new(collection_name)
        scene_root.children.link(collection)
    elif scene_root.children.get(collection.name) is None:
        scene_root.children.link(collection)
    return collection


def build_box_mesh(mesh_name: str, size: float = 2.0) -> bpy.types.Mesh:
    half = size / 2.0
    vertices = [
        (-half, -half, -half),
        (half, -half, -half),
        (half, half, -half),
        (-half, half, -half),
        (-half, -half, half),
        (half, -half, half),
        (half, half, half),
        (-half, half, half),
    ]
    edges = []
    faces = [
        (0, 1, 2, 3),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (3, 0, 4, 7),
    ]

    mesh = bpy.data.meshes.new(mesh_name)
    mesh.from_pydata(vertices, edges, faces)
    mesh.validate(verbose=True)
    mesh.update()
    return mesh


def create_object_in_collection(
    collection_name: str,
    object_name: str,
    mesh_name: str,
    location=(0.0, 0.0, 0.0),
):
    collection = ensure_collection(collection_name)
    mesh = build_box_mesh(mesh_name)
    obj = bpy.data.objects.new(object_name, mesh)
    collection.objects.link(obj)
    obj.location = location
    return obj


if __name__ == "__main__":
    print(f"Running in Blender {bpy.app.version_string}")
    obj = create_object_in_collection(
        collection_name="Props",
        object_name="BoxInProps",
        mesh_name="BoxInPropsMesh",
        location=(2.0, 0.0, 0.0),
    )
    print(f"Created object in collection: {obj.name}")
