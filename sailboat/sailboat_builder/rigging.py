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
    bowsprit_tip = (params.bow_x() + 0.20, 0.0, params.deck_z_at(1.0) + 0.40)

    mast = _make_cylinder_object(
        "Mast",
        rig_collection,
        mast_base,
        mast_top,
        0.075,
        materials["metal"],
        root_empty,
    )
    boom = _make_cylinder_object(
        "Boom",
        rig_collection,
        (params.mast_x, 0.0, params.boom_z),
        boom_end,
        0.045,
        materials["metal"],
        root_empty,
    )
    bowsprit = _make_cylinder_object(
        "Bowsprit",
        rig_collection,
        (params.bow_x() - 0.45, 0.0, params.deck_z_at(1.0) + 0.42),
        bowsprit_tip,
        0.035,
        materials["metal"],
        root_empty,
    )

    bow_rail_points = [
        (params.bow_x() - 1.00, 1.10, params.deck_z_at(0.92) + 0.55),
        (params.bow_x() - 0.45, 1.28, params.deck_z_at(0.97) + 0.82),
        (params.bow_x() - 0.05, 0.98, params.deck_z_at(1.0) + 0.62),
    ]
    stern_rail_points = [
        (params.stern_x() + 0.75, 1.12, params.deck_z_at(0.06) + 0.62),
        (params.stern_x() + 0.22, 1.00, params.deck_z_at(0.0) + 0.70),
        (params.stern_x() - 0.08, 0.72, params.deck_z_at(0.0) + 0.48),
    ]
    lifeline_points = [
        (params.stern_x() + 0.70, 1.06, params.deck_z_at(0.07) + params.rail_height),
        (params.stern_x() + 2.40, 1.40, params.deck_z_at(0.25) + params.rail_height),
        (params.mast_x + 0.90, 1.56, params.deck_z_at(0.58) + params.rail_height),
        (params.bow_x() - 0.60, 1.12, params.deck_z_at(0.95) + params.rail_height),
    ]

    bow_rail = create_curve_object(
        "BowRail_Starboard",
        rig_collection,
        bow_rail_points,
        bevel_depth=0.008,
        material=materials["metal"],
        parent=root_empty,
    )
    create_curve_object(
        "BowRail_Port",
        rig_collection,
        _mirror_points(bow_rail_points),
        bevel_depth=0.008,
        material=materials["metal"],
        parent=root_empty,
    )
    stern_rail = create_curve_object(
        "SternRail_Starboard",
        rig_collection,
        stern_rail_points,
        bevel_depth=0.008,
        material=materials["metal"],
        parent=root_empty,
    )
    create_curve_object(
        "SternRail_Port",
        rig_collection,
        _mirror_points(stern_rail_points),
        bevel_depth=0.008,
        material=materials["metal"],
        parent=root_empty,
    )
    lifeline_upper = create_curve_object(
        "LifelineUpper_Starboard",
        rig_collection,
        lifeline_points,
        bevel_depth=0.0025,
        material=materials["metal"],
        parent=root_empty,
    )
    create_curve_object(
        "LifelineUpper_Port",
        rig_collection,
        _mirror_points(lifeline_points),
        bevel_depth=0.0025,
        material=materials["metal"],
        parent=root_empty,
    )
    lifeline_lower = create_curve_object(
        "LifelineLower_Starboard",
        rig_collection,
        [(x, y, z - 0.22) for x, y, z in lifeline_points],
        bevel_depth=0.0020,
        material=materials["metal"],
        parent=root_empty,
    )
    create_curve_object(
        "LifelineLower_Port",
        rig_collection,
        _mirror_points([(x, y, z - 0.22) for x, y, z in lifeline_points]),
        bevel_depth=0.0020,
        material=materials["metal"],
        parent=root_empty,
    )

    stays: list[bpy.types.Object] = []
    if params.detail_toggles["standing_rigging"]:
        stay_specs = [
            ("Forestay", mast_top, (params.bow_x() - 0.12, 0.0, params.deck_z_at(1.0) + 0.25)),
            ("Backstay", mast_top, (params.stern_x() + 0.20, 0.0, params.deck_z_at(0.0) + 0.55)),
            ("ShroudFore_Starboard", (params.mast_x, 0.0, params.mast_base_z() + 9.2), (params.mast_x + 0.25, 1.58, params.deck_z_at(0.62) + 0.12)),
            ("ShroudAft_Starboard", (params.mast_x, 0.0, params.mast_base_z() + 8.0), (params.mast_x - 0.35, 1.50, params.deck_z_at(0.48) + 0.12)),
            ("ShroudFore_Port", (params.mast_x, 0.0, params.mast_base_z() + 9.2), (params.mast_x + 0.25, -1.58, params.deck_z_at(0.62) + 0.12)),
            ("ShroudAft_Port", (params.mast_x, 0.0, params.mast_base_z() + 8.0), (params.mast_x - 0.35, -1.50, params.deck_z_at(0.48) + 0.12)),
        ]
        for name, start, end in stay_specs:
            stays.append(
                create_curve_object(
                    name,
                    rig_collection,
                    [start, end],
                    bevel_depth=0.0022,
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
