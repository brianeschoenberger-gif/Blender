from __future__ import annotations

import bpy

from house_params import MedievalHouseParams
from medieval_house_builder.common import create_box


def build_props(
    params: MedievalHouseParams,
    collection: bpy.types.Collection,
    materials: dict[str, bpy.types.Material],
) -> list[bpy.types.Object]:
    props: list[bpy.types.Object] = []

    if params.variant_toggles.get("stone_steps", True):
        step_height = 0.15
        step_depth = 0.35
        for i in range(3):
            props.append(
                create_box(
                    f"House_Step_{i + 1}",
                    collection,
                    (1.8 - i * 0.12, step_depth, step_height),
                    (
                        0.0,
                        params.depth * 0.5 + params.door_depth + 0.15 + i * (step_depth * 0.55),
                        step_height * 0.5 + i * step_height,
                    ),
                    materials["stone"],
                )
            )

    if params.variant_toggles.get("shutters", True):
        shutter_w = 0.24
        shutter_d = 0.08
        shutter_h = params.window_height + 0.05
        z = 0.45 + params.wall_height * 0.57
        y = params.depth * 0.5 + shutter_d * 0.4
        for idx, x in enumerate((-params.width * 0.28, params.width * 0.28), start=1):
            props.append(
                create_box(
                    f"House_Shutter_Left_{idx}",
                    collection,
                    (shutter_w, shutter_d, shutter_h),
                    (x - (params.window_width * 0.5 + shutter_w * 0.5), y, z),
                    materials["timber"],
                )
            )
            props.append(
                create_box(
                    f"House_Shutter_Right_{idx}",
                    collection,
                    (shutter_w, shutter_d, shutter_h),
                    (x + (params.window_width * 0.5 + shutter_w * 0.5), y, z),
                    materials["timber"],
                )
            )

    return props
