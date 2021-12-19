import numpy as np
from rich import pretty, print
pretty.install()
from data import test_case, real_deal
from typing import Tuple, List
import itertools as it

def read_data(x: str) -> Tuple[np.ndarray, List[Tuple[int, int]]]:
    vals = [eval(xx)[::-1] for xx in x.splitlines() if ',' in xx]
    arrx = max(list(zip(*vals))[0]) + 1
    arry = max(list(zip(*vals))[1]) + 1
    arr = np.zeros((arrx, arry), dtype = np.int16)
    for v in vals:
        arr[v] = 1

    instructions = [xx for xx in x.splitlines() if '=' in xx]
    instructions = [''.join(filter(lambda x: '=' in x, x.split())) for x in instructions]
    instructions = list(map(lambda x: (0 if x.split('=')[0] == 'y' else 1, int(x.split('=')[1])), instructions))
    return arr, instructions

def fold(x, y):
    print(x.shape)
    yy = y.copy()
    if len(yy) == 0:
        return x
    else:
        axis, pos = yy.pop(0)
        if axis == 0:
            lhs = x[:pos, :].copy()
            rhs = x[pos+1:,:][::-1, :].copy()
            if lhs.shape[0] > rhs.shape[0]:
                rhs = np.row_stack([rhs, np.zeros_like(lhs[0, :])])

        else:
            lhs = x[:, :pos].copy()
            rhs = x[:,pos+1:][:,::-1].copy()
            if lhs.shape[1] > rhs.shape[1]:
                rhs = np.column_stack([rhs, np.zeros_like(lhs[:, 0])])
        x = np.clip(lhs + rhs, 0, 1)
        print(x.shape)
        print(x.sum())
        return fold(x, yy)

arr = fold(*read_data(test_case))
import matplotlib.pyplot as plt

arr = fold(*read_data(real_deal))
plt.matshow(1-arr)
plt.show()
arr = arr.astype(str)
arr[np.where(arr == '1')] = '1'
arr[np.where(arr != '1')] = ' '
arr = arr.tolist()
arr = ["".join(row).replace('1', '*') for row in arr]
print(arr)
import pdb; pdb.set_trace() #XXX: Breakpoint






