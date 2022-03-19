from dataclasses import dataclass
import numba
from functools import cache


@cache
@numba.jit(nopython=True)
def _energy_arriving(planet_distance: float, from_range: float, from_energy_cap: float, sent_energy: float):
    scale = (1 / 2) ** (planet_distance / from_range)
    arriving = scale * sent_energy - 0.05 * from_energy_cap

    return arriving


@dataclass
class Move:
    sender: str
    fromPlanetId: str
    toPlanetId: str
    energySpent: float
    arrivalTime: float
    distance: float
    # ugly
    _fromRange: float
    _fromEnergyCap: float
    id: int = -1

    @property
    def energyArriving(self) -> float:
        # doesn't account for abandoning and wormholes

        arriving = _energy_arriving(self.distance, self._fromRange, self._fromEnergyCap, self.energySpent)

        return max(0, arriving)
