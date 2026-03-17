from __future__ import annotations

import bpy

from sailboat_params import SailboatParams
from sailboat_builder.common import add_modifier, create_mesh_object


def _build_half_hull_mesh(
    params: SailboatParams,
) -> tuple[list[tuple[float, float, float]], list[tuple[int, int, int, int]]]:
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, int, int, int]] = []

    station_count = 16
    row_count = 7

    for station_index in range(station_count):
        t = station_index / (station_count - 1)
        base_x = params.x_at(t)
        half_beam = params.half_beam_at(t)
        keel_z = params.keel_z_at(t)
        deck_z = params.deck_z_at(t)
        hull_depth = deck_z - keel_z
        chine_z = keel_z + hull_depth * 0.17
        bilge_z = keel_z + hull_depth * 0.34
        lower_topside_z = keel_z + hull_depth * 0.56
        shoulder_z = deck_z - (0.24 + 0.05 * max(0.0, 0.50 - t) + 0.04 * max(0.0, t - 0.80))
        sheer_z = deck_z - 0.06
        bow_rake = max(0.0, (t - 0.80) / 0.20)
        stern_taper = max(0.0, (0.18 - t) / 0.18)
        flare = 0.02 + (0.04 * max(0.0, 0.16 - t)) + (0.01 * max(0.0, t - 0.88))
        deck_edge_y = half_beam * (0.74 if t < 0.08 else 0.82 if t > 0.92 else 0.90)

        x_offsets = (
            stern_taper * 0.05,
            stern_taper * 0.09,
            stern_taper * 0.11 - bow_rake * 0.03,
            stern_taper * 0.16 - bow_rake * 0.10,
            stern_taper * 0.22 - bow_rake * 0.22,
            stern_taper * 0.32 - bow_rake * 0.38,
            stern_taper * 0.39 - bow_rake * 0.58,
        )

        widths = (
            0.0,
            half_beam * 0.06,
            half_beam * 0.28,
            half_beam * 0.53,
            half_beam * (0.72 + flare * 0.35),
            half_beam * (0.84 + flare * 0.25),
            deck_edge_y,
        )
        heights = (
            keel_z,
            chine_z,
            bilge_z,
            lower_topside_z,
            shoulder_z,
            sheer_z,
            deck_z,
        )

        for x_offset, width, height in zip(x_offsets, widths, heights):
            vertices.append((base_x + x_offset, width, height))

    for station_index in range(station_count - 1):
        for row_index in range(row_count - 1):
            a = station_index * row_count + row_index
            b = a + 1
            c = a + row_count + 1
            d = a + row_count
            faces.append((a, b, c, d))

    return vertices, faces


def build_hull(params: SailboatParams, context: dict) -> dict[str, bpy.types.Object]:
    hull_collection = context["collections"]["Hull"]
    materials = context["materials"]
    root_empty = context["root_empty"]

    vertices, faces = _build_half_hull_mesh(params)
    hull = create_mesh_object(
        "Hull",
        hull_collection,
        vertices,
        faces,
        material=materials["hull"],
        parent=root_empty,
    )

    mirror = add_modifier(hull, "MIRROR", "HullMirror")
    mirror.use_axis[0] = False
    mirror.use_axis[1] = True
    mirror.use_clip = True
    mirror.merge_threshold = 0.0005

    subdiv = add_modifier(hull, "SUBSURF", "HullSubdiv")
    subdiv.levels = 2
    subdiv.render_levels = 2

    return {"hull": hull}
