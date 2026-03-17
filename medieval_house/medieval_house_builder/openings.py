from __future__ import annotations

import bpy

from house_params import MedievalHouseParams
from medieval_house_builder.common import create_box


def build_door(
    params: MedievalHouseParams,
    collection: bpy.types.Collection,
    materials: dict[str, bpy.types.Material],
) -> bpy.types.Object:
    z = 0.45 + params.door_height * 0.5
    y = params.depth * 0.5 + params.door_depth * 0.45
    return create_box(
        "House_Door_Main",
        collection,
        (params.door_width, params.door_depth, params.door_height),
        (0.0, y, z),
        materials["timber"],
    )


def build_windows(
    params: MedievalHouseParams,
    collection: bpy.types.Collection,
    materials: dict[str, bpy.types.Material],
) -> list[bpy.types.Object]:
    windows: list[bpy.types.Object] = []
    z = 0.45 + params.wall_height * 0.57
    y_front = params.depth * 0.5 + params.window_depth * 0.45
    y_back = -params.depth * 0.5 - params.window_depth * 0.45

    for idx, x in enumerate((-params.width * 0.28, params.width * 0.28), start=1):
        windows.append(
            create_box(
                f"House_Window_Front_{idx}",
                collection,
                (params.window_width, params.window_depth, params.window_height),
                (x, y_front, z),
                materials["glass"],
            )
        )
        windows.append(
            create_box(
                f"House_Window_Back_{idx}",
                collection,
                (params.window_width, params.window_depth, params.window_height),
                (x, y_back, z),
                materials["glass"],
            )
        )

    return windows
