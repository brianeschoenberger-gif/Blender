from __future__ import annotations

import bpy

from house_params import MedievalHouseParams
from medieval_house_builder.common import create_box


def build_door(
    params: MedievalHouseParams,
    collection: bpy.types.Collection,
    materials: dict[str, bpy.types.Material],
) -> list[bpy.types.Object]:
    objects: list[bpy.types.Object] = []
    z = params.base_height + params.door_height * 0.5
    y = params.depth * 0.5 + params.door_depth * 0.42

    objects.append(
        create_box(
            "House_Door_Main",
            collection,
            (params.door_width, params.door_depth, params.door_height),
            (0.0, y, z),
            materials["timber"],
        )
    )
    objects.append(
        create_box(
            "House_Door_Arch",
            collection,
            (params.door_width * 1.25, params.door_depth * 1.1, 0.34),
            (0.0, y + 0.01, params.base_height + params.door_height + 0.12),
            materials["stone"],
        )
    )
    objects.append(
        create_box(
            "House_Door_Frame",
            collection,
            (params.door_width * 1.36, params.door_depth * 0.55, params.door_height + 0.26),
            (0.0, y - 0.04, z + 0.04),
            materials["stone"],
        )
    )
    if params.variant_toggles.get("front_balcony", True):
        balcony_y = params.depth * 0.5 + params.balcony_depth * 0.42
        balcony_z = params.base_height + params.ground_floor_height + params.upper_floor_height * 0.48
        objects.append(
            create_box(
                "House_Balcony",
                collection,
                (params.balcony_width, params.balcony_depth, 0.12),
                (0.0, balcony_y, balcony_z),
                materials["timber"],
            )
        )
        objects.append(
            create_box(
                "House_Balcony_Rail",
                collection,
                (params.balcony_width, 0.08, 0.42),
                (0.0, balcony_y + params.balcony_depth * 0.42, balcony_z + 0.24),
                materials["timber"],
            )
        )
    return objects


def build_windows(
    params: MedievalHouseParams,
    collection: bpy.types.Collection,
    materials: dict[str, bpy.types.Material],
) -> list[bpy.types.Object]:
    objects: list[bpy.types.Object] = []
    glass = materials["glass"]
    timber = materials["timber"]

    placements = [
        ("Front_Left", -params.width * 0.21, params.depth * 0.5 + params.window_depth * 0.45, params.base_height + params.ground_floor_height + params.upper_floor_height * 0.42),
        ("Front_Right", params.width * 0.21, params.depth * 0.5 + params.window_depth * 0.45, params.base_height + params.ground_floor_height + params.upper_floor_height * 0.42),
        ("Front_Gable", 0.0, params.depth * 0.5 + params.window_depth * 0.45, params.base_height + params.ground_floor_height + params.upper_floor_height + params.front_gable_height * 0.36),
        ("Left_Ground", -params.width * 0.5 - params.window_depth * 0.45, params.depth * 0.14, params.base_height + params.ground_floor_height * 0.62),
        ("Left_Upper", -params.width * 0.5 - params.window_depth * 0.45, -params.depth * 0.16, params.base_height + params.ground_floor_height + params.upper_floor_height * 0.45),
        ("Right_Upper", params.width * 0.5 + params.window_depth * 0.45, -params.depth * 0.08, params.base_height + params.ground_floor_height + params.upper_floor_height * 0.40),
        ("Back_Upper", 0.0, -params.depth * 0.5 - params.window_depth * 0.45, params.base_height + params.ground_floor_height + params.upper_floor_height * 0.44),
    ]

    for name, x, y, z in placements:
        size_x = params.window_width * (0.78 if "Gable" in name else 1.0)
        size_y = params.window_depth if "Front" in name or "Back" in name else params.window_depth * 0.9
        size_z = params.window_height * (0.85 if "Ground" in name else 1.0)
        if "Left" in name or "Right" in name:
            size = (size_y, size_x, size_z)
        else:
            size = (size_x, size_y, size_z)

        objects.append(create_box(f"House_Window_{name}", collection, size, (x, y, z), glass))

        frame_depth = 0.08
        if "Left" in name or "Right" in name:
            frame_size = (frame_depth, size_x + 0.18, size_z + 0.16)
        else:
            frame_size = (size_x + 0.18, frame_depth, size_z + 0.16)
        objects.append(create_box(f"House_WindowFrame_{name}", collection, frame_size, (x, y, z), timber))

        if params.variant_toggles.get("flower_boxes", True) and ("Front_Left" in name or "Front_Right" in name):
            objects.append(
                create_box(
                    f"House_FlowerBox_{name}",
                    collection,
                    (size_x * 0.92, 0.22, 0.18),
                    (x, y + 0.08, z - size_z * 0.56),
                    timber,
                )
            )

    return objects
