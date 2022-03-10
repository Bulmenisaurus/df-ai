from typing import Optional

from simulation.planet import Planet
from simulation.utils import distance


class Universe:
    def __init__(self, planets: list[Planet], address: str):

        self.planet_dict: dict[str, Planet] = {p.locationId: p for p in planets}
        self.address = address

    def get_planet_by_id(self, planet_id: str) -> Optional[Planet]:
        return self.planet_dict[planet_id]

    # https://github.com/darkforest-eth/client/blob/54cfeb0ff87cb6ea1f2a13ff888eefd1befdc908/src/Backend/GameLogic/GameManager.ts#L3063-L3086
    def get_planets_in_range(self, planet_id: str, sending_percent=100.0):
        planet = self.planet_dict[planet_id]
        planet_range = planet.get_range(sending_percent)

        planets_in_range = [p for p in self.planet_dict.values() if distance(planet, p) < planet_range]

        return planets_in_range

    def get_my_planets(self):
        return [p for p in self.planet_dict.values() if p.owner == self.address]


    def generate_all_possible_moves(self):
        moves = []
        for planet in self.get_my_planets():
            for used_energy_cap_percent in range(5, round(planet.percent_full), 10):
                for reciever in self.get_planets_in_range(planet.locationId, used_energy_cap_percent):
                    moves.append(
                        [planet.locationId, reciever.locationId, used_energy_cap_percent]
                    )
        return moves