from dataclasses import dataclass
from random import randint

@dataclass
class DieThrow:
    value: int
    color: str

class Dice:

    def __init__(self, color, sides = 6):
        self.color = color
        self.sides = sides
        self.last_value = None


    def throw(self) -> DieThrow:
        self.last_value = randint(1, self.sides)
        return DieThrow(self.last_value, self.color)