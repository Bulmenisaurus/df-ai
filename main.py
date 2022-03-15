from simulation.simulation import Universe
from simulation.planet import Planet
import json
import random

with open('./simulation/planets.json', 'r') as file:
    objects = json.load(file)
    planets: list[Planet] = [Planet(**obj) for obj in objects]

universe = Universe(planets, '0x6969a5B0aeCf560282dc5d8A0a9e0e3989d7f29A'.lower())

# TODO: find better way to set individual planet properties for debugging?
universe.planet_dict['0000adb99b421da16417a25122cfefb106125624ccffffeab3a2dbfe96636491'].owner = universe.address
universe.planet_dict['0000adb99b421da16417a25122cfefb106125624ccffffeab3a2dbfe96636491'].energy = 75


all_moves = universe.generate_all_possible_moves()
for i in range(1000):
    move = random.choice(all_moves)

    fromPlanet = universe.get_planet_by_id(move.fromPlanetId)

    if move.energySpent > fromPlanet.energy:
        continue

    universe.make_move(move)
    universe.advance_time(100)


def sort_key(planet: Planet) -> float:
    return planet.energyCap


print('\n'.join([f'{round(p.energy, 1)} / {round(p.energyCap)}' for p in
                 sorted(universe.get_my_planets(), key=sort_key, reverse=True)]))
