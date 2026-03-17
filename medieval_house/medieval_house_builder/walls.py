from __future__ import annotations

import bpy

from house_params import MedievalHouseParams
from medieval_house_builder.common import create_box, create_mesh_object


def _gable_panel(
    name: str,
    width: float,
    y: float,
    z_base: float,
    z_peak: float,
    depth: float,
    material: bpy.types.Material,
    collection: bpy.types.Collection,
) -> bpy.types.Object:
    half_width = width * 0.5
    half_depth = depth * 0.5
    vertices = [
        (-half_width, y - half_depth, z_base),
        (half_width, y - half_depth, z_base),
        (0.0, y - half_depth, z_peak),
        (-half_width, y + half_depth, z_base),
        (half_width, y + half_depth, z_base),
        (0.0, y + half_depth, z_peak),
    ]
    faces = [
        (0, 1, 2),
        (3, 5, 4),
        (0, 2, 5, 3),
        (1, 4, 5, 2),
        (0, 3, 4, 1),
    ]
    return create_mesh_object(name, f"{name}Mesh", collection, vertices, faces, material)


def build_walls(
    params: MedievalHouseParams,
    collection: bpy.types.Collection,
    materials: dict[str, bpy.types.Material],
) -> list[bpy.types.Object]:
    objects: list[bpy.types.Object] = []
    stone = materials["stone"]
    plaster = materials["plaster"]

    base_top = params.base_height
    ground_center_z = base_top + params.ground_floor_height * 0.5
    upper_base_z = base_top + params.ground_floor_height
    upper_center_z = upper_base_z + params.upper_floor_height * 0.5

    objects.append(
        create_box(
            "Walls_Ground",
            collection,
            (params.width, params.depth, params.ground_floor_height),
            (0.0, 0.0, ground_center_z),
            stone,
        )
    )
    objects.append(
        create_box(
            "Walls_Upper",
            collection,
            (
                params.width - params.upper_inset * 2.0,
                params.depth - params.upper_inset * 1.4,
                params.upper_floor_height,
            ),
            (0.0, -0.10, upper_center_z),
            plaster,
        )
    )

    gable_half_width = (params.width - params.upper_inset * 1.8) * 0.5
    upper_top = upper_base_z + params.upper_floor_height
    gable_peak_z = upper_top + params.front_gable_height

    front_gable = _gable_panel(
        "Gable_Front",
        params.width - params.upper_inset * 1.8,
        params.depth * 0.5 - params.upper_inset * 0.55,
        upper_top,
        gable_peak_z,
        0.10,
        plaster,
        collection,
    )

    back_gable = _gable_panel(
        "Gable_Back",
        (params.width - params.upper_inset * 1.8) * 0.96,
        -params.depth * 0.5 + params.upper_inset * 0.85,
        upper_top,
        upper_top + params.front_gable_height * 0.78,
        0.10,
        plaster,
        collection,
    )

    if params.variant_toggles.get("left_lean_to", True):
        objects.append(
            create_box(
                "Walls_LeftLeanTo",
                collection,
                (params.left_lean_to_width, params.depth * 0.48, params.ground_floor_height * 0.82),
                (
                    -(params.width * 0.5 + params.left_lean_to_width * 0.38),
                    params.depth * 0.02,
                    base_top + params.ground_floor_height * 0.41,
                ),
                plaster,
            )
        )
    if params.variant_toggles.get("right_lean_to", True):
        objects.append(
            create_box(
                "Walls_RightPorch",
                collection,
                (params.right_lean_to_width, params.depth * 0.30, params.ground_floor_height * 0.64),
                (
                    params.width * 0.5 + params.right_lean_to_width * 0.18,
                    -params.depth * 0.18,
                    base_top + params.ground_floor_height * 0.32,
                ),
                plaster,
            )
        )

    objects.extend([front_gable, back_gable])
    return objects
