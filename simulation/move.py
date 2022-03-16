from dataclasses import dataclass


@dataclass
class Move:
    sender: str
    fromPlanetId: str
    toPlanetId: str
    energySpent: float
    energyArriving: float
    arrivalTime: float
    id: int = -1


