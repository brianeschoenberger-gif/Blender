from __future__ import annotations

import bpy
import math


def ensure_collection(name: str, parent: bpy.types.Collection | None = None) -> bpy.types.Collection:
    collection = bpy.data.collections.get(name)
    if collection is None:
        collection = bpy.data.collections.new(name)

    if parent is None:
        scene_root = bpy.context.scene.collection
        if scene_root.children.get(collection.name) is None:
            scene_root.children.link(collection)
    elif parent.children.get(collection.name) is None:
        parent.children.link(collection)

    return collection


def ensure_child_collections(
    root: bpy.types.Collection, names: list[str]
) -> dict[str, bpy.types.Collection]:
    return {name: ensure_collection(name, root) for name in names}


def delete_collection_tree(name: str) -> None:
    collection = bpy.data.collections.get(name)
    if collection is None:
        return

    for child in list(collection.children):
        delete_collection_tree(child.name)

    for obj in list(collection.objects):
        bpy.data.objects.remove(obj, do_unlink=True)

    bpy.data.collections.remove(collection)


def assign_material(obj: bpy.types.Object, material: bpy.types.Material) -> None:
    if obj.type != "MESH" or obj.data is None:
        return
    if obj.data.materials.get(material.name) is None:
        obj.data.materials.append(material)


def create_mesh_object(
    name: str,
    mesh_name: str,
    collection: bpy.types.Collection,
    vertices: list[tuple[float, float, float]],
    faces: list[tuple[int, ...]],
    material: bpy.types.Material | None = None,
) -> bpy.types.Object:
    mesh = bpy.data.meshes.new(mesh_name)
    mesh.from_pydata(vertices, [], faces)
    mesh.validate(verbose=True)
    mesh.update()

    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)

    if material is not None:
        assign_material(obj, material)

    return obj


def create_box(
    name: str,
    collection: bpy.types.Collection,
    size: tuple[float, float, float],
    center: tuple[float, float, float] = (0.0, 0.0, 0.0),
    material: bpy.types.Material | None = None,
) -> bpy.types.Object:
    sx, sy, sz = size
    cx, cy, cz = center
    hx, hy, hz = sx * 0.5, sy * 0.5, sz * 0.5
    vertices = [
        (cx - hx, cy - hy, cz - hz),
        (cx + hx, cy - hy, cz - hz),
        (cx + hx, cy + hy, cz - hz),
        (cx - hx, cy + hy, cz - hz),
        (cx - hx, cy - hy, cz + hz),
        (cx + hx, cy - hy, cz + hz),
        (cx + hx, cy + hy, cz + hz),
        (cx - hx, cy + hy, cz + hz),
    ]
    faces = [
        (0, 1, 2, 3),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (3, 0, 4, 7),
    ]
    return create_mesh_object(name, f"{name}Mesh", collection, vertices, faces, material)


def create_prism(
    name: str,
    collection: bpy.types.Collection,
    points_2d: list[tuple[float, float]],
    z_min: float,
    z_max: float,
    material: bpy.types.Material | None = None,
) -> bpy.types.Object:
    vertices: list[tuple[float, float, float]] = []
    count = len(points_2d)
    for x, y in points_2d:
        vertices.append((x, y, z_min))
    for x, y in points_2d:
        vertices.append((x, y, z_max))

    faces: list[tuple[int, ...]] = [tuple(range(count)), tuple(range(count, count * 2))]
    for index in range(count):
        next_index = (index + 1) % count
        faces.append((index, next_index, next_index + count, index + count))

    return create_mesh_object(name, f"{name}Mesh", collection, vertices, faces, material)


def create_ngon_cylinder(
    name: str,
    collection: bpy.types.Collection,
    radius: float,
    height: float,
    center: tuple[float, float, float],
    segments: int = 12,
    material: bpy.types.Material | None = None,
) -> bpy.types.Object:
    cx, cy, cz = center
    half_height = height * 0.5
    vertices: list[tuple[float, float, float]] = []
    for ring_z in (cz - half_height, cz + half_height):
        for index in range(segments):
            angle = (index / segments) * math.tau
            vertices.append((cx + math.cos(angle) * radius, cy + math.sin(angle) * radius, ring_z))

    faces: list[tuple[int, ...]] = [tuple(range(segments)), tuple(range(segments, segments * 2))]
    for index in range(segments):
        next_index = (index + 1) % segments
        faces.append((index, next_index, next_index + segments, index + segments))

    return create_mesh_object(name, f"{name}Mesh", collection, vertices, faces, material)
