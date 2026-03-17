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
    hull_length: float = 11.0
    beam: float = 3.18
    hull_height: float = 2.6
    deck_height: float = 0.28
    cabin_roof_height: float = 0.80
    canopy_top_height: float = 0.76
    mast_height: float = 12.4
    boom_length: float = 3.70
    jib_foretriangle_height: float = 9.2
    mast_x: float = 0.36
    boom_z: float = 0.90
    sail_camber: float = 0.14
    main_sail_resolution: tuple[int, int] = (14, 18)
    jib_resolution: tuple[int, int] = (12, 16)
    rail_height: float = 0.95
    stripe_z: tuple[float, float] = (-1.58, -1.38)
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
        (0.00, 0.05, 1.00, 0.13),
        (0.06, 0.14, 0.82, 0.08),
        (0.16, 0.40, 0.46, 0.03),
        (0.32, 0.74, 0.13, 0.00),
        (0.56, 0.92, 0.00, 0.00),
        (0.78, 0.84, 0.02, 0.01),
        (0.92, 0.38, 0.14, 0.04),
        (1.00, 0.08, 0.24, 0.06),
    )
    deck_profile: tuple[tuple[float, float, float], ...] = (
        (0.00, 0.00, 0.01),
        (0.15, 0.12, 0.025),
        (0.35, 0.36, 0.05),
        (0.58, 0.40, 0.05),
        (0.80, 0.22, 0.03),
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
        return self.deck_height + _sample_profile(self.hull_profile, t, 3) * 0.55

    def deck_camber_at(self, t: float) -> float:
        return _sample_profile(self.deck_profile, t, 2)

    def cabin_half_width_at(self, t: float) -> float:
        return self.half_beam_at(t) * _sample_profile(self.deck_profile, t, 1) * 0.62

    def stern_x(self) -> float:
        return -0.5 * self.hull_length

    def bow_x(self) -> float:
        return 0.5 * self.hull_length

    def mast_base_z(self) -> float:
        mast_t = (self.mast_x + (0.5 * self.hull_length)) / self.hull_length
        return self.deck_z_at(mast_t)


DEFAULT_PARAMS = SailboatParams()
