from __future__ import annotations

import bpy

from sailboat_params import SailboatParams
from sailboat_builder.common import add_modifier, create_curve_object, create_mesh_object


def _mirror_points(points: list[tuple[float, float, float]]) -> list[tuple[float, float, float]]:
    return [(x, -y, z) for x, y, z in points]


def _build_half_deck(
    params: SailboatParams,
) -> tuple[list[tuple[float, float, float]], list[tuple[int, int, int, int]]]:
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, int, int, int]] = []
    station_count = 12
    row_count = 3

    for station_index in range(station_count):
        t = station_index / (station_count - 1)
        x = params.x_at(t)
        edge_y = params.half_beam_at(t) * 0.94
        cabin_y = max(params.cabin_half_width_at(t), edge_y * 0.25)
        edge_z = params.deck_z_at(t)
        camber = params.deck_camber_at(t)

        vertices.extend(
            [
                (x, 0.0, edge_z + camber),
                (x, cabin_y, edge_z + camber * 0.36),
                (x, edge_y, edge_z),
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


def _build_half_cabin(
    params: SailboatParams,
) -> tuple[list[tuple[float, float, float]], list[tuple[int, int, int, int]]]:
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, int, int, int]] = []
    cabin_stations = (0.26, 0.39, 0.53, 0.66)
    row_count = 3

    for station_index, t in enumerate(cabin_stations):
        x = params.x_at(t)
        base_z = params.deck_z_at(t)
        width = max(params.cabin_half_width_at(t) * 0.92, 0.30)
        roof_shape = (0.40, 0.58, 0.54, 0.36)[station_index]

        vertices.extend(
            [
                (x, 0.0, base_z + params.cabin_roof_height * roof_shape),
                (x, width * 0.58, base_z + params.cabin_roof_height * (roof_shape * 0.86)),
                (x, width, base_z + 0.04),
            ]
        )

    for station_index in range(len(cabin_stations) - 1):
        for row_index in range(row_count - 1):
            a = station_index * row_count + row_index
            b = a + 1
            c = a + row_count + 1
            d = a + row_count
            faces.append((a, b, c, d))

    return vertices, faces


def _build_half_canopy(
    params: SailboatParams,
) -> tuple[list[tuple[float, float, float]], list[tuple[int, int, int, int]]]:
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, int, int, int]] = []
    section_ts = (0.00, 0.28, 0.62, 1.0)
    canopy_start_x = params.stern_x() + 1.42
    canopy_length = 1.55
    row_count = 2

    for section_t in section_ts:
        x = canopy_start_x + canopy_length * section_t
        hull_t = min(1.0, max(0.0, (x - params.stern_x()) / params.hull_length))
        half_width = max(params.cabin_half_width_at(hull_t) * 1.02, 0.56)
        deck_z = params.deck_z_at(hull_t)
        crown = 0.014 + (0.022 if section_t < 0.65 else 0.010)
        drop = 0.05 + (0.02 * section_t)

        vertices.extend(
            [
                (x, 0.0, deck_z + params.canopy_top_height + crown - drop),
                (x, half_width, deck_z + params.canopy_top_height - drop),
            ]
        )

    for section_index in range(len(section_ts) - 1):
        a = section_index * row_count
        b = a + 1
        c = a + row_count + 1
        d = a + row_count
        faces.append((a, b, c, d))

    return vertices, faces


def _build_half_window_band(
    params: SailboatParams,
) -> tuple[list[tuple[float, float, float]], list[tuple[int, int, int, int]]]:
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, int, int, int]] = []
    section_ts = (0.30, 0.44, 0.58, 0.70)
    row_count = 2

    for t in section_ts:
        x = params.x_at(t)
        width = max(params.cabin_half_width_at(t) * 0.96, 0.28)
        base_z = params.deck_z_at(t) + 0.14
        top_z = base_z + 0.105
        vertices.extend([(x, width, top_z), (x, width * 0.98, base_z)])

    for section_index in range(len(section_ts) - 1):
        a = section_index * row_count
        b = a + 1
        c = a + row_count + 1
        d = a + row_count
        faces.append((a, b, c, d))

    return vertices, faces


def _build_half_windshield(
    params: SailboatParams,
) -> tuple[list[tuple[float, float, float]], list[tuple[int, int, int, int]]]:
    front_t = 0.34
    front_x = params.x_at(front_t)
    width = max(params.cabin_half_width_at(front_t) * 0.80, 0.34)
    base_z = params.deck_z_at(front_t) + 0.21

    vertices = [
        (front_x + 0.08, width * 0.26, base_z + 0.14),
        (front_x - 0.11, width * 0.74, base_z + 0.12),
        (front_x - 0.11, width * 0.77, base_z),
        (front_x + 0.08, width * 0.28, base_z + 0.02),
    ]
    faces = [(0, 1, 2, 3)]
    return vertices, faces


def build_deckhouse(params: SailboatParams, context: dict) -> dict[str, bpy.types.Object]:
    deckhouse_collection = context["collections"]["Deckhouse"]
    canopy_collection = context["collections"]["Canopy"]
    materials = context["materials"]
    root_empty = context["root_empty"]

    deck_vertices, deck_faces = _build_half_deck(params)
    deck = create_mesh_object(
        "Deck",
        deckhouse_collection,
        deck_vertices,
        deck_faces,
        material=materials["deck"],
        parent=root_empty,
    )
    deck_mirror = add_modifier(deck, "MIRROR", "DeckMirror")
    deck_mirror.use_axis[0] = False
    deck_mirror.use_axis[1] = True
    deck_mirror.use_clip = True
    add_modifier(deck, "SUBSURF", "DeckSubdiv").levels = 1

    cabin_vertices, cabin_faces = _build_half_cabin(params)
    cabin = create_mesh_object(
        "Cabin",
        deckhouse_collection,
        cabin_vertices,
        cabin_faces,
        material=materials["cabin"],
        parent=root_empty,
    )
    cabin_mirror = add_modifier(cabin, "MIRROR", "CabinMirror")
    cabin_mirror.use_axis[0] = False
    cabin_mirror.use_axis[1] = True
    cabin_mirror.use_clip = True
    add_modifier(cabin, "SUBSURF", "CabinSubdiv").levels = 1

    window_vertices, window_faces = _build_half_window_band(params)
    cabin_windows = create_mesh_object(
        "CabinWindowBand",
        deckhouse_collection,
        window_vertices,
        window_faces,
        material=materials["window"],
        parent=root_empty,
    )
    window_mirror = add_modifier(cabin_windows, "MIRROR", "WindowMirror")
    window_mirror.use_axis[0] = False
    window_mirror.use_axis[1] = True
    window_mirror.use_clip = True

    canopy_vertices, canopy_faces = _build_half_canopy(params)
    canopy = create_mesh_object(
        "CanopyTop",
        canopy_collection,
        canopy_vertices,
        canopy_faces,
        material=materials["canopy"],
        parent=root_empty,
    )
    canopy_mirror = add_modifier(canopy, "MIRROR", "CanopyMirror")
    canopy_mirror.use_axis[0] = False
    canopy_mirror.use_axis[1] = True
    canopy_mirror.use_clip = True
    add_modifier(canopy, "SUBSURF", "CanopySubdiv").levels = 1

    windshield_vertices, windshield_faces = _build_half_windshield(params)
    windshield = create_mesh_object(
        "Windshield",
        canopy_collection,
        windshield_vertices,
        windshield_faces,
        material=materials["window"],
        parent=root_empty,
    )
    windshield_mirror = add_modifier(windshield, "MIRROR", "WindshieldMirror")
    windshield_mirror.use_axis[0] = False
    windshield_mirror.use_axis[1] = True
    windshield_mirror.use_clip = True

    frame_specs = [
        (
            "CanopyFrontFrame_Starboard",
            [
                (params.stern_x() + 1.48, 0.60, params.deck_z_at(0.20) + 0.09),
                (params.stern_x() + 1.53, 0.64, params.deck_z_at(0.20) + 0.41),
                (params.stern_x() + 1.54, 0.59, params.deck_z_at(0.20) + params.canopy_top_height - 0.04),
            ],
        ),
        (
            "CanopyRearFrame_Starboard",
            [
                (params.stern_x() + 2.22, 0.65, params.deck_z_at(0.27) + 0.06),
                (params.stern_x() + 2.28, 0.70, params.deck_z_at(0.27) + 0.40),
                (params.stern_x() + 2.29, 0.62, params.deck_z_at(0.27) + params.canopy_top_height - 0.06),
            ],
        ),
        (
            "CanopyTopRail_Starboard",
            [
                (params.stern_x() + 1.54, 0.59, params.deck_z_at(0.20) + params.canopy_top_height - 0.04),
                (params.stern_x() + 1.88, 0.66, params.deck_z_at(0.23) + params.canopy_top_height - 0.03),
                (params.stern_x() + 2.29, 0.62, params.deck_z_at(0.27) + params.canopy_top_height - 0.06),
            ],
        ),
    ]
    for name, points in frame_specs:
        create_curve_object(
            name,
            canopy_collection,
            points,
            bevel_depth=0.007,
            material=materials["metal"],
            parent=root_empty,
        )
        create_curve_object(
            name.replace("_Starboard", "_Port"),
            canopy_collection,
            _mirror_points(points),
            bevel_depth=0.007,
            material=materials["metal"],
            parent=root_empty,
        )

    aft_span_points = [
        (params.stern_x() + 2.22, -0.62, params.deck_z_at(0.27) + params.canopy_top_height - 0.06),
        (params.stern_x() + 2.27, 0.0, params.deck_z_at(0.27) + params.canopy_top_height - 0.04),
        (params.stern_x() + 2.22, 0.62, params.deck_z_at(0.27) + params.canopy_top_height - 0.06),
    ]
    create_curve_object(
        "CanopyAftSpan",
        canopy_collection,
        aft_span_points,
        bevel_depth=0.006,
        material=materials["metal"],
        parent=root_empty,
    )

    return {
        "deck": deck,
        "cabin": cabin,
        "cabin_windows": cabin_windows,
        "canopy": canopy,
        "windshield": windshield,
    }
