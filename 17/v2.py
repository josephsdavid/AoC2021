import numpy as np
import tqdm
from rich import print
import itertools as it
from functools import partial



def read_input(inp: str):
    inp = inp.split(":")[-1]
    split_inp = inp.split(',')
    split_inp = map(lambda x: x.split("=")[-1], split_inp)
    split_inp = map(lambda x: tuple(sorted(map(int, x.split("..")))), split_inp)
    x,y = split_inp
    return x, y

def make_y_probe(y0, vy, n_timesteps = 2500):
    tries = np.arange(n_timesteps)
    for attempt in tries:
        if attempt == 0:
            tries[attempt] = y0
        else:
            tries[attempt] = tries[attempt-1] + vy
            vy -= 1
    return tries

def make_x_probe(x0, vx, n_timesteps = 2500):
    tries = np.arange(n_timesteps)
    for attempt in tries:
        if attempt == 0:
            tries[attempt] = x0
        else:
            tries[attempt] = tries[attempt-1] + vx
            vx -= np.sign(vx)
    return tries


def check_probe(bounds, fn):
    lhs, rhs = bounds
    out = []
    out2 = []
    for v in tqdm.tqdm(range(-5000, 5000)):
        p = fn(0, v)
        idx = np.where((p >= lhs) & (p <= rhs))
        ret = p[idx]
        if ret.size > 0:
            out.append(p)
            out2.append(v)
    return out, out2

check_x_probes = partial(check_probe, fn = make_x_probe)
check_y_probes = partial(check_probe, fn = make_y_probe)


def probe_machine(inp):
    x,y = read_input(inp)
    xprobes, xv = check_x_probes(x)
    yprobes, yv = check_y_probes(y)
    vc = list(it.product(xv, yv))
    out = []
    for i, p in enumerate(tqdm.tqdm(list(it.product(xprobes, yprobes)))):
        ret = np.column_stack(p)
        idx = np.where(((ret[:, 0] >= x[0]) & (ret[:, 0] <= x[1])) & ((ret[:, 1] >= y[0]) & (ret[:, 1] <= y[1])))
        res = ret[idx]
        if res.size > 0:
            out.append(vc[i])
    print(len((out)))
    return out

ret = probe_machine("target area: x=269..292, y=-68..-44")

import pdb; pdb.set_trace() #XXX: Breakpoint




