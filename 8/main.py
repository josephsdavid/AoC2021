from data import test_case, real_deal
import numpy as np
from collections import Counter
from rich import pretty, print
import itertools as it

pretty.install()


def ssorted(s):
    return "".join(sorted(s))


def p1_runner(signal: str) -> int:
    known_digits = {
        2: 1,
        3: 7,
        4: 4,
        7: 8
    }
    out = 0
    for row in signal.splitlines():
        rhs = row.split(' | ')[-1]
        lhs = row.split(' | ')[0]
        mapping = {
            ssorted(s): known_digits[len(s)] for s in lhs.split() if len(s) in known_digits.keys()
        }
        for s in rhs.split():
            if ssorted(s) in mapping.keys():
                out += 1


    return out


def p2_runner(signal: str) -> int:
    out = 0
    known_digits = {
        2: 1,
        3: 7,
        4: 4,
        7: 8
    }
    for row in signal.splitlines():
        id_d = {}
        rhs = row.split(' | ')[-1]
        lhs = row.split(' | ')[0]
        mapping = {known_digits[len(s)]: list(s) for s in lhs.split() if len(s) in known_digits.keys()}
        number_d = {k:("".join(sorted(v))) for k, v in mapping.items()}
        id_d[0] = [x for x in mapping[7] if x not in mapping[1]][0]
        four_count = [[z for z in mapping[4] if z not in xx] for xx in lhs.split() ]
        id_d[3] = [k for k, v in Counter(it.chain(*four_count)).items() if v == 3][0]
        unknown = [x for x in lhs.split() if len(x) not in known_digits.keys()]
        missing_one = [x for x in unknown if len(x) == 6]
        number_d[0] = [ssorted(x) for x in missing_one if id_d[3] not in x][0]
        number_d[6] = [ssorted(x) for x in missing_one if len([z for z in number_d[1] if z in x]) == 1][0]
        number_d[9] = [ssorted(x) for x in missing_one if ssorted(x) not in [number_d[6], number_d[0]]][0]
        unknown = [x for x in lhs.split() if ssorted(x) not in number_d.values()]
        number_d[3] = [ssorted(x) for x in unknown if len([z for z in number_d[4] if z in x]) == 2][0]
        id_d[4] = [x for x in number_d[6] if x not in number_d[9]][0]
        unknown = [x for x in lhs.split() if ssorted(x) not in number_d.values()]
        number_d[5] = [ssorted(x) for x in unknown if id_d[4] not in x][0]
        number_d[2] = [ssorted(x) for x in lhs.split() if ssorted(x) not in number_d.values()][0]
        number_map = {v: k for k,v in number_d.items()}
        num = int("".join([str(number_map[ssorted(x)]) for x in rhs.split()]))
        print(num)
        out += num
    return out


print(p2_runner(test_case))
