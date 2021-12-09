from data import test_case, real_deal
from collections import Counter
from typing import List
import itertools as it
from functools import reduce

class LavaAvoider(object):
    def __init__(self, heightmap: str):
        self.valleys = []
        self.risk_factor = []
        self.heightmap = self.generate_dataset(heightmap)


    def generate_dataset(self, heightmap: str) -> List[List[int]]:
        dataset = [[int(x) for x in row] for row in heightmap.splitlines()]
        boundary = max(it.chain(*dataset))
        dataset = [[boundary] + row + [boundary] for row in dataset]
        vert_boundary = [boundary for _ in range(len(dataset[0]))]
        dataset = [vert_boundary] + dataset + [vert_boundary]
        return dataset

    def find_lowpoints(self):
        for idy in range(1, len(self.heightmap) - 1):
            for idx in range(1, len(self.heightmap[0])-1):
                curr = self.heightmap[idy][idx]
                idx_vals = [idx, idx+1, idx-1]
                idy_vals = [idy, idy+1, idy-1]
                combos = list(it.product(idx_vals, idy_vals))
                combos = [c for c in combos if c not in [(idx + 1, idy + 1), (idx -1, idy -1)]]
                values = list(map(lambda x: self.heightmap[x[1]][x[0]], combos))
                if values[0] == min(values) and Counter(values)[values[0]] == 1:
                    self.valleys.append((idx, idy))
                    self.risk_factor.append(values[0] + 1)
    def __call__(self):
        self.find_lowpoints()
        return sum(self.risk_factor)

class BespokeLavaAvoider(LavaAvoider):
    def __init__(self, heightmap):
        super().__init__(heightmap)
        super().find_lowpoints()
        self.basins = []

    def find_basins(self):
        for valley in self.valleys:
            self.basins.append(self.expand([valley]))

    def check_9(self, idx, idy):
        return self.heightmap[idy][idx] != 9

    def expand(self, init):
        tmp = init.copy()
        for (idx, idy) in init:
            if self.check_9(idx+1, idy) and (idx+1, idy) not in tmp:
                tmp.append((idx+1, idy))
            if self.check_9(idx-1, idy) and (idx-1, idy) not in tmp:
                tmp.append((idx-1, idy))
            if self.check_9(idx, idy+1) and (idx, idy+1) not in tmp:
                tmp.append((idx, idy+1))
            if self.check_9(idx, idy-1) and (idx, idy-1) not in tmp:
                tmp.append((idx, idy-1))
        if len(tmp) != len(init):
            return self.expand(tmp)
        else:
            return tmp

    def __call__(self):
        self.find_basins()
        basin_lens = [len(x) for x in self.basins]
        top3 = sorted(basin_lens)[-3:]
        return reduce(lambda x,y : x*y, top3)





if __name__ == "__main__":
    xx = LavaAvoider(test_case)
    print(xx())
    print(LavaAvoider(real_deal)())
    xx = BespokeLavaAvoider(test_case)
    # too many basins!
    print(xx())
    print(BespokeLavaAvoider(real_deal)())



