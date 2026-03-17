from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class MedievalHouseParams:
    name: str = "MedievalHouse"
    width: float = 7.6
    depth: float = 9.8
    base_height: float = 0.42
    ground_floor_height: float = 2.9
    upper_floor_height: float = 2.55
    upper_inset: float = 0.24
    front_gable_height: float = 2.95
    roof_height: float = 3.25
    roof_overhang: float = 0.52
    roof_thickness: float = 0.16
    left_lean_to_width: float = 2.2
    right_lean_to_width: float = 1.9
    porch_depth: float = 1.55
    porch_height: float = 1.92

    door_width: float = 1.2
    door_height: float = 2.2
    door_depth: float = 0.18

    window_width: float = 0.86
    window_height: float = 1.05
    window_depth: float = 0.12

    chimney_width: float = 0.82
    chimney_depth: float = 0.82
    chimney_height: float = 2.9

    timber_beam_depth: float = 0.14
    timber_beam_width: float = 0.18
    balcony_depth: float = 0.75
    balcony_width: float = 2.05

    variant_toggles: dict[str, bool] = field(
        default_factory=lambda: {
            "extra_front_beam": True,
            "shutters": True,
            "stone_steps": True,
            "front_balcony": True,
            "left_lean_to": True,
            "right_lean_to": True,
            "dense_props": True,
            "flower_boxes": True,
        }
    )


DEFAULT_PARAMS = MedievalHouseParams()
