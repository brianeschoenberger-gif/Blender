from __future__ import annotations

import bpy

from sailboat_params import SailboatParams
from sailboat_builder.common import add_modifier, create_mesh_object


def _build_half_hull_mesh(
    params: SailboatParams,
) -> tuple[list[tuple[float, float, float]], list[tuple[int, int, int, int]]]:
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, int, int, int]] = []

    station_count = 22
    row_count = 8

    for station_index in range(station_count):
        t = station_index / (station_count - 1)
        base_x = params.x_at(t)
        half_beam = params.half_beam_at(t)
        keel_z = params.keel_z_at(t)
        deck_z = params.deck_z_at(t)
        hull_depth = deck_z - keel_z

        chine_z = keel_z + hull_depth * 0.15
        bilge_low_z = keel_z + hull_depth * 0.30
        bilge_high_z = keel_z + hull_depth * 0.48
        lower_topside_z = keel_z + hull_depth * 0.63
        shoulder_z = deck_z - (0.21 + 0.05 * max(0.0, 0.24 - t) + 0.03 * max(0.0, t - 0.82))
        sheer_z = deck_z - 0.05

        bow_rake = max(0.0, (t - 0.83) / 0.17)
        stern_taper = max(0.0, (0.20 - t) / 0.20)
        flare = 0.022 + (0.035 * max(0.0, 0.20 - t)) + (0.014 * max(0.0, t - 0.88))
        deck_edge_y = half_beam * (0.78 if t < 0.08 else 0.84 if t > 0.92 else 0.92)

        x_offsets = (
            stern_taper * 0.05,
            stern_taper * 0.08,
            stern_taper * 0.10 - bow_rake * 0.02,
            stern_taper * 0.13 - bow_rake * 0.07,
            stern_taper * 0.18 - bow_rake * 0.16,
            stern_taper * 0.25 - bow_rake * 0.30,
            stern_taper * 0.33 - bow_rake * 0.46,
            stern_taper * 0.40 - bow_rake * 0.64,
        )

        widths = (
            0.0,
            half_beam * 0.04,
            half_beam * 0.18,
            half_beam * 0.39,
            half_beam * 0.60,
            half_beam * (0.76 + flare * 0.20),
            half_beam * (0.86 + flare * 0.28),
            deck_edge_y,
        )
        heights = (
            keel_z,
            chine_z,
            bilge_low_z,
            bilge_high_z,
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
