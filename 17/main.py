from rich import print
import itertools as it
import numpy as np
import tqdm

print("""
        TODO LIST:
        ACTUALLY SATISFY THE VELOCITY CONDITIONS
        FIX IT TO BE FOR ALL INTEGERS
        """)


def calc_y_pos(a0: int, v0: int, y0: int, maxsize: int = 20000) -> np.ndarray:
    t = np.arange(maxsize)
    pos = y0 + v0*t - 0.5 * a0 * (t**2)
    return pos

def calc_x_pos(v0: int, x0: int, maxsize: int = 20000) -> np.ndarray:
    t = np.arange(maxsize)
    vsub = np.sign(np.abs(v0) - t)
    vsub[np.where(vsub == 0)[0][0]:] = 0
    vsub *= np.sign(v0)
    subtraction_vector = np.add.accumulate(vsub)
    vsub = subtraction_vector
    v = v0 - vsub
    x = x0 + v
    x = np.roll(x, 1)
    pos = np.add.accumulate(x)
    return pos


def trajectory_in_bucket(x0, y0, vx, vy, bounds):
    xpos = calc_x_pos(vx, x0)
    ypos = calc_y_pos(1, vy, y0)
    ret = np.column_stack((xpos, ypos))
    xb, yb = bounds
    idx = np.where(((ret[:, 0] >= xb[0]) & (ret[:, 0] < xb[1])) & ((ret[:, 1] >= yb[0]) & (ret[:, 1] < yb[1])))
    bucket = ret[idx]
    if bucket.size > 0:
        return {'vx': vx, 'vy': vy, 'max_y': ypos.max()}
    else:
        return None




def read_input(inp: str):
    inp = inp.split(":")[-1]
    split_inp = inp.split(',')
    split_inp = map(lambda x: x.split("=")[-1], split_inp)
    split_inp = map(lambda x: tuple(sorted(map(int, x.split("..")))), split_inp)
    x,y = split_inp
    return x, y

def p1_runner(inp: str):
    x0 = 0
    y0 = 0
    bounds = read_input(inp)
    vx = list(range(1, 100))
    vy = list(range(-1000, 0))
    ret = []
    for yv in tqdm.tqdm(vy):
        for xv in tqdm.tqdm(vx):
            out = trajectory_in_bucket(x0, y0, xv, yv, bounds)
            if out is not None:
                ret.append(out)
    return sorted(ret, key = lambda x: x['max_y'], reverse=True)

res = p1_runner("target area: x=269..292, y=-68..-44")


import pdb; pdb.set_trace() #XXX: Breakpoint

