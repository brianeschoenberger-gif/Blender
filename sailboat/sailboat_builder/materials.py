from __future__ import annotations

import bpy

from sailboat_params import SailboatParams


def _new_material(name: str) -> bpy.types.Material:
    material = bpy.data.materials.get(name)
    if material is None:
        material = bpy.data.materials.new(name)
    material.use_nodes = True
    material.node_tree.nodes.clear()
    return material


def _configure_transparency(material: bpy.types.Material) -> None:
    if hasattr(material, "surface_render_method"):
        material.surface_render_method = "BLENDED"
    if hasattr(material, "blend_method"):
        material.blend_method = "BLEND"


def _make_output(material: bpy.types.Material) -> bpy.types.Node:
    nodes = material.node_tree.nodes
    links = material.node_tree.links

    output = nodes.new("ShaderNodeOutputMaterial")
    output.location = (420, 0)
    shader = nodes.new("ShaderNodeBsdfPrincipled")
    shader.location = (80, 0)
    links.new(shader.outputs["BSDF"], output.inputs["Surface"])
    return shader


def _set_principled(
    shader: bpy.types.Node,
    base_color: tuple[float, float, float, float],
    roughness: float,
    metallic: float = 0.0,
    alpha: float = 1.0,
    transmission_weight: float = 0.0,
) -> None:
    shader.inputs["Base Color"].default_value = base_color
    shader.inputs["Roughness"].default_value = roughness
    shader.inputs["Metallic"].default_value = metallic
    shader.inputs["Alpha"].default_value = alpha
    if "Transmission Weight" in shader.inputs:
        shader.inputs["Transmission Weight"].default_value = transmission_weight
    elif "Transmission" in shader.inputs:
        shader.inputs["Transmission"].default_value = transmission_weight


def _hull_material(params: SailboatParams) -> bpy.types.Material:
    material = _new_material("Sailboat_Hull")
    nodes = material.node_tree.nodes
    links = material.node_tree.links

    shader = _make_output(material)
    _set_principled(shader, (0.97, 0.975, 0.98, 1.0), roughness=0.19)

    geometry = nodes.new("ShaderNodeNewGeometry")
    geometry.location = (-900, 40)
    separate_xyz = nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz.location = (-700, 40)
    greater = nodes.new("ShaderNodeMath")
    greater.operation = "GREATER_THAN"
    greater.inputs[1].default_value = params.stripe_z[0]
    greater.location = (-480, 120)
    less = nodes.new("ShaderNodeMath")
    less.operation = "LESS_THAN"
    less.inputs[1].default_value = params.stripe_z[1]
    less.location = (-480, -20)
    multiply = nodes.new("ShaderNodeMath")
    multiply.operation = "MULTIPLY"
    multiply.location = (-260, 50)
    mix = nodes.new("ShaderNodeMixRGB")
    mix.location = (-60, 50)
    mix.inputs["Color1"].default_value = (0.97, 0.975, 0.98, 1.0)
    mix.inputs["Color2"].default_value = (0.02, 0.14, 0.38, 1.0)

    links.new(geometry.outputs["Position"], separate_xyz.inputs["Vector"])
    links.new(separate_xyz.outputs["Z"], greater.inputs[0])
    links.new(separate_xyz.outputs["Z"], less.inputs[0])
    links.new(greater.outputs["Value"], multiply.inputs[0])
    links.new(less.outputs["Value"], multiply.inputs[1])
    links.new(multiply.outputs["Value"], mix.inputs["Fac"])
    links.new(mix.outputs["Color"], shader.inputs["Base Color"])
    return material


def ensure_materials(params: SailboatParams) -> dict[str, bpy.types.Material]:
    hull = _hull_material(params)

    deck = _new_material("Sailboat_Deck")
    deck_shader = _make_output(deck)
    _set_principled(deck_shader, (0.95, 0.93, 0.87, 1.0), roughness=0.42)

    cabin = _new_material("Sailboat_Cabin")
    cabin_shader = _make_output(cabin)
    _set_principled(cabin_shader, (0.94, 0.92, 0.88, 1.0), roughness=0.34)

    sail = _new_material("Sailboat_Sail")
    _configure_transparency(sail)
    sail_shader = _make_output(sail)
    _set_principled(
        sail_shader,
        (0.93, 0.94, 0.93, 1.0),
        roughness=0.62,
        alpha=0.82,
        transmission_weight=0.10,
    )

    window = _new_material("Sailboat_Window")
    _configure_transparency(window)
    window_shader = _make_output(window)
    _set_principled(
        window_shader,
        (0.04, 0.07, 0.10, 1.0),
        roughness=0.09,
        alpha=0.78,
        transmission_weight=0.10,
    )

    canopy = _new_material("Sailboat_Canopy")
    canopy_shader = _make_output(canopy)
    _set_principled(canopy_shader, (0.02, 0.20, 0.52, 1.0), roughness=0.50)

    metal = _new_material("Sailboat_Metal")
    metal_shader = _make_output(metal)
    _set_principled(metal_shader, (0.66, 0.69, 0.73, 1.0), roughness=0.20, metallic=0.95)

    trim = _new_material("Sailboat_Trim")
    trim_shader = _make_output(trim)
    _set_principled(trim_shader, (0.35, 0.22, 0.11, 1.0), roughness=0.46)

    return {
        "hull": hull,
        "deck": deck,
        "cabin": cabin,
        "sail": sail,
        "window": window,
        "canopy": canopy,
        "metal": metal,
        "trim": trim,
    }
