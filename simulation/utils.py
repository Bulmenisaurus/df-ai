from simulation.planet import Planet
import math
import numba
from functools import cache


@cache
def distance(from_planet: Planet, to_planet: Planet):
    return _distance(from_planet.x, from_planet.y, to_planet.x, to_planet.y)



@numba.jit(nopython=True)
def _distance(x1: int, y1: int, x2: int, y2: int) -> float:
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

