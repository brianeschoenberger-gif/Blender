from __future__ import annotations

from dataclasses import dataclass, field


def _lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def _sample_profile(profile: tuple[tuple[float, ...], ...], t: float, column: int) -> float:
    if t <= profile[0][0]:
        return profile[0][column]
    if t >= profile[-1][0]:
        return profile[-1][column]

    for left, right in zip(profile, profile[1:]):
        if left[0] <= t <= right[0]:
            local_t = (t - left[0]) / (right[0] - left[0])
            return _lerp(left[column], right[column], local_t)

    return profile[-1][column]


@dataclass(frozen=True)
class SailboatParams:
    name: str = "Sailboat"
    hull_length: float = 11.2
    beam: float = 2.94
    hull_height: float = 2.6
    deck_height: float = 0.22
    cabin_roof_height: float = 0.72
    canopy_top_height: float = 0.66
    mast_height: float = 11.6
    boom_length: float = 3.56
    jib_foretriangle_height: float = 8.35
    mast_x: float = 0.30
    boom_z: float = 0.95
    sail_camber: float = 0.12
    main_sail_resolution: tuple[int, int] = (14, 18)
    jib_resolution: tuple[int, int] = (12, 16)
    rail_height: float = 0.95
    stripe_z: tuple[float, float] = (-1.64, -1.48)
    detail_toggles: dict[str, bool] = field(
        default_factory=lambda: {
            "portholes": True,
            "cleats": True,
            "winches": True,
            "stanchions": True,
            "lifelines": True,
            "standing_rigging": True,
        }
    )
    hull_profile: tuple[tuple[float, float, float, float], ...] = (
        (0.00, 0.04, 0.98, 0.12),
        (0.06, 0.11, 0.80, 0.08),
        (0.14, 0.30, 0.49, 0.04),
        (0.28, 0.66, 0.17, 0.00),
        (0.54, 0.90, 0.00, 0.00),
        (0.76, 0.82, 0.01, 0.01),
        (0.90, 0.42, 0.10, 0.04),
        (1.00, 0.07, 0.24, 0.07),
    )
    deck_profile: tuple[tuple[float, float, float], ...] = (
        (0.00, 0.00, 0.01),
        (0.15, 0.10, 0.024),
        (0.35, 0.31, 0.048),
        (0.58, 0.36, 0.046),
        (0.80, 0.19, 0.026),
        (1.00, 0.00, 0.02),
    )
    canopy_profile: tuple[tuple[float, float], ...] = (
        (0.00, 0.01),
        (0.30, 0.05),
        (0.55, 0.08),
        (0.80, 0.04),
        (1.00, 0.01),
    )

    def x_at(self, t: float) -> float:
        return -0.5 * self.hull_length + (self.hull_length * t)

    def half_beam_at(self, t: float) -> float:
        return 0.5 * self.beam * _sample_profile(self.hull_profile, t, 1)

    def keel_z_at(self, t: float) -> float:
        return -1.95 + _sample_profile(self.hull_profile, t, 2) * 1.15

    def deck_z_at(self, t: float) -> float:
        return self.deck_height + _sample_profile(self.hull_profile, t, 3) * 0.48

    def deck_camber_at(self, t: float) -> float:
        return _sample_profile(self.deck_profile, t, 2)

    def cabin_half_width_at(self, t: float) -> float:
        return self.half_beam_at(t) * _sample_profile(self.deck_profile, t, 1) * 0.58

    def stern_x(self) -> float:
        return -0.5 * self.hull_length

    def bow_x(self) -> float:
        return 0.5 * self.hull_length

    def mast_base_z(self) -> float:
        mast_t = (self.mast_x + (0.5 * self.hull_length)) / self.hull_length
        return self.deck_z_at(mast_t)


DEFAULT_PARAMS = SailboatParams()
