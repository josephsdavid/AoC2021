import numpy as np
from rich import print
from data import test_case, real_deal
from collections import Counter
import itertools as it
import matplotlib.pyplot as plt
from  matplotlib.animation import FuncAnimation


def load_data(d: str):
    return np.array([[float(xx) for xx in x] for x in d.splitlines()])
load_data(test_case)


def find_flashes(a: np.ndarray):
    flash_idxs = np.where(a > 9)
    a[flash_idxs] = 0
    x,y = flash_idxs
    x_list = [x+1, x-1, x]
    y_list = [y+1, y-1, y]
    coords = list(zip(*flash_idxs))
    for c in coords:
        x,y = c
        x_list = [x+1, x-1, x]
        y_list = [y+1, y-1, y]
        prod = it.product(x_list, y_list)
        prod = [p for p in prod if p[0] >= 0 and p[1] >= 0]
        prod = [p for p in prod if p[0] < a.shape[0] and p[1] < a.shape[1]]
        for p in prod:
            if a[p] != 0:
                a[p] += 1
    next_idxs = np.where(a > 9)
    if next_idxs[0].size != 0:
        return find_flashes(a)
    else:
        return a

def run(d, n_iter = 100):
    out = 0
    xx = load_data(d)
    for _ in range(n_iter):
        xx += 1
        xx = find_flashes(xx)
        out += np.where(xx == 0, 1, 0).sum()
    return out

print(run(test_case, 100))
print(run(real_deal, 100))

def find_flashes(a: np.ndarray, ret = []):
    flash_idxs = np.where(a > 9)
    a[flash_idxs] = 0
    ret.append(a.copy())
    x,y = flash_idxs
    x_list = [x+1, x-1, x]
    y_list = [y+1, y-1, y]
    coords = list(zip(*flash_idxs))
    for c in coords:
        x,y = c
        x_list = [x+1, x-1, x]
        y_list = [y+1, y-1, y]
        prod = it.product(x_list, y_list)
        prod = [p for p in prod if p[0] >= 0 and p[1] >= 0]
        prod = [p for p in prod if p[0] < a.shape[0] and p[1] < a.shape[1]]
        for p in prod:
            if a[p] != 0:
                a[p] += 1
    next_idxs = np.where(a > 9)
    if next_idxs[0].size != 0:
        return find_flashes(a, ret)
    else:
        return a, ret


def run_p2(xx, i = 1, ret = []):
    xx += 1
    xx, tmp = find_flashes(xx)
    for t in tmp:
        ret.append(t.copy())
    if np.all(xx == 0):
        return i, ret
    else:
        return run_p2(xx, i+1, ret)

real_deal = load_data(real_deal)
_, llist = (run_p2(real_deal))

data = [9 - x for x in llist]

fig = plt.figure()
plot =plt.matshow(data[0], fignum=0)

def init():
    plot.set_data(data[0])
    return plot

def update(j):
    plot.set_data(data[j])
    return [plot]

anim = FuncAnimation(fig, update, init_func = init, frames=len(data), interval = 1, repeat_delay = 5000)


plt.show()

