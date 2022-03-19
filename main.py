from simulation.simulation import Universe
from simulation.planet import Planet
import json
import random
import time


import cProfile

random.seed(123)

with open('./simulation/planets.json', 'r') as file:
    objects = json.load(file)
    planets: list[Planet] = [Planet(**obj) for obj in objects]

universe = Universe(planets, '0x6969a5B0aeCf560282dc5d8A0a9e0e3989d7f29A'.lower())

# TODO: find better way to set individual planet properties for debugging?
universe.planet_dict['0000adb99b421da16417a25122cfefb106125624ccffffeab3a2dbfe96636491'].owner = universe.address
universe.planet_dict['0000adb99b421da16417a25122cfefb106125624ccffffeab3a2dbfe96636491'].energy = 75


def main():
    all_planets = list(universe.planet_dict.keys())
    random.shuffle(all_planets)

    ROUND_DURATION = 60 * 60 * 10  # 10 hours (or 2 on x5 speed)
    TOTAL_TRANSACTIONS = 200  # 200 total moves

    for i in range(TOTAL_TRANSACTIONS):
        all_moves = universe.generate_all_possible_moves()

        if len(all_moves) == 0:
            continue

        move = random.choice(all_moves)

        fromPlanet = universe.get_planet_by_id(move.fromPlanetId)

        if move.energySpent > fromPlanet.energy:
            continue

        universe.make_move(move)
        universe.advance_time(ROUND_DURATION / TOTAL_TRANSACTIONS)
        print(f'{i}/200 {time.process_time()}')

    def sort_key(planet: Planet) -> float:
        return planet.energyCap

    print('\n'.join([f'{round(p.energy, 1)} / {round(p.energyCap)}' for p in
                     sorted(universe.get_my_planets(), key=sort_key, reverse=True)]))



cProfile.run('main()', sort='time')