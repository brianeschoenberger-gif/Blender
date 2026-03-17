from __future__ import annotations

import bpy

from house_params import MedievalHouseParams
from medieval_house_builder.common import create_mesh_object


def build_main_roof(
    params: MedievalHouseParams,
    collection: bpy.types.Collection,
    materials: dict[str, bpy.types.Material],
) -> bpy.types.Object:
    over = params.roof_overhang
    width = params.width + over * 2.0
    depth = params.depth + over * 2.0

    z0 = 0.45 + params.wall_height
    z_ridge = z0 + params.roof_height
    x_half = width * 0.5
    y_half = depth * 0.5

    vertices = [
        (-x_half, -y_half, z0),
        (x_half, -y_half, z0),
        (x_half, y_half, z0),
        (-x_half, y_half, z0),
        (0.0, -y_half, z_ridge),
        (0.0, y_half, z_ridge),
    ]
    faces = [
        (0, 1, 4),
        (3, 5, 2),
        (0, 4, 5, 3),
        (1, 2, 5, 4),
        (0, 3, 2, 1),
    ]

    return create_mesh_object(
        "House_Roof_Main",
        "HouseRoofMainMesh",
        collection,
        vertices,
        faces,
        materials["roof"],
    )


def build_chimney(
    params: MedievalHouseParams,
    collection: bpy.types.Collection,
    materials: dict[str, bpy.types.Material],
) -> bpy.types.Object:
    from medieval_house_builder.common import create_box

    z0 = 0.45 + params.wall_height + params.roof_height * 0.52
    center = (params.width * 0.20, -params.depth * 0.18, z0 + params.chimney_height * 0.5)

    return create_box(
        "House_Chimney",
        collection,
        (params.chimney_width, params.chimney_depth, params.chimney_height),
        center,
        materials["stone"],
    )
