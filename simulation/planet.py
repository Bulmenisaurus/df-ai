from dataclasses import dataclass
import math


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
