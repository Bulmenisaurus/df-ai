from dataclasses import dataclass
import math

import numba

from simulation.move import Move

EMPTY_ADDRESS = "0x0000000000000000000000000000000000000000"


class PlanetManager(dict):
    def __init__(self, *args, **kwargs):
        """
        Class that manages lazy updating planets when they are fetched
        """
        super().__init__(*args, **kwargs)
        self.time = 0

    def __getitem__(self, item) -> 'Planet':
        planet: 'Planet' = dict.__getitem__(self, item)
        if planet.last_updated_at != self.time:
            planet.update(self.time)
            planet.last_updated_at = self.time

        return planet


@numba.jit()
def _get_energy_at_time(energy_growth: float, time_elapsed: float, energy_cap: float, energy: float):
    denominator = math.exp((-4 * energy_growth * time_elapsed) / energy_cap) * \
                  (energy_cap / energy - 1) + \
                  1

    return energy_cap / denominator

@dataclass
class Planet:
    energy: float
    energyCap: float
    energyGrowth: float
    range: float
    defense: float
    speed: float
    locationId: str
    owner: str
    x: int
    y: int
    last_updated_at: int = -1
    _hash: int = -1

    # for caching

    def __hash__(self):
        if self._hash == -1:
            self._hash = hash(self.locationId)
        return self._hash


    # https://github.com/darkforest-eth/packages/blob/71f81ef7aaa05dfb03c3e2914c7b36736f5f84d3/gamelogic/src/planet.ts#L15-L23
    def get_range(self, sending_percent=100.0):
        if sending_percent == 0:
            return 0
        return max(math.log2(sending_percent / 5), 0) * self.range

    def get_move_args(self):
        """
        Get the arguments for this planet that will be fed into the AI
        """

        return self.energy, self.energyCap, self.energyGrowth, self.range, self.defense, self.speed

    @property
    def percent_full(self):
        """
        How much % of the planets energy cap is full
        :return: Percent from 0-100
        """

        return (self.energy / self.energyCap) * 100

    def execute_move_departure(self, move: Move):
        self.energy -= move.energySpent

    # https://github.com/darkforest-eth/client/blob/54cfeb0ff87cb6ea1f2a13ff888eefd1befdc908/src/Backend/GameLogic/ArrivalUtils.ts#L144-L225
    def execute_move_arrival(self, move: Move):
        if self.owner == move.sender:
            # reinforcing
            self.energy += move.energyArriving
        else:
            # attacking

            if self.energy > ((move.energyArriving * 100) / self.defense):
                # not enough to take
                self.energy -= ((move.energyArriving * 100) / self.defense)
            else:
                # captures
                self.owner = move.sender
                self.energy = move.energyArriving - ((self.energy * self.defense) / 100)

        if self.energyGrowth == 0 and self.energy > self.energyCap:
            self.energy = self.energyCap

    def get_energy_at_time(self, time: float):
        if self.energy == 0:
            return 0

        if self.owner == EMPTY_ADDRESS:
            return self.energy

        # TODO: this should be silver bank
        # https://github.com/darkforest-eth/client/blob/54cfeb0ff87cb6ea1f2a13ff888eefd1befdc908/src/Backend/GameLogic/ArrivalUtils.ts#L61-L81
        if self.energyGrowth == 0 and self.energy > self.energyCap:
            return self.energyCap

        time_elapsed = time - self.last_updated_at

        return _get_energy_at_time(self.energyGrowth, time_elapsed, self.energyCap, self.energy)

    def update(self, current_time: float):
        self.energy = self.get_energy_at_time(current_time)
