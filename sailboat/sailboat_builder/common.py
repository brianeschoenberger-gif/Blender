from __future__ import annotations

import math

import bpy
from mathutils import Matrix, Vector


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

    child_names = [child.name for child in collection.children]
    for child_name in child_names:
        delete_collection_tree(child_name)

    object_names = [obj.name for obj in collection.objects]
    for object_name in object_names:
        obj = bpy.data.objects.get(object_name)
        if obj is not None:
            bpy.data.objects.remove(obj, do_unlink=True)

    bpy.data.collections.remove(collection)


def make_empty(
    name: str,
    collection: bpy.types.Collection,
    location: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> bpy.types.Object:
    empty = bpy.data.objects.new(name, None)
    collection.objects.link(empty)
    empty.location = location
    return empty


def assign_material(obj: bpy.types.Object, material: bpy.types.Material) -> None:
    if obj.data is None:
        return
    if obj.data.materials.get(material.name) is None:
        obj.data.materials.append(material)


def create_mesh_object(
    name: str,
    collection: bpy.types.Collection,
    vertices: list[tuple[float, float, float]],
    faces: list[tuple[int, ...]],
    edges: list[tuple[int, int]] | None = None,
    material: bpy.types.Material | None = None,
    parent: bpy.types.Object | None = None,
) -> bpy.types.Object:
    mesh = bpy.data.meshes.new(f"{name}Mesh")
    mesh.from_pydata(vertices, edges or [], faces)
    mesh.validate(verbose=True)
    mesh.update()

    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    obj.parent = parent

    if material is not None:
        assign_material(obj, material)

    for polygon in mesh.polygons:
        polygon.use_smooth = True
    return obj


def create_curve_object(
    name: str,
    collection: bpy.types.Collection,
    points: list[tuple[float, float, float]],
    bevel_depth: float,
    material: bpy.types.Material | None = None,
    parent: bpy.types.Object | None = None,
    cyclic: bool = False,
    resolution_u: int = 12,
) -> bpy.types.Object:
    curve = bpy.data.curves.new(f"{name}Curve", type="CURVE")
    curve.dimensions = "3D"
    curve.resolution_u = resolution_u
    curve.bevel_depth = bevel_depth
    curve.fill_mode = "FULL"

    spline = curve.splines.new("POLY")
    spline.points.add(len(points) - 1)
    for point, coord in zip(spline.points, points):
        point.co = (coord[0], coord[1], coord[2], 1.0)
    spline.use_cyclic_u = cyclic

    obj = bpy.data.objects.new(name, curve)
    collection.objects.link(obj)
    obj.parent = parent
    if material is not None:
        assign_material(obj, material)
    return obj


def add_modifier(
    obj: bpy.types.Object, modifier_type: str, name: str
) -> bpy.types.Modifier:
    return obj.modifiers.new(name=name, type=modifier_type)


def collection_triangle_count(collection: bpy.types.Collection) -> int:
    total = 0
    for obj in collection.all_objects:
        if obj.type != "MESH" or obj.data is None:
            continue
        for polygon in obj.data.polygons:
            total += max(1, len(polygon.vertices) - 2)
    return total


def build_cylinder_between(
    start: tuple[float, float, float],
    end: tuple[float, float, float],
    radius: float,
    segments: int = 12,
) -> tuple[list[tuple[float, float, float]], list[tuple[int, int, int, int]]]:
    start_v = Vector(start)
    end_v = Vector(end)
    axis = end_v - start_v
    length = axis.length
    if length == 0.0:
        raise ValueError("Cylinder endpoints must not be identical.")

    z_axis = axis.normalized()
    reference = Vector((0.0, 0.0, 1.0))
    if abs(z_axis.dot(reference)) > 0.99:
        reference = Vector((0.0, 1.0, 0.0))

    x_axis = z_axis.cross(reference).normalized()
    y_axis = z_axis.cross(x_axis).normalized()
    rotation = Matrix((x_axis, y_axis, z_axis)).transposed()

    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, int, int, int]] = []

    for ring_z in (0.0, length):
        for index in range(segments):
            angle = (index / segments) * math.tau
            local = Vector((math.cos(angle) * radius, math.sin(angle) * radius, ring_z))
            world = start_v + (rotation @ local)
            vertices.append((world.x, world.y, world.z))

    for index in range(segments):
        next_index = (index + 1) % segments
        faces.append((index, next_index, segments + next_index, segments + index))

    return vertices, faces
