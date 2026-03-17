from __future__ import annotations

import bpy


MATERIAL_NAMES = {
    "timber": "MedievalHouse_Timber",
    "plaster": "MedievalHouse_Plaster",
    "roof": "MedievalHouse_Roof",
    "stone": "MedievalHouse_Stone",
    "metal": "MedievalHouse_Metal",
    "glass": "MedievalHouse_Glass",
}


def _new_material(name: str) -> bpy.types.Material:
    material = bpy.data.materials.get(name)
    if material is None:
        material = bpy.data.materials.new(name)
    material.use_fake_user = True
    material.use_nodes = True
    nodes = material.node_tree.nodes
    nodes.clear()
    return material


def _set_principled(
    material: bpy.types.Material,
    base_color: tuple[float, float, float, float],
    roughness: float,
    metallic: float = 0.0,
    alpha: float = 1.0,
) -> None:
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    shader = nodes.new("ShaderNodeBsdfPrincipled")
    output = nodes.new("ShaderNodeOutputMaterial")

    shader.inputs["Base Color"].default_value = base_color
    shader.inputs["Roughness"].default_value = roughness
    shader.inputs["Metallic"].default_value = metallic
    shader.inputs["Alpha"].default_value = alpha

    links.new(shader.outputs["BSDF"], output.inputs["Surface"])


def ensure_materials() -> dict[str, bpy.types.Material]:
    timber = _new_material(MATERIAL_NAMES["timber"])
    _set_principled(timber, (0.23, 0.12, 0.06, 1.0), roughness=0.68)

    plaster = _new_material(MATERIAL_NAMES["plaster"])
    _set_principled(plaster, (0.78, 0.73, 0.64, 1.0), roughness=0.92)

    roof = _new_material(MATERIAL_NAMES["roof"])
    _set_principled(roof, (0.24, 0.13, 0.08, 1.0), roughness=0.84)

    stone = _new_material(MATERIAL_NAMES["stone"])
    _set_principled(stone, (0.42, 0.41, 0.40, 1.0), roughness=0.95)

    metal = _new_material(MATERIAL_NAMES["metal"])
    _set_principled(metal, (0.27, 0.27, 0.28, 1.0), roughness=0.35, metallic=0.8)

    glass = _new_material(MATERIAL_NAMES["glass"])
    if hasattr(glass, "surface_render_method"):
        glass.surface_render_method = "BLENDED"
    if hasattr(glass, "blend_method"):
        glass.blend_method = "BLEND"
    _set_principled(glass, (0.47, 0.57, 0.66, 1.0), roughness=0.08, alpha=0.45)

    return {
        "timber": timber,
        "plaster": plaster,
        "roof": roof,
        "stone": stone,
        "metal": metal,
        "glass": glass,
    }
