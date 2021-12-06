import numpy as np
import itertools as it
import ast
from typing import List, Tuple
from rich import print

class VentFinder(object):

    def __init__(self, coords: str):
        split = coords.splitlines()
        split = [s for s in split if len(s) > 0]
        self.coords = [[ast.literal_eval(y) for y in z.split(' -> ')] for z in split]
        max_val = max(list(it.chain(*(it.chain(*self.coords)))))
        self.grid = np.zeros((max_val+1, max_val+1))
        self.find_linear_vents()

    @staticmethod
    def _slope(start: Tuple[int, int], end: Tuple[int, int]) -> Tuple[float, int, int]:
        dy = end[-1]  - start[-1]
        dx = end[0] - start[0]
        return (dy/dx) if dx != 0 else 0, dy, dx

    def find_linear_vents(self):
        for c in self.coords:
            if self._slope(*c)[0] == 0:
                coord_transpose = tuple(zip(*c))
                idxs = list(map(lambda x: np.arange(*sorted(x)), coord_transpose))
                idxs = [coord_transpose[i][0] if idx.size == 0 else np.hstack([idx, idx.max() +1]) for i, idx in enumerate(idxs)]
                self.grid[idxs[0], idxs[1]] += 1

    def __call__(self) -> int:
        return self.grid[np.where(self.grid >= 2)].size

class SuperVentFinder(VentFinder):
    def __init__(self, coords: str):
        super().__init__(coords)
        self.find_diag_vents()

    def find_diag_vents(self):
        for c in self.coords:
            slope, dy, dx = self._slope(*c)
            start = c[0]
            stop = c[1]
            x = start[0]
            y = start[1]
            xe = stop[0]
            ye = stop[1]
            if np.abs(slope) == 1:
                idx = np.arange(x, xe+1) if x < xe else np.arange(xe, x+1)[::-1]
                idy = np.arange(y, ye+1) if y < ye else np.arange(ye, y+1)[::-1]
                for idxx, idyy in zip(idx, idy):
                    self.grid[idxx, idyy] += 1




if __name__ == "__main__":
    test = """
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
9,5 -> 4,0
"""

    print(VentFinder(test)())

    from data import seafloor
    print(VentFinder(seafloor)())
    print(SuperVentFinder(test)())
    print(SuperVentFinder(seafloor)())
    #svf = SuperVentFinder(seafloor)


