from __future__ import annotations

import bpy

from sailboat_params import SailboatParams
from sailboat_builder.common import add_modifier, create_mesh_object


def _build_half_hull_mesh(
    params: SailboatParams,
) -> tuple[list[tuple[float, float, float]], list[tuple[int, int, int, int]]]:
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, int, int, int]] = []

    station_count = 14
    row_count = 6

    for station_index in range(station_count):
        t = station_index / (station_count - 1)
        x = params.x_at(t)
        half_beam = params.half_beam_at(t)
        keel_z = params.keel_z_at(t)
        deck_z = params.deck_z_at(t)
        hull_depth = deck_z - keel_z
        chine_z = keel_z + hull_depth * 0.16
        bilge_z = keel_z + hull_depth * 0.38
        shoulder_z = deck_z - (0.24 + 0.04 * (1.0 - abs(t - 0.56) * 1.8))
        flare = 0.03 + (0.07 * max(0.0, 0.18 - t)) + (0.02 * max(0.0, t - 0.84))
        deck_edge_y = half_beam * (0.82 if t < 0.10 else 0.86 if t > 0.90 else 0.92)

        vertices.extend(
            [
                (x, 0.0, keel_z),
                (x, half_beam * 0.06, chine_z),
                (x, half_beam * 0.34, bilge_z),
                (x, half_beam * (0.60 + flare), shoulder_z),
                (x, half_beam * (0.82 + flare * 0.30), deck_z - 0.08),
                (x, deck_edge_y, deck_z),
            ]
        )

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
