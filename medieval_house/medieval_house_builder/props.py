from __future__ import annotations

import bpy

from house_params import MedievalHouseParams
from medieval_house_builder.common import create_box, create_ngon_cylinder


def build_props(
    params: MedievalHouseParams,
    collection: bpy.types.Collection,
    materials: dict[str, bpy.types.Material],
) -> list[bpy.types.Object]:
    props: list[bpy.types.Object] = []
    stone = materials["stone"]
    timber = materials["timber"]
    plaster = materials["plaster"]

    if params.variant_toggles.get("stone_steps", True):
        step_height = 0.15
        step_depth = 0.34
        for index in range(3):
            props.append(
                create_box(
                    f"House_Step_{index + 1}",
                    collection,
                    (1.9 - index * 0.12, step_depth, step_height),
                    (
                        0.0,
                        params.depth * 0.5 + params.door_depth + 0.18 + index * step_depth * 0.62,
                        step_height * 0.5 + index * step_height,
                    ),
                    stone,
                )
            )

    porch_y = params.depth * 0.5 + params.porch_depth * 0.30
    post_height = params.porch_height
    for idx, x in enumerate((-params.width * 0.16, params.width * 0.16), start=1):
        props.append(
            create_box(
                f"House_PorchPost_{idx}",
                collection,
                (0.14, 0.14, post_height),
                (x, porch_y, params.base_height + post_height * 0.5),
                timber,
            )
        )

    for idx, x in enumerate((-params.width * 0.42, params.width * 0.36), start=1):
        props.append(
            create_ngon_cylinder(
                f"House_Barrel_{idx}",
                collection,
                radius=0.26 if idx == 1 else 0.22,
                height=0.56 if idx == 1 else 0.48,
                center=(x, params.depth * 0.5 + 0.72, 0.28),
                segments=10,
                material=timber,
            )
        )

    props.append(
        create_box(
            "House_Crate",
            collection,
            (0.52, 0.52, 0.42),
            (params.width * 0.34, params.depth * 0.5 + 0.64, 0.21),
            timber,
        )
    )
    props.append(
        create_box(
            "House_Planter_Front",
            collection,
            (0.82, 0.32, 0.26),
            (-params.width * 0.26, params.depth * 0.5 + 0.52, 0.13),
            plaster,
        )
    )
    props.append(
        create_box(
            "House_Planter_Right",
            collection,
            (0.60, 0.28, 0.24),
            (params.width * 0.5 + 0.52, -params.depth * 0.22, 0.12),
            plaster,
        )
    )

    if params.variant_toggles.get("dense_props", True):
        for idx, offset in enumerate((-0.48, 0.0, 0.46), start=1):
            props.append(
                create_box(
                    f"House_FenceFront_{idx}",
                    collection,
                    (0.10, 0.08, 0.82),
                    (offset, params.depth * 0.5 + params.porch_depth + 0.22, 0.41),
                    timber,
                )
            )
        props.append(
            create_box(
                "House_Bench_Left",
                collection,
                (0.92, 0.26, 0.32),
                (-(params.width * 0.5 + 0.68), params.depth * 0.14, 0.16),
                timber,
            )
        )
        props.append(
            create_box(
                "House_LeanTo_Table",
                collection,
                (0.86, 0.48, 0.42),
                (params.width * 0.5 + 0.58, -params.depth * 0.18, 0.21),
                timber,
            )
        )

    return props
