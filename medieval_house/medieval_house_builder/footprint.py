from __future__ import annotations

import bpy

from house_params import MedievalHouseParams
from medieval_house_builder.common import create_box


def build_base(
    params: MedievalHouseParams,
    collection: bpy.types.Collection,
    materials: dict[str, bpy.types.Material],
) -> list[bpy.types.Object]:
    objects: list[bpy.types.Object] = []
    base_height = params.base_height
    objects.append(
        create_box(
            "House_Base",
            collection,
            size=(params.width, params.depth, base_height),
            center=(0.0, 0.0, base_height * 0.5),
            material=materials["stone"],
        )
    )

    left_width = params.left_lean_to_width
    right_width = params.right_lean_to_width
    porch_depth = params.porch_depth

    objects.append(
        create_box(
            "House_Base_LeftWing",
            collection,
            size=(left_width, params.depth * 0.56, base_height * 0.92),
            center=(
                -(params.width * 0.5 + left_width * 0.38),
                params.depth * 0.02,
                base_height * 0.46,
            ),
            material=materials["stone"],
        )
    )
    objects.append(
        create_box(
            "House_Base_FrontPorch",
            collection,
            size=(params.width * 0.42, porch_depth, base_height * 0.7),
            center=(0.0, params.depth * 0.5 + porch_depth * 0.36, base_height * 0.35),
            material=materials["stone"],
        )
    )
    objects.append(
        create_box(
            "House_Base_RightPorch",
            collection,
            size=(right_width, params.depth * 0.34, base_height * 0.6),
            center=(
                params.width * 0.5 + right_width * 0.18,
                -params.depth * 0.18,
                base_height * 0.30,
            ),
            material=materials["stone"],
        )
    )
    return objects
