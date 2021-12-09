from data import test_case, real_deal
import numpy as np
from collections import Counter
from rich import pretty, print
import itertools as it

pretty.install()

base_dict = {
        0: 'abcefg',
        1: 'cf',
        2: 'acdeg',
        3: 'acdfg',
        4: 'bcdf',
        5: 'abdfg',
        6: 'abdefg',
        7: 'acf',
        8: 'abcdefg',
        9: 'abcdfg'}

class WireMapper(object):
    def __init__(self):
        base_dict = {
                0: 'abcefg',
                1: 'cf',
                2: 'acdeg',
                3: 'acdfg',
                4: 'bcdf',
                5: 'abdfg',
                6: 'abdefg',
                7: 'acf',
                8: 'abcdefg',
                9: 'abcdfg'}
        len_dict = {k: {"v": v, "len": len(v)} for k, v in base_dict.items()}
        len_counts = Counter([v["len"] for v in len_dict.values()])
        self.len_dict = len_dict
        self.len_counts = len_counts

    def reverse_len_dict(self):
        out = {}
        for k, v in self.len_dict.items():
            out.setdefault(v['len'], []).append(k)
        return out

    def reverse_mapping(self):
        return {v: k for k, v in self.mapping.items()}

    def fit(self, wire: str):
        mapping = {}
        for w in wire.split():
            if self.len_counts[len(w)] == 1:
                mapping["".join(sorted(list(w)))] = self.reverse_len_dict()[len(w)][0]
        self.mapping = mapping

    def predict(self, wire: str) -> str:
        out = ''
        for w in wire.split():
            sw = "".join(sorted(list(w)))
            if sw in self.mapping.keys():
                out += str(self.mapping[sw])
        return out


    def fit_predict(self, wire: str) -> str:
        splitwire = wire.split(' | ')
        self.fit(splitwire[0])
        return self.predict(splitwire[1])

class CrazyWireMapper(WireMapper):
    def __init__(self):
        super().__init__()


    def fit(self, wire: str):
        super().fit(wire)
        most_common = self.len_counts.most_common()
        most_common = list(filter(lambda x: x[-1] != 1, most_common))
        most_common = sorted(most_common, key = lambda x: x[0])
        len_dict = {k[0]:[] for k in most_common}
        for w in wire.split():
            lw = len(w)
            if lw in len_dict.keys(): len_dict[lw].append(w)
        self.fit_six(len_dict)
        self.fit_five(len_dict)


    def fit_five(self, len_dict: dict):
        wire = len_dict[5]
        diff7 = [self.check_setdiff(x,7) for x in wire]
        self.mapping["".join(sorted(list(wire.pop(diff7.index(min(diff7))))))] = 3
        diff9 = [self.check_setdiff(x,9) for x in wire]
        self.mapping["".join(sorted(list(wire.pop(diff9.index(min(diff9))))))] = 5
        self.mapping["".join(sorted(list(wire.pop(0))))] = 2



    def fit_six(self, len_dict: dict):
        wire = len_dict[6]
        # 0 and 9 share a wall with 1, 6 does not
        diff1 = [self.check_setdiff(x,1) for x in wire]
        self.mapping["".join(sorted(list(wire.pop(diff1.index(max(diff1))))))] = 6
        # zero shares less walls with 4 than 9
        diff4 = [self.check_setdiff(x,4) for x in wire]
        self.mapping["".join(sorted(list(wire.pop(diff4.index(max(diff4))))))] = 0
        # 9 is all thats left
        self.mapping["".join(sorted(list(wire.pop(0))))] = 9

    def check_setdiff(self,x: str, key: int):
        setdiff = set(x) - set(self.reverse_mapping()[key])
        return len(setdiff)



class WireRunner(object):
    def __init__(self, wires: str, cls):
        self.wires = wires.splitlines()
        self.results = []
        for w in self.wires:
            self.results.append(cls().fit_predict(w))
    def __call__(self):
        return self.results

def p1_runner(wires: str):
    test = WireRunner(wires, WireMapper)()
    print(test)
    ret = sum([len(x) for x in test])
    print(ret)
    return ret
def p2_runner(wires: str):
    test = WireRunner(wires, CrazyWireMapper)()
    print(sum(map(int, test)))


print("Starting Problem 1!")
#p1_runner(test_case)
#p1_runner(real_deal)

print("starting 2")
p2_runner(test_case)
p2_runner(real_deal)
