from simulation.planet import Planet
import math


def distance(from_planet: Planet, to_planet: Planet):
    return math.sqrt((from_planet.x - to_planet.x) ** 2 + (from_planet.y - to_planet.y) ** 2)
