from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class MedievalHouseParams:
    name: str = "MedievalHouse"
    width: float = 6.8
    depth: float = 9.2
    wall_height: float = 4.8
    roof_height: float = 3.1
    roof_overhang: float = 0.38

    door_width: float = 1.2
    door_height: float = 2.3
    door_depth: float = 0.18

    window_width: float = 1.0
    window_height: float = 1.15
    window_depth: float = 0.12

    chimney_width: float = 0.95
    chimney_depth: float = 0.95
    chimney_height: float = 2.25

    timber_beam_depth: float = 0.12
    timber_beam_width: float = 0.22

    variant_toggles: dict[str, bool] = field(
        default_factory=lambda: {
            "extra_front_beam": True,
            "shutters": True,
            "stone_steps": True,
        }
    )


DEFAULT_PARAMS = MedievalHouseParams()
