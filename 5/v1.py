import numpy as np
import itertools as it
import ast
from typing import List, Tuple
from rich import print


class VentFinder(object):

    def __init__(self, coords: str):
        split = coords.splitlines()
        split = [s for s in split if len(s) > 0]
        coord_tuples = [[ast.literal_eval(y) for y in z.split(' -> ')] for z in split]
        coord_tuples = list(
            filter(lambda x: x[0][0] == x[1][0] or x[0][1] == x[1][1], coord_tuples))
        max_val = max(list(it.chain(*(it.chain(*coord_tuples)))))
        self.grid = np.zeros((max_val+1, max_val+1))
        self.coords = coord_tuples
        self.map_vents(self.coords)

    def map_vents(self, coords: List[List[Tuple[int, int]]]):
        for c in coords:
            print(c)
            coord_transpose = tuple(zip(*c))
            idxs = list(map(lambda x: np.arange(*sorted(x)), coord_transpose))
            max_len = max([len(x) for x in idxs if isinstance(x, np.ndarray)])
            idxs = [np.repeat(coord_transpose[i][0], max_len) if idx.size == 0 else np.hstack([idx, idx.max() +1]) for i, idx in enumerate(idxs)]
            _, dy, dx = self._slope(*c)
            if np.sign(dy) == -1:
                idxs[-1] = idxs[-1][::-1]
            elif np.sign(dx) == -1:
                idxs[0] = idxs[0][::-1]
            for idx in zip(*idxs):
                print(idx)
                self.grid[idx] += 1

    @staticmethod
    def _slope(start: Tuple[int, int], end: Tuple[int, int]) -> Tuple[float, int, int]:
        dy = end[-1]  - start[-1]
        dx = end[0] - start[0]
        return (dy/dx) if dx != 0 else 0, dy, dx

    def __call__(self) -> int:
        return self.grid[np.where(self.grid >= 2)].size


class VentFinderDiag(VentFinder):
    def __init__(self, coords: str):
        split = coords.splitlines()
        split = [s for s in split if len(s) > 0]
        coord_tuples = [[ast.literal_eval(y) for y in z.split(' -> ')] for z in split]
        max_val = max(list(it.chain(*(it.chain(*coord_tuples)))))
        self.grid = np.zeros((max_val+1, max_val+1))
        self.map_vents(coord_tuples)


    def map_vents(self, coords: List[List[Tuple[int, int]]]):
        hcoords = list(
            filter(lambda x: x[0][0] == x[1][0] or x[0][1] == x[1][1], coords))
        super().map_vents(hcoords)
        zcoords = list(filter(lambda x: np.abs(self._slope(*x)[0]) == 1, coords))
        super().map_vents(zcoords)
        import pdb; pdb.set_trace() #XXX: Breakpoint








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
"""

    print(VentFinder(test)())

    from data import seafloor
    #print(VentFinder(seafloor)())

    print(VentFinderDiag(test)())
