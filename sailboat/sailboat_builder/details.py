from __future__ import annotations

import math

import bpy

from sailboat_params import SailboatParams
from sailboat_builder.common import build_cylinder_between, create_curve_object, create_mesh_object


def _make_cylinder(
    name: str,
    collection: bpy.types.Collection,
    start: tuple[float, float, float],
    end: tuple[float, float, float],
    radius: float,
    material: bpy.types.Material,
    parent: bpy.types.Object,
) -> bpy.types.Object:
    vertices, faces = build_cylinder_between(start, end, radius, segments=10)
    return create_mesh_object(
        name,
        collection,
        vertices,
        faces,
        material=material,
        parent=parent,
    )


def _oval_plane(
    center: tuple[float, float, float],
    width: float,
    height: float,
    depth_offset: float,
    segments: int = 12,
) -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    cx, cy, cz = center
    vertices = [(cx, cy + depth_offset, cz)]
    for index in range(segments):
        angle = (index / segments) * math.tau
        x = cx + math.cos(angle) * width * 0.5
        z = cz + math.sin(angle) * height * 0.5
        vertices.append((x, cy + depth_offset, z))
    return vertices, [tuple(range(len(vertices)))]


def _mirror_vertices_y(vertices: list[tuple[float, float, float]]) -> list[tuple[float, float, float]]:
    return [(x, -y, z) for x, y, z in vertices]


def build_details(
    params: SailboatParams,
    context: dict,
    hull_data: dict[str, bpy.types.Object],
    deckhouse_data: dict[str, bpy.types.Object],
    rigging_data: dict[str, object],
    sails_data: dict[str, bpy.types.Object],
) -> dict[str, list[bpy.types.Object]]:
    del hull_data, deckhouse_data

    details_collection = context["collections"]["Details"]
    rig_collection = context["collections"]["Rig"]
    materials = context["materials"]
    root_empty = context["root_empty"]

    created: dict[str, list[bpy.types.Object]] = {
        "portholes": [],
        "stanchions": [],
        "deck_hardware": [],
        "sail_lines": [],
    }

    if params.detail_toggles["portholes"]:
        specs = [
            (params.x_at(0.30), params.half_beam_at(0.30) * 0.98, -0.32, 0.46, 0.16),
            (params.x_at(0.48), params.half_beam_at(0.48) * 0.98, -0.26, 0.56, 0.18),
            (params.x_at(0.66), params.half_beam_at(0.66) * 0.98, -0.26, 0.56, 0.18),
            (params.x_at(0.84), params.half_beam_at(0.84) * 0.98, -0.30, 0.46, 0.16),
        ]
        for index, (x, y, z, width, height) in enumerate(specs, start=1):
            vertices, faces = _oval_plane((x, y, z), width, height, 0.03)
            created["portholes"].append(
                create_mesh_object(
                    f"Porthole_{index:02d}_Starboard",
                    details_collection,
                    vertices,
                    faces,
                    material=materials["window"],
                    parent=root_empty,
                )
            )
            created["portholes"].append(
                create_mesh_object(
                    f"Porthole_{index:02d}_Port",
                    details_collection,
                    _mirror_vertices_y(vertices),
                    faces,
                    material=materials["window"],
                    parent=root_empty,
                )
            )

    if params.detail_toggles["stanchions"]:
        for index, t in enumerate((0.12, 0.24, 0.38, 0.52, 0.68, 0.84), start=1):
            x = params.x_at(t)
            y = params.half_beam_at(t) * 0.96
            z0 = params.deck_z_at(t) + 0.05
            z1 = z0 + params.rail_height - 0.08
            created["stanchions"].append(
                _make_cylinder(
                    f"Stanchion_{index:02d}_Starboard",
                    rig_collection,
                    (x, y, z0),
                    (x, y, z1),
                    0.009,
                    materials["metal"],
                    root_empty,
                )
            )
            created["stanchions"].append(
                _make_cylinder(
                    f"Stanchion_{index:02d}_Port",
                    rig_collection,
                    (x, -y, z0),
                    (x, -y, z1),
                    0.009,
                    materials["metal"],
                    root_empty,
                )
            )

    if params.detail_toggles["cleats"]:
        for index, (x, y, z) in enumerate(
            [
                (params.bow_x() - 0.65, 0.42, params.deck_z_at(0.94) + 0.08),
                (params.stern_x() + 0.72, 0.72, params.deck_z_at(0.08) + 0.08),
            ],
            start=1,
        ):
            created["deck_hardware"].append(
                _make_cylinder(
                    f"CleatBase_{index:02d}",
                    details_collection,
                    (x, y, z),
                    (x, y, z + 0.06),
                    0.05,
                    materials["metal"],
                    root_empty,
                )
            )
            created["deck_hardware"].append(
                _make_cylinder(
                    f"CleatBase_{index:02d}_Port",
                    details_collection,
                    (x, -y, z),
                    (x, -y, z + 0.06),
                    0.05,
                    materials["metal"],
                    root_empty,
                )
            )

    if params.detail_toggles["winches"]:
        for index, (x, y, z) in enumerate(
            [
                (params.x_at(0.34), 0.68, params.deck_z_at(0.34) + 0.10),
                (params.x_at(0.28), 0.92, params.deck_z_at(0.28) + 0.12),
            ],
            start=1,
        ):
            created["deck_hardware"].append(
                _make_cylinder(
                    f"Winch_{index:02d}",
                    details_collection,
                    (x, y, z),
                    (x, y, z + 0.24),
                    0.06,
                    materials["metal"],
                    root_empty,
                )
            )
            created["deck_hardware"].append(
                _make_cylinder(
                    f"Winch_{index:02d}_Port",
                    details_collection,
                    (x, -y, z),
                    (x, -y, z + 0.24),
                    0.06,
                    materials["metal"],
                    root_empty,
                )
            )

    if params.detail_toggles["lifelines"]:
        specs = [
            ("MainHalyard", rigging_data["mast_top"], sails_data["main_head"]),
            ("MainSheet", sails_data["main_clew"], (params.x_at(0.18), 0.0, params.deck_z_at(0.18) + 0.18)),
            ("JibSheet", sails_data["jib_clew"], (params.x_at(0.18), 1.05, params.deck_z_at(0.18) + 0.12)),
        ]
        for name, start, end in specs:
            created["sail_lines"].append(
                create_curve_object(
                    name,
                    rig_collection,
                    [start, end],
                    bevel_depth=0.0016,
                    material=materials["metal"],
                    parent=root_empty,
                )
            )

    return created
