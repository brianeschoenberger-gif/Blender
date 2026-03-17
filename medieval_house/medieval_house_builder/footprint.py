from __future__ import annotations

import bpy

from house_params import MedievalHouseParams
from medieval_house_builder.common import create_box


def build_base(
    params: MedievalHouseParams,
    collection: bpy.types.Collection,
    materials: dict[str, bpy.types.Material],
) -> bpy.types.Object:
    base_height = 0.45
    return create_box(
        "House_Base",
        collection,
        size=(params.width, params.depth, base_height),
        center=(0.0, 0.0, base_height * 0.5),
        material=materials["stone"],
    )
