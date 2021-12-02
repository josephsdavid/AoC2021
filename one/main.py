from typing import List
import numpy as np


class SonarSweep(object):

    def __init__(self, report: List[int]):
        self.report = np.array(report)
        self.change = self.find_change_in_depth(self.report)
        self.change_sign = np.sign(self.change)

    def find_change_in_depth(self, arr: np.ndarray) -> np.ndarray:
        before = arr[:-1]
        after = arr[1:]
        diff = after - before
        return np.hstack([0, diff])

    def __call__(self):
        return int(np.clip(self.change_sign, 0., 1.).sum())


class SlidingSonarSweep(SonarSweep):

    def __init__(self, report: List[int], winsize: int = 3):
        self.winsize = winsize
        self.report = np.lib.stride_tricks.sliding_window_view(report, self.winsize).sum(1)
        self.change = super().find_change_in_depth(self.report)
        self.change_sign = np.sign(self.change)


if __name__ == "__main__":
    from rich import print
    test = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]

    if SonarSweep(test)() != 7:
        raise ValueError("test failed!")

    from data import report
    print("running part 1!")
    print(SonarSweep(report)())

    if SlidingSonarSweep(test)() != 5:
        raise ValueError("Test Failed!")

    print("Running Part 2!")
    print(SlidingSonarSweep(report)())
