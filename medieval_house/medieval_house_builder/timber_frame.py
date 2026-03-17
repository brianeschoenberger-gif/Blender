from __future__ import annotations

import bpy

from house_params import MedievalHouseParams
from medieval_house_builder.common import create_box


def build_timber_frame(
    params: MedievalHouseParams,
    collection: bpy.types.Collection,
    materials: dict[str, bpy.types.Material],
) -> list[bpy.types.Object]:
    beam_mat = materials["timber"]
    beams: list[bpy.types.Object] = []

    wall_mid_z = 0.45 + params.wall_height * 0.5
    top_z = 0.45 + params.wall_height - params.timber_beam_width * 0.5

    beams.append(
        create_box(
            "House_Beam_Top_Front",
            collection,
            (params.width, params.timber_beam_depth, params.timber_beam_width),
            (0.0, params.depth * 0.5 + params.timber_beam_depth * 0.5, top_z),
            beam_mat,
        )
    )
    beams.append(
        create_box(
            "House_Beam_Top_Back",
            collection,
            (params.width, params.timber_beam_depth, params.timber_beam_width),
            (0.0, -params.depth * 0.5 - params.timber_beam_depth * 0.5, top_z),
            beam_mat,
        )
    )

    for idx, x in enumerate((-params.width * 0.25, params.width * 0.25), start=1):
        beams.append(
            create_box(
                f"House_Beam_Vert_Front_{idx}",
                collection,
                (params.timber_beam_width, params.timber_beam_depth, params.wall_height),
                (x, params.depth * 0.5 + params.timber_beam_depth * 0.5, wall_mid_z),
                beam_mat,
            )
        )

    if params.variant_toggles.get("extra_front_beam", True):
        beams.append(
            create_box(
                "House_Beam_Center_Front",
                collection,
                (params.timber_beam_width, params.timber_beam_depth, params.wall_height),
                (0.0, params.depth * 0.5 + params.timber_beam_depth * 0.5, wall_mid_z),
                beam_mat,
            )
        )

    return beams
