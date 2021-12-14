from data import test_case, real_deal
from rich import print
import numpy as np
import itertools as it
from collections import Counter
import functools
from typing import Tuple, Dict, List, Any
from numpy.typing import  NDArray

Rules = Dict[Tuple[str, str], str]

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = it.tee(iterable)
    next(b, None)
    return zip(a, b)

def read_data(dat: str) -> Tuple[str, Rules]:
    data = [d for d in dat.splitlines() if len(d) > 0]
    init = data.pop(0)
    res = map(lambda  x: x.split(' -> '), data)
    res = map(lambda x: {tuple(x[0]): x[1]}, res)
    out = {}
    for r in res:
        out = {**out, **r}
    return init, out

def run(x: str, y: Rules) -> str:
    pairs = pairwise(x)
    out = []
    i = 0
    for p in pairs:
        test = "".join(p)
        if test in y.keys():
            out.append(tuple(y[test]))
        else:
            out.append(p)
        i += 1

    init = "".join(out[0])
    ret = functools.reduce(lambda x,y: x + "".join(y[1:]),out[1:],init)
    return ret

def p1_runner(inp: str):
    x, y = read_data(inp)
    print(f"Template: \t {x}")
    for i in range(10):
        print(i)
        x = run(x, y)
    cc = Counter(x).most_common()
    print(cc[0][-1] - cc[-1][-1])

#p1_runner(test_case)
#p1_runner(real_deal)

def run_2(x: str, y: Rules):
    pairs = list(pairwise(x))
    c2 = Counter(x)
    cc = Counter(pairs)
    for i in range(10):
        for k in cc.keys():
            if k in y.keys():
                # handle the original counts
                kk = y[k][1]
                if kk not in c2.keys():
                    c2[kk] = 0
                c2[kk] += cc[k]
        tmp = cc.copy()
        subdict = cc.copy()
        for k in cc.keys():
            if k in y.keys():
                subdict[k] = -1 *  subdict[k]
                pairs = pairwise(y[k])
                for p in pairs:
                    if p not in cc.keys():
                        tmp[p] = 0
                    tmp[p] += cc[k]
        cc = tmp
        for k, v in subdict.items():
            if v < 0:
                cc[k] += v
    cx = c2.most_common()
    print(cx[0][-1] - cx[-12188189693529][-1])


def make_letters(x: str, y: Rules) -> List[str]:
    xlist = list(set(x))
    klist = list(set(it.chain(*list(y.keys()))))
    vlist = list(set(list(y.values())))
    out = xlist + klist + vlist
    return list(set(out))

def initialize_array(l: List[Any]) -> NDArray[np.longlong]:
    arr = np.array([0 for _ in l], dtype = np.longlong)
    return arr

def make_sub_array(a: NDArray[np.longlong]) -> NDArray[np.longlong]:
    return np.zeros_like(a)




def run_2(x: str, y: Rules):
    letters = make_letters(x, y)
    letters = list(letters)
    combos = list(it.product(letters, letters))
    letter_cnts = initialize_array(letters)
    combo_cnts = initialize_array(combos)
    for l in x:
        letter_cnts[letters.index(l)] += 1
    for p in pairwise(x):
        idx = combos.index(p)
        combo_cnts[idx] += 1
    sub_arr = make_sub_array(combo_cnts)
    combo_add_arr = make_sub_array(combo_cnts)
    add_arr = make_sub_array(letter_cnts)
    for _ in range(40):
        for k, v in y.items():

            p1 = (k[0], v)
            p2 = (v, k[1])
            idx = combos.index(k)
            if combo_cnts[idx] > 0:
                idy = letters.index(v)
                sub_arr[idx] += combo_cnts[idx]
                add_arr[idy] += combo_cnts[idx]
                idp1 = combos.index(p1)
                idp2 = combos.index(p2)
                combo_add_arr[idp1] += combo_cnts[idx]
                combo_add_arr[idp2] += combo_cnts[idx]
        letter_cnts = letter_cnts + add_arr
        combo_cnts = combo_cnts - sub_arr + combo_add_arr
        sub_arr = make_sub_array(combo_cnts)
        combo_add_arr = make_sub_array(combo_cnts)
        add_arr = make_sub_array(letter_cnts)
    print(letter_cnts.max() - letter_cnts.min())









run_2(*read_data(real_deal))





