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

def known_mapper(row: str):
    known_digits = {
        2: 1,
        3: 7,
        4: 4,
        7: 8
    }
    lhs = row.split(' | ')[0]
    mapping = {known_digits[len(s)]: set(s) for s in lhs.split() if len(s) in known_digits.keys()}
    return mapping

def p2_runner(signal: str) -> int:
    base_combos = list(it.permutations(base_dict.items(), 2))
    diffs = [(c[0][0], c[1][0], len(set(c[0][1]).symmetric_difference(set(c[1][1])))) for c in base_combos]
    diff_dict = {}
    for diff in diffs:
        diff_dict.setdefault(diff[-1], []).append((diff[0], diff[1]))
    for row in signal.splitlines():
        lhs = row.split(' | ')[0]
        mapping = known_mapper(row)
        known_map = {ssorted("".join(sorted(v))):k for k, v in mapping.items()}
        unknown = {ssorted(x) for x in lhs.split() if set(x) not in mapping.values()}
        def magic_machine(unknown, mapping, known_map, diff_dict):
            combos = it.product(unknown, mapping.values())
            combos = list(combos)
            setdiffs = list(map(lambda x: (x[0], ''.join(sorted(x[1])), len(set(x[0]).symmetric_difference(x[1]))), combos))
            setdiffs = [(x[0], known_map[x[1]], x[-1]) for x in setdiffs if x[1] in known_map.keys()]
            for k, v in diff_dict.items():
                print(k, len(v))
                if len(v) == 2:
                    of_note = [x for x in setdiffs if x[-1] == k]
                    if len(of_note) != 0:
                        of_note = of_note[0]
                    else:
                        continue
                    replacement = [vv for vv in v if vv[0] == of_note[1]][0]
                    result = replacement[-1]
                    print(of_note[0], result)
                    known_map[result] = ssorted(of_note[0])
                    unknown = {n for n in unknown if n != ssorted(of_note[0])}
                    mapping[result] = set(of_note[0])
                    import pdb; pdb.set_trace() #XXX: Breakpointcombinations itertoos
                    diff_dict = {k: [vv for vv in v if sorted(vv) not in it.combinations(known_map.keys(), 2)] for k, v in diff_dict.items()}
            return unknown, mapping, known_map, diff_dict
        unknown, mapping, known_map, diff_dict = magic_machine(unknown, mapping, known_map, diff_dict)
        print(known_map)
        unknown, mapping, known_map, diff_dict = magic_machine(unknown, mapping, known_map, diff_dict)
        print(known_map)


        import pdb; pdb.set_trace() #XXX: Breakpoint



#def p2_runner(signal: str) -> int:
#    out = 0
#    known_digits = {
#        2: 1,
#        3: 7,
#        4: 4,
#        7: 8
#    }
#    for row in signal.splitlines():
#        id_d = {}
#        rhs = row.split(' | ')[-1]
#        lhs = row.split(' | ')[0]
#        mapping = {known_digits[len(s)]: list(s) for s in lhs.split() if len(s) in known_digits.keys()}
#        number_d = {k:("".join(sorted(v))) for k, v in mapping.items()}
#        id_d[0] = [x for x in mapping[7] if x not in mapping[1]][0]
#        four_count = [[z for z in mapping[4] if z not in xx] for xx in lhs.split() ]
#        id_d[3] = [k for k, v in Counter(it.chain(*four_count)).items() if v == 3][0]
#        unknown = [x for x in lhs.split() if len(x) not in known_digits.keys()]
#        missing_one = [x for x in unknown if len(x) == 6]
#        number_d[0] = [ssorted(x) for x in missing_one if id_d[3] not in x][0]
#        number_d[6] = [ssorted(x) for x in missing_one if len([z for z in number_d[1] if z in x]) == 1][0]
#        number_d[9] = [ssorted(x) for x in missing_one if ssorted(x) not in [number_d[6], number_d[0]]][0]
#        unknown = [x for x in lhs.split() if ssorted(x) not in number_d.values()]
#        number_d[3] = [ssorted(x) for x in unknown if len([z for z in number_d[4] if z in x]) == 2][0]
#        id_d[4] = [x for x in number_d[6] if x not in number_d[9]][0]
#        unknown = [x for x in lhs.split() if ssorted(x) not in number_d.values()]
#        number_d[5] = [ssorted(x) for x in unknown if id_d[4] not in x][0]
#        number_d[2] = [ssorted(x) for x in lhs.split() if ssorted(x) not in number_d.values()][0]
#        number_map = {v: k for k,v in number_d.items()}
#        num = int("".join([str(number_map[ssorted(x)]) for x in rhs.split()]))
#        print(num)
#        out += num
#    return out


print(p2_runner(test_case))
