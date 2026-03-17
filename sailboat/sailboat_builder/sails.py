from __future__ import annotations

import math

import bpy
from mathutils import Vector

from sailboat_params import SailboatParams
from sailboat_builder.common import create_mesh_object


def _build_triangular_sail(
    a: tuple[float, float, float],
    b: tuple[float, float, float],
    c: tuple[float, float, float],
    cols: int,
    rows: int,
    camber: float,
    twist: float = 0.0,
    leech_curve_x: float = 0.0,
    leech_curve_z: float = 0.0,
    foot_sag_z: float = 0.0,
    luff_s_curve_x: float = 0.0,
) -> tuple[list[tuple[float, float, float]], list[tuple[int, int, int, int]]]:
    a_v = Vector(a)
    b_v = Vector(b)
    c_v = Vector(c)

    normal = (b_v - a_v).cross(c_v - a_v).normalized()
    if normal.y < 0.0:
        normal = -normal

    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, int, int, int]] = []

    for row in range(rows + 1):
        v = row / rows
        left = a_v.lerp(c_v, v)
        right = b_v.lerp(c_v, v)
        leech_shape = math.sin(math.pi * v)
        right += Vector((-leech_curve_x * leech_shape, 0.0, leech_curve_z * leech_shape))
        left += Vector((luff_s_curve_x * math.sin(math.pi * v) * (0.5 - v), 0.0, 0.0))
        for col in range(cols + 1):
            u = col / cols
            point = left.lerp(right, u)
            fullness = math.sin(math.pi * u) * math.sin(math.pi * (1.0 - v))
            point += normal * (camber * fullness)
            point += Vector((0.0, twist * v * (u - 0.5), 0.0))
            point.z -= foot_sag_z * math.sin(math.pi * u) * ((1.0 - v) ** 1.35)
            vertices.append((point.x, point.y, point.z))

    stride = cols + 1
    for row in range(rows):
        for col in range(cols):
            a_index = row * stride + col
            b_index = a_index + 1
            c_index = a_index + stride + 1
            d_index = a_index + stride
            faces.append((a_index, b_index, c_index, d_index))

    return vertices, faces


def build_sails(
    params: SailboatParams,
    context: dict,
    rigging_data: dict[str, object],
) -> dict[str, bpy.types.Object]:
    sail_collection = context["collections"]["Sails"]
    materials = context["materials"]
    root_empty = context["root_empty"]

    mast_top = rigging_data["mast_top"]
    boom_end = rigging_data["boom_end"]
    mast_base = rigging_data["mast_base"]

    main_head = (mast_top[0] - 0.08, 0.0, mast_top[2] - 1.78)
    main_tack = (params.mast_x - 0.03, 0.0, params.boom_z)
    main_vertices, main_faces = _build_triangular_sail(
        main_tack,
        boom_end,
        main_head,
        cols=params.main_sail_resolution[0],
        rows=params.main_sail_resolution[1],
        camber=params.sail_camber * 0.68,
        twist=0.05,
        leech_curve_x=0.22,
        leech_curve_z=0.16,
        foot_sag_z=0.06,
        luff_s_curve_x=0.02,
    )
    mainsail = create_mesh_object(
        "MainSail",
        sail_collection,
        main_vertices,
        main_faces,
        material=materials["sail"],
        parent=root_empty,
    )

    jib_head = (params.mast_x + 0.06, 0.0, params.mast_base_z() + params.jib_foretriangle_height - 0.80)
    jib_tack = (params.bow_x() - 0.20, 0.0, params.deck_z_at(1.0) + 0.30)
    jib_clew = (params.mast_x + 0.06, 0.0, params.deck_z_at(0.56) + 0.96)
    jib_vertices, jib_faces = _build_triangular_sail(
        jib_tack,
        jib_clew,
        jib_head,
        cols=params.jib_resolution[0],
        rows=params.jib_resolution[1],
        camber=params.sail_camber * 0.34,
        twist=-0.01,
        leech_curve_x=0.12,
        leech_curve_z=0.06,
        foot_sag_z=0.02,
        luff_s_curve_x=0.02,
    )
    jib = create_mesh_object(
        "Jib",
        sail_collection,
        jib_vertices,
        jib_faces,
        material=materials["sail"],
        parent=root_empty,
    )

    return {
        "mainsail": mainsail,
        "jib": jib,
        "jib_head": jib_head,
        "jib_tack": jib_tack,
        "jib_clew": jib_clew,
        "main_head": main_head,
        "main_tack": main_tack,
        "main_clew": boom_end,
        "mast_base": mast_base,
    }
