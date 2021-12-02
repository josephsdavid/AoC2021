import numpy as np
from typing import List


class SubmarinePilot(object):

    def __init__(self):
        self.xy = np.array([0, 0])
        self.mapping = {
            "forward": np.array([1, 0]),
            "down": np.array([0, 1]),
            "up": np.array([0, -1])
        }

    def advance(self, instruction: str):
        vector = instruction.split()
        basis = self.mapping[vector[0]]
        magnitude = int(vector[1])
        self.xy += basis * magnitude
        self.xy[np.where(self.xy < 0)] = 0


    def __call__(self):
        return self.xy[0] * self.xy[1]

class AimedPilot(SubmarinePilot):
    def __init__(self):
        self.xy = np.array([0, 0,0])
        self.mapping = {
            "forward": 0,
            "down": 1,
            "up": -1
        }

    def advance(self, instruction: str):
        vector = instruction.split()
        basis = self.mapping[vector[0]]
        magnitude = int(vector[1])
        self.xy[-1] += basis * magnitude
        if vector[0] == "forward":
            self.xy[0] += magnitude
            self.xy[1] += magnitude * self.xy[-1]
        self.xy[1] = max(self.xy[1], 0)



def runner(p: SubmarinePilot, instructions: List[str]) -> int:
    for i in instructions:
        p.advance(i)
    return p()


if __name__ == "__main__":
    from rich import print
    from data import instructions

    test = ["forward 5", "down 5", "forward 8", "up 3", "down 8", "forward 2"]
    pilot = SubmarinePilot()
    if runner(pilot, test) != 150:
        raise ValueError("Test Failed")

    print("Running submarine")
    pilot = SubmarinePilot()
    print(runner(pilot, instructions))

    pilot = AimedPilot()
    if runner(pilot, test) != 900:
        raise ValueError("Test Failed")
    print("Running submarine")
    pilot = AimedPilot()
    print(runner(pilot, instructions))


