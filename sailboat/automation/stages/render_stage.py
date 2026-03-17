from __future__ import annotations

from pathlib import Path
import sys

import bpy
from mathutils import Vector


CAMERA_NAME = "PipelineCamera"
SUN_NAME = "PipelineSun"
FILL_NAME = "PipelineFill"


def stage_args() -> list[str]:
    if "--" not in sys.argv:
        raise SystemExit("render_stage.py requires scene and preview paths after '--'.")
    return sys.argv[sys.argv.index("--") + 1 :]


def collection_bounds(collection: bpy.types.Collection) -> tuple[Vector, Vector]:
    minimum = Vector((float("inf"), float("inf"), float("inf")))
    maximum = Vector((float("-inf"), float("-inf"), float("-inf")))

    for obj in collection.all_objects:
        if obj.type not in {"MESH", "CURVE"}:
            continue
        for corner in obj.bound_box:
            world_corner = obj.matrix_world @ Vector(corner)
            minimum.x = min(minimum.x, world_corner.x)
            minimum.y = min(minimum.y, world_corner.y)
            minimum.z = min(minimum.z, world_corner.z)
            maximum.x = max(maximum.x, world_corner.x)
            maximum.y = max(maximum.y, world_corner.y)
            maximum.z = max(maximum.z, world_corner.z)

    if minimum.x == float("inf"):
        return Vector((0.0, 0.0, 0.0)), Vector((8.0, 4.0, 6.0))
    return minimum, maximum


def ensure_camera(target_collection: bpy.types.Collection) -> bpy.types.Object:
    camera = bpy.data.objects.get(CAMERA_NAME)
    if camera is None or camera.type != "CAMERA":
        camera_data = bpy.data.cameras.new(CAMERA_NAME)
        camera = bpy.data.objects.new(CAMERA_NAME, camera_data)
        bpy.context.scene.collection.objects.link(camera)

    minimum, maximum = collection_bounds(target_collection)
    center = (minimum + maximum) * 0.5
    size = maximum - minimum
    span = max(size.x, size.y, size.z, 1.0)
    location = center + Vector((span * 1.22, -span * 2.10, span * 0.28))
    target = Vector((center.x, center.y, minimum.z + size.z * 0.16))

    camera.location = location
    camera.rotation_euler = (target - location).to_track_quat("-Z", "Y").to_euler()
    camera.data.lens = 50
    bpy.context.scene.camera = camera
    return camera


def frame_camera(
    camera: bpy.types.Object,
    minimum: Vector,
    maximum: Vector,
    location_factor: tuple[float, float, float],
    target_height_factor: float,
    lens: float,
) -> None:
    center = (minimum + maximum) * 0.5
    size = maximum - minimum
    span = max(size.x, size.y, size.z, 1.0)
    location = center + Vector(
        (
            span * location_factor[0],
            span * location_factor[1],
            span * location_factor[2],
        )
    )
    target = Vector((center.x, center.y, minimum.z + size.z * target_height_factor))
    camera.location = location
    camera.rotation_euler = (target - location).to_track_quat("-Z", "Y").to_euler()
    camera.data.lens = lens


def ensure_sun() -> bpy.types.Object:
    sun = bpy.data.objects.get(SUN_NAME)
    if sun is None or sun.type != "LIGHT":
        light_data = bpy.data.lights.new(SUN_NAME, type="SUN")
        sun = bpy.data.objects.new(SUN_NAME, light_data)
        bpy.context.scene.collection.objects.link(sun)
    sun.location = (7.5, -6.0, 12.0)
    sun.rotation_euler = (0.95, -0.10, 0.42)
    sun.data.energy = 1.8
    return sun


def ensure_fill_light(target_collection: bpy.types.Collection) -> bpy.types.Object:
    fill = bpy.data.objects.get(FILL_NAME)
    if fill is None or fill.type != "LIGHT":
        light_data = bpy.data.lights.new(FILL_NAME, type="AREA")
        fill = bpy.data.objects.new(FILL_NAME, light_data)
        bpy.context.scene.collection.objects.link(fill)

    minimum, maximum = collection_bounds(target_collection)
    center = (minimum + maximum) * 0.5
    size = maximum - minimum
    span = max(size.x, size.y, size.z, 1.0)
    fill.location = center + Vector((-span * 1.05, -span * 0.90, span * 0.55))
    fill.rotation_euler = (1.08, 0.0, -0.95)
    fill.data.energy = 3500.0
    fill.data.shape = "RECTANGLE"
    fill.data.size = span * 0.95
    fill.data.size_y = span * 0.65
    return fill


def ensure_world() -> None:
    scene = bpy.context.scene
    if scene.world is None:
        scene.world = bpy.data.worlds.new("PipelineWorld")
    world = scene.world
    world.use_nodes = True
    nodes = world.node_tree.nodes
    links = world.node_tree.links
    nodes.clear()

    background = nodes.new("ShaderNodeBackground")
    background.inputs["Color"].default_value = (0.74, 0.77, 0.82, 1.0)
    background.inputs["Strength"].default_value = 0.32
    output = nodes.new("ShaderNodeOutputWorld")
    links.new(background.outputs["Background"], output.inputs["Surface"])


def configure_render(preview_path: Path) -> None:
    scene = bpy.context.scene
    engine_items = bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items.keys()
    for engine in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE", "BLENDER_WORKBENCH"):
        if engine in engine_items:
            scene.render.engine = engine
            break

    scene.render.resolution_x = 1600
    scene.render.resolution_y = 900
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = str(preview_path)
    scene.render.film_transparent = False
    scene.view_settings.exposure = -0.35

    if hasattr(scene, "eevee"):
        eevee = scene.eevee
        if hasattr(eevee, "taa_render_samples"):
            eevee.taa_render_samples = 64
        if hasattr(eevee, "shadow_pool_size"):
            eevee.shadow_pool_size = "1024"


def render_to_file(preview_path: Path) -> None:
    bpy.context.scene.render.filepath = str(preview_path)
    bpy.ops.render.render(write_still=True)


def main() -> int:
    args = stage_args()
    if len(args) != 3:
        raise SystemExit(
            "Usage: render_stage.py -- <scene.blend> <preview.png> <hull_preview.png>"
        )

    scene_path = Path(args[0]).resolve()
    preview_path = Path(args[1]).resolve()
    hull_preview_path = Path(args[2]).resolve()
    preview_path.parent.mkdir(parents=True, exist_ok=True)

    bpy.ops.wm.open_mainfile(filepath=str(scene_path))
    target_collection = bpy.data.collections.get("Sailboat")
    if target_collection is None:
        raise SystemExit("Sailboat collection not found in scene.")

    minimum, maximum = collection_bounds(target_collection)
    camera = ensure_camera(target_collection)
    ensure_sun()
    ensure_fill_light(target_collection)
    ensure_world()
    configure_render(preview_path)

    frame_camera(camera, minimum, maximum, (1.22, -2.10, 0.28), 0.16, 50)
    render_to_file(preview_path)

    hull_minimum = minimum.copy()
    hull_maximum = maximum.copy()
    hull_maximum.z = minimum.z + (maximum.z - minimum.z) * 0.36
    frame_camera(camera, hull_minimum, hull_maximum, (1.45, -2.25, 0.12), 0.28, 58)
    render_to_file(hull_preview_path)

    print(f"Rendered preview to {preview_path}")
    print(f"Rendered hull preview to {hull_preview_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
