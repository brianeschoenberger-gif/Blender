from __future__ import annotations

import bpy

from house_params import MedievalHouseParams
from medieval_house_builder.common import create_box


def build_walls(
    params: MedievalHouseParams,
    collection: bpy.types.Collection,
    materials: dict[str, bpy.types.Material],
) -> bpy.types.Object:
    wall_z = 0.45 + params.wall_height * 0.5
    return create_box(
        "House_Walls",
        collection,
        size=(params.width, params.depth, params.wall_height),
        center=(0.0, 0.0, wall_z),
        material=materials["plaster"],
    )
