from simulation.simulation import Universe
from simulation.planet import Planet
import json

with open('./simulation/planets.json', 'r') as file:
    objects = json.load(file)
    planets: list[Planet] = [Planet(**obj) for obj in objects]

universe = Universe(planets, '0x6969a5B0aeCf560282dc5d8A0a9e0e3989d7f29A'.lower())

# TODO: find better way to set individual planet properties for debugging?
universe.planet_dict['0000adb99b421da16417a25122cfefb106125624ccffffeab3a2dbfe96636491'].owner = universe.address
universe.planet_dict['0000adb99b421da16417a25122cfefb106125624ccffffeab3a2dbfe96636491'].energy = 150

all_moves = universe.generate_all_possible_moves()

print(f'Found {len(all_moves)} possible valid moves. ')
