from typing import Optional

from functools import cache

from simulation.planet import Planet, PlanetManager
from simulation.utils import distance
from simulation.move import Move


class Universe:
    def __init__(self, planets: list[Planet], address: str):

        self.planet_dict: PlanetManager[str, Planet] = PlanetManager({p.locationId: p for p in planets})
        self.address = address
        self.moves: list[Move] = []
        self._last_move_id = 0
        self.time: float = 0.0

    def get_planet_by_id(self, planet_id: str) -> Optional[Planet]:
        return self.planet_dict[planet_id]

    # https://github.com/darkforest-eth/client/blob/54cfeb0ff87cb6ea1f2a13ff888eefd1befdc908/src/Backend/GameLogic/GameManager.ts#L3063-L3086
    @cache
    def get_planets_in_range(self, planet_id: str, sending_percent=100.0):
        planet = self.planet_dict[planet_id]
        planet_range = planet.get_range(sending_percent)

        planets_in_range = [p for p in self.planet_dict.values(
        ) if distance(planet, p) < planet_range]

        return planets_in_range

    def get_my_planets(self):
        return [self.planet_dict[p] for p in self.planet_dict.keys() if self.planet_dict[p].owner == self.address]


    def get_time_for_move(self, from_id: str, to_id: str):
        from_planet = self.get_planet_by_id(from_id)
        to_planet = self.get_planet_by_id(to_id)

        planet_distance = distance(from_planet, to_planet)

        return planet_distance / (from_planet.speed / 100)

    def _get_move_from_basic_args(self, from_id: str, to_id: str, used_energy_cap_percent: float) -> Move:
        from_planet = self.get_planet_by_id(from_id)
        to_planet = self.get_planet_by_id(to_id)

        energy_used = from_planet.energyCap * (used_energy_cap_percent / 100)

        move_time = self.get_time_for_move(
            from_id,
            to_id
        )

        return Move(
            fromPlanetId=from_id,
            toPlanetId=to_id,
            energySpent=energy_used,
            arrivalTime=self.time + move_time,
            sender=self.address,
            distance=distance(from_planet, to_planet),
            _fromRange=from_planet.range,
            _fromEnergyCap=from_planet.energyCap)

    def generate_all_possible_moves(self) -> list[Move]:
        moves = []
        for planet in self.get_my_planets():
            for used_energy_cap_percent in range(5, round(planet.percent_full), 10):
                for receiver in self.get_planets_in_range(planet.locationId, used_energy_cap_percent):
                    move = self._get_move_from_basic_args(planet.locationId, receiver.locationId,
                                                          used_energy_cap_percent)

                    moves.append(move)
        return moves

    def make_move(self, move: Move):
        if move.energySpent > self.planet_dict[move.fromPlanetId].energy:
            raise ValueError('Tried to move more population than exists')

        self.planet_dict[move.fromPlanetId].execute_move_departure(move)

        self._last_move_id += 1
        move.id = self._last_move_id

        self.moves.append(move)

    def advance_time(self, seconds: float):
        self.time += seconds
        self.planet_dict.time += seconds

        for move in self.moves:
            if move.arrivalTime <= self.time:
                self.planet_dict[move.toPlanetId].execute_move_arrival(move)

                self.moves.remove(move)
