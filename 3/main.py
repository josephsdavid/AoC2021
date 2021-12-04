from typing import List, Tuple
import itertools as it
from collections import Counter

InputType = List[str]

class Diagnoser(object):
    def __init__(self, report: InputType):
        self.report = report
        transposed = self.transpose_bits(self.report)
        counted = [Counter(x) for x in transposed]
        gamma = self.calculate_gamma(counted)
        eps = self.calculate_epsilon(counted)
        self.gamma = int(gamma, 2)
        self.eps = int(eps, 2)

    def transpose_bits(self, x: InputType) -> List[Tuple[str]]:
        split = [list(it.chain(*xx)) for xx in x]
        transposed = list(zip(*split))
        return transposed

    def calculate_gamma(self, x: List[Counter]) -> str:
        out = ''
        for cc in x:
            out += cc.most_common()[0][0]
        return out


    def calculate_epsilon(self, x: List[Counter]) -> str:
        out = ''
        for cc in x:
            out += cc.most_common()[-1][0]
        return out

    def __call__(self):
        return self.gamma * self.eps

class LifeSupport(Diagnoser):
    def __init__(self, report: InputType):
        super().__init__(report)
        self.o2 = self.calculate_o2(report)
        self.co2 = self.calculate_co2(report)
        self.o2 = int(self.o2, 2)
        self.co2 = int(self.co2, 2)

    def calculate_o2(self,x: InputType, i: int = 0) -> str:
        if len(x) == 1:
            return x[0]
        transposed = self.transpose_bits(x)
        test = transposed[i]
        indexed = [(x, i) for i, x in enumerate(test)]
        indexed = sorted(indexed, key = lambda x: x[0])
        grouped = {k:[gg[-1] for gg in g] for k, g in it.groupby(indexed, key = lambda x: x[0])}
        if len(grouped['1']) == len(grouped['0']):
            winner = grouped['1']
        elif len(grouped['1']) > len(grouped['0']):
            winner = grouped['1']
        else:
            winner = grouped['0']
        out = [x[idx] for idx in winner]
        return self.calculate_o2(out, i + 1)

    def calculate_co2(self,x: InputType, i: int = 0) -> str:
        if len(x) == 1:
            return x[0]
        transposed = self.transpose_bits(x)
        test = transposed[i]
        indexed = [(x, i) for i, x in enumerate(test)]
        indexed = sorted(indexed, key = lambda x: x[0])
        grouped = {k:[gg[-1] for gg in g] for k, g in it.groupby(indexed, key = lambda x: x[0])}
        if len(grouped['1']) == len(grouped['0']):
            winner = grouped['0']
        elif len(grouped['1']) < len(grouped['0']):
            winner = grouped['1']
        else:
            winner = grouped['0']
        out = [x[idx] for idx in winner]
        return self.calculate_co2(out, i + 1)

    def __call__(self):
        return self.co2 * self.o2








if __name__ == "__main__":
    test_case = ['00100', '11110', '10110', '10111', '10101', '01111', '00111', '11100', '10000', '11001', '00010', '01010']
    Diagnoser(test_case)()

    from data import report
    Diagnoser(report)()

    lfs = LifeSupport(test_case)
    print(lfs.o2)
    print(lfs.co2)
    print(lfs())
    print(LifeSupport(report)())


