from __future__ import annotations

import bpy

from sailboat_params import SailboatParams
from sailboat_builder.common import build_cylinder_between, create_curve_object, create_mesh_object


def _make_cylinder_object(
    name: str,
    collection: bpy.types.Collection,
    start: tuple[float, float, float],
    end: tuple[float, float, float],
    radius: float,
    material: bpy.types.Material,
    parent: bpy.types.Object,
) -> bpy.types.Object:
    vertices, faces = build_cylinder_between(start, end, radius, segments=14)
    return create_mesh_object(
        name,
        collection,
        vertices,
        faces,
        material=material,
        parent=parent,
    )


def _mirror_points(points: list[tuple[float, float, float]]) -> list[tuple[float, float, float]]:
    return [(x, -y, z) for x, y, z in points]


def build_rigging(params: SailboatParams, context: dict) -> dict[str, object]:
    rig_collection = context["collections"]["Rig"]
    materials = context["materials"]
    root_empty = context["root_empty"]

    mast_base = (params.mast_x, 0.0, params.mast_base_z())
    mast_top = (params.mast_x, 0.0, params.mast_base_z() + params.mast_height)
    boom_end = (params.mast_x - params.boom_length, 0.0, params.boom_z)
    bowsprit_tip = (params.bow_x() + 0.16, 0.0, params.deck_z_at(1.0) + 0.36)

    mast = _make_cylinder_object(
        "Mast",
        rig_collection,
        mast_base,
        mast_top,
        0.068,
        materials["metal"],
        root_empty,
    )
    boom = _make_cylinder_object(
        "Boom",
        rig_collection,
        (params.mast_x, 0.0, params.boom_z),
        boom_end,
        0.040,
        materials["metal"],
        root_empty,
    )
    bowsprit = _make_cylinder_object(
        "Bowsprit",
        rig_collection,
        (params.bow_x() - 0.45, 0.0, params.deck_z_at(1.0) + 0.42),
        bowsprit_tip,
        0.032,
        materials["metal"],
        root_empty,
    )

    bow_rail_points = [
        (params.bow_x() - 0.92, 1.02, params.deck_z_at(0.92) + 0.50),
        (params.bow_x() - 0.42, 1.16, params.deck_z_at(0.97) + 0.72),
        (params.bow_x() - 0.06, 0.90, params.deck_z_at(1.0) + 0.57),
    ]
    stern_rail_points = [
        (params.stern_x() + 0.88, 1.02, params.deck_z_at(0.08) + 0.54),
        (params.stern_x() + 0.34, 0.92, params.deck_z_at(0.02) + 0.62),
        (params.stern_x() + 0.04, 0.68, params.deck_z_at(0.0) + 0.42),
    ]
    lifeline_points = [
        (params.stern_x() + 0.82, 1.00, params.deck_z_at(0.08) + params.rail_height),
        (params.stern_x() + 2.55, 1.28, params.deck_z_at(0.28) + params.rail_height),
        (params.mast_x + 0.96, 1.40, params.deck_z_at(0.58) + params.rail_height),
        (params.bow_x() - 0.56, 1.03, params.deck_z_at(0.95) + params.rail_height),
    ]

    bow_rail = create_curve_object(
        "BowRail_Starboard",
        rig_collection,
        bow_rail_points,
        bevel_depth=0.007,
        material=materials["metal"],
        parent=root_empty,
    )
    create_curve_object(
        "BowRail_Port",
        rig_collection,
        _mirror_points(bow_rail_points),
        bevel_depth=0.007,
        material=materials["metal"],
        parent=root_empty,
    )
    stern_rail = create_curve_object(
        "SternRail_Starboard",
        rig_collection,
        stern_rail_points,
        bevel_depth=0.007,
        material=materials["metal"],
        parent=root_empty,
    )
    create_curve_object(
        "SternRail_Port",
        rig_collection,
        _mirror_points(stern_rail_points),
        bevel_depth=0.007,
        material=materials["metal"],
        parent=root_empty,
    )
    lifeline_upper = create_curve_object(
        "LifelineUpper_Starboard",
        rig_collection,
        lifeline_points,
        bevel_depth=0.0021,
        material=materials["metal"],
        parent=root_empty,
    )
    create_curve_object(
        "LifelineUpper_Port",
        rig_collection,
        _mirror_points(lifeline_points),
        bevel_depth=0.0021,
        material=materials["metal"],
        parent=root_empty,
    )
    lifeline_lower = create_curve_object(
        "LifelineLower_Starboard",
        rig_collection,
        [(x, y, z - 0.22) for x, y, z in lifeline_points],
        bevel_depth=0.0018,
        material=materials["metal"],
        parent=root_empty,
    )
    create_curve_object(
        "LifelineLower_Port",
        rig_collection,
        _mirror_points([(x, y, z - 0.22) for x, y, z in lifeline_points]),
        bevel_depth=0.0018,
        material=materials["metal"],
        parent=root_empty,
    )

    stays: list[bpy.types.Object] = []
    if params.detail_toggles["standing_rigging"]:
        stay_specs = [
            ("Forestay", mast_top, (params.bow_x() - 0.10, 0.0, params.deck_z_at(1.0) + 0.27)),
            ("Backstay", mast_top, (params.stern_x() + 0.26, 0.0, params.deck_z_at(0.0) + 0.51)),
            ("ShroudFore_Starboard", (params.mast_x, 0.0, params.mast_base_z() + 9.6), (params.mast_x + 0.30, 1.42, params.deck_z_at(0.62) + 0.12)),
            ("ShroudAft_Starboard", (params.mast_x, 0.0, params.mast_base_z() + 8.4), (params.mast_x - 0.30, 1.34, params.deck_z_at(0.48) + 0.11)),
            ("ShroudFore_Port", (params.mast_x, 0.0, params.mast_base_z() + 9.6), (params.mast_x + 0.30, -1.42, params.deck_z_at(0.62) + 0.12)),
            ("ShroudAft_Port", (params.mast_x, 0.0, params.mast_base_z() + 8.4), (params.mast_x - 0.30, -1.34, params.deck_z_at(0.48) + 0.11)),
        ]
        for name, start, end in stay_specs:
            stays.append(
                create_curve_object(
                    name,
                    rig_collection,
                    [start, end],
                    bevel_depth=0.0019,
                    material=materials["metal"],
                    parent=root_empty,
                )
            )

    return {
        "mast": mast,
        "boom": boom,
        "bowsprit": bowsprit,
        "bow_rail": bow_rail,
        "stern_rail": stern_rail,
        "lifeline_upper": lifeline_upper,
        "lifeline_lower": lifeline_lower,
        "stays": stays,
        "mast_base": mast_base,
        "mast_top": mast_top,
        "boom_end": boom_end,
        "bowsprit_tip": bowsprit_tip,
    }
