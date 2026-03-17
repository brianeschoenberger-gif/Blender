from __future__ import annotations

import bpy

from house_params import MedievalHouseParams
from medieval_house_builder.common import create_box, create_mesh_object


def _gable_roof(
    name: str,
    width: float,
    depth: float,
    base_z: float,
    ridge_z: float,
    center: tuple[float, float],
    material: bpy.types.Material,
    collection: bpy.types.Collection,
) -> bpy.types.Object:
    cx, cy = center
    x_half = width * 0.5
    y_half = depth * 0.5
    vertices = [
        (cx - x_half, cy - y_half, base_z),
        (cx + x_half, cy - y_half, base_z),
        (cx + x_half, cy + y_half, base_z),
        (cx - x_half, cy + y_half, base_z),
        (cx, cy - y_half, ridge_z),
        (cx, cy + y_half, ridge_z),
    ]
    faces = [
        (0, 1, 4),
        (3, 5, 2),
        (0, 4, 5, 3),
        (1, 2, 5, 4),
        (0, 3, 2, 1),
    ]
    return create_mesh_object(name, f"{name}Mesh", collection, vertices, faces, material)


def _shed_roof(
    name: str,
    width: float,
    depth: float,
    low_z: float,
    high_z: float,
    center: tuple[float, float],
    high_on_negative_x: bool,
    material: bpy.types.Material,
    collection: bpy.types.Collection,
) -> bpy.types.Object:
    cx, cy = center
    x_half = width * 0.5
    y_half = depth * 0.5
    left_z = high_z if high_on_negative_x else low_z
    right_z = low_z if high_on_negative_x else high_z
    vertices = [
        (cx - x_half, cy - y_half, left_z),
        (cx + x_half, cy - y_half, right_z),
        (cx + x_half, cy + y_half, right_z),
        (cx - x_half, cy + y_half, left_z),
        (cx - x_half, cy - y_half, low_z - 0.18),
        (cx + x_half, cy - y_half, low_z - 0.18),
        (cx + x_half, cy + y_half, low_z - 0.18),
        (cx - x_half, cy + y_half, low_z - 0.18),
    ]
    faces = [
        (0, 1, 2, 3),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (3, 0, 4, 7),
    ]
    return create_mesh_object(name, f"{name}Mesh", collection, vertices, faces, material)


def build_main_roof(
    params: MedievalHouseParams,
    collection: bpy.types.Collection,
    materials: dict[str, bpy.types.Material],
) -> list[bpy.types.Object]:
    roof = materials["roof"]
    objects: list[bpy.types.Object] = []
    upper_top = params.base_height + params.ground_floor_height + params.upper_floor_height

    objects.append(
        _gable_roof(
            "House_Roof_Main",
            params.width + params.roof_overhang * 2.0,
            params.depth + params.roof_overhang * 1.55,
            upper_top - 0.10,
            upper_top + params.roof_height,
            (0.0, -0.10),
            roof,
            collection,
        )
    )

    if params.variant_toggles.get("left_lean_to", True):
        objects.append(
            _shed_roof(
                "House_Roof_LeftLeanTo",
                params.left_lean_to_width + params.roof_overhang * 1.35,
                params.depth * 0.56 + params.roof_overhang * 0.95,
                params.base_height + params.ground_floor_height * 0.82,
                params.base_height + params.ground_floor_height + 0.55,
                (-(params.width * 0.5 + params.left_lean_to_width * 0.35), params.depth * 0.02),
                False,
                roof,
                collection,
            )
        )

    if params.variant_toggles.get("right_lean_to", True):
        objects.append(
            _shed_roof(
                "House_Roof_RightPorch",
                params.right_lean_to_width + params.roof_overhang,
                params.depth * 0.36 + params.roof_overhang * 0.65,
                params.base_height + params.ground_floor_height * 0.64,
                params.base_height + params.ground_floor_height + 0.42,
                (params.width * 0.5 + params.right_lean_to_width * 0.12, -params.depth * 0.18),
                True,
                roof,
                collection,
            )
        )

    objects.append(
        _shed_roof(
            "House_Roof_FrontPorch",
            params.width * 0.46 + params.roof_overhang * 1.1,
            params.porch_depth + params.roof_overhang * 0.75,
            params.base_height + params.porch_height,
            params.base_height + params.ground_floor_height + 0.28,
            (0.0, params.depth * 0.5 + params.porch_depth * 0.20),
            True,
            roof,
            collection,
        )
    )
    return objects


def build_chimney(
    params: MedievalHouseParams,
    collection: bpy.types.Collection,
    materials: dict[str, bpy.types.Material],
) -> list[bpy.types.Object]:
    z0 = params.base_height + params.ground_floor_height + params.upper_floor_height + params.roof_height * 0.30
    center = (params.width * 0.18, -params.depth * 0.18, z0 + params.chimney_height * 0.5)
    chimney = create_box(
        "House_Chimney",
        collection,
        (params.chimney_width, params.chimney_depth, params.chimney_height),
        center,
        materials["stone"],
    )
    cap = create_box(
        "House_Chimney_Cap",
        collection,
        (params.chimney_width * 1.18, params.chimney_depth * 1.18, 0.12),
        (center[0], center[1], center[2] + params.chimney_height * 0.5 + 0.04),
        materials["stone"],
    )
    return [chimney, cap]
