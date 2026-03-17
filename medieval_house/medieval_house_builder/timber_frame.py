from __future__ import annotations

import bpy

from house_params import MedievalHouseParams
from medieval_house_builder.common import create_box


def build_timber_frame(
    params: MedievalHouseParams,
    collection: bpy.types.Collection,
    materials: dict[str, bpy.types.Material],
) -> list[bpy.types.Object]:
    beam = materials["timber"]
    objects: list[bpy.types.Object] = []
    bw = params.timber_beam_width
    bd = params.timber_beam_depth

    ground_top = params.base_height + params.ground_floor_height
    upper_top = ground_top + params.upper_floor_height
    front_y = params.depth * 0.5 + bd * 0.5 - params.upper_inset * 0.35
    back_y = -params.depth * 0.5 - bd * 0.5 + params.upper_inset * 0.55

    objects.extend(
        [
            create_box("House_Beam_Top_Front", collection, (params.width - params.upper_inset, bd, bw), (0.0, front_y, upper_top - bw * 0.5), beam),
            create_box("House_Beam_Mid_Front", collection, (params.width - params.upper_inset * 1.4, bd, bw), (0.0, front_y, ground_top + params.upper_floor_height * 0.48), beam),
            create_box("House_Beam_Top_Back", collection, (params.width - params.upper_inset * 1.2, bd, bw), (0.0, back_y, upper_top - bw * 0.5), beam),
        ]
    )

    for idx, x in enumerate((-params.width * 0.26, 0.0, params.width * 0.26), start=1):
        objects.append(
            create_box(
                f"House_Beam_Vert_Front_{idx}",
                collection,
                (bw, bd, params.upper_floor_height),
                (x, front_y, ground_top + params.upper_floor_height * 0.5),
                beam,
            )
        )

    for idx, x in enumerate((-params.width * 0.22, params.width * 0.22), start=1):
        objects.append(
            create_box(
                f"House_Beam_Vert_Back_{idx}",
                collection,
                (bw, bd, params.upper_floor_height * 0.92),
                (x, back_y, ground_top + params.upper_floor_height * 0.46),
                beam,
            )
        )

    diag_height = ground_top + params.upper_floor_height * 0.54
    objects.extend(
        [
            create_box("House_Beam_Diag_Front_Left", collection, (bw, bd, params.upper_floor_height * 0.74), (-params.width * 0.17, front_y, diag_height), beam),
            create_box("House_Beam_Diag_Front_Right", collection, (bw, bd, params.upper_floor_height * 0.74), (params.width * 0.17, front_y, diag_height), beam),
        ]
    )
    objects[-2].rotation_euler[1] = -0.68
    objects[-1].rotation_euler[1] = 0.68

    if params.variant_toggles.get("extra_front_beam", True):
        objects.append(
            create_box(
                "House_Beam_Gable_Center",
                collection,
                (bw, bd, params.front_gable_height * 0.98),
                (0.0, front_y, upper_top + params.front_gable_height * 0.48),
                beam,
            )
        )
        left_diag = create_box(
            "House_Beam_Gable_Left",
            collection,
            (bw, bd, params.front_gable_height * 0.92),
            (-params.width * 0.12, front_y, upper_top + params.front_gable_height * 0.40),
            beam,
        )
        right_diag = create_box(
            "House_Beam_Gable_Right",
            collection,
            (bw, bd, params.front_gable_height * 0.92),
            (params.width * 0.12, front_y, upper_top + params.front_gable_height * 0.40),
            beam,
        )
        left_diag.rotation_euler[1] = -0.58
        right_diag.rotation_euler[1] = 0.58
        objects.extend([left_diag, right_diag])

    side_y_offsets = (params.depth * 0.24, -params.depth * 0.06)
    side_x = params.width * 0.5 + bd * 0.5
    for idx, y in enumerate(side_y_offsets, start=1):
        objects.append(
            create_box(
                f"House_Beam_Vert_Right_{idx}",
                collection,
                (bd, bw, params.ground_floor_height + params.upper_floor_height * 0.54),
                (side_x, y, params.base_height + (params.ground_floor_height + params.upper_floor_height * 0.54) * 0.5),
                beam,
            )
        )
        objects.append(
            create_box(
                f"House_Beam_Vert_Left_{idx}",
                collection,
                (bd, bw, params.ground_floor_height + params.upper_floor_height * 0.64),
                (-side_x, y, params.base_height + (params.ground_floor_height + params.upper_floor_height * 0.64) * 0.5),
                beam,
            )
        )

    return objects
