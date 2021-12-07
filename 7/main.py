from typing import List, Tuple
import numpy as np
from data import crabs
from rich import pretty
pretty.install()

test_case = [16,1,2,0,4,2,7,1,2,14]

def crab_shifter(init: List[int]) -> Tuple[int, int]:
    x = np.array(init)
    base = np.arange(x.min(), x.max() + 1)
    y = np.row_stack([base for _ in range(x.shape[0])])
    fuel_array = (x - y.T)
    fuel_array = np.abs(fuel_array)
    fuel_costs = fuel_array.sum(1)
    return fuel_costs.argmin(), fuel_costs.min()

val, cost = crab_shifter(test_case)
val,cost = crab_shifter(crabs)
print(cost)


def crab_shifter_v2(init: List[int]) -> Tuple[int, int]:
    x = np.array(init)
    base = np.arange(x.min(), x.max() + 1)
    y = np.row_stack([base for _ in range(x.shape[0])])
    fuel_array = (x - y.T)
    fuel_array = np.abs(fuel_array)
    for i in range(fuel_array.shape[0]):
        for j in range(fuel_array.shape[1]):
            fuel_array[i,j] = np.arange(fuel_array[i,j] + 1).sum()
    fuel_costs = fuel_array.sum(1)
    return fuel_costs.argmin(), fuel_costs.min()


def crab_shifter_v2(init: List[int]) -> Tuple[int, int]:
    x = np.array(init)
    base = np.arange(x.min(), x.max() + 1)
    y = np.row_stack([base for _ in range(x.shape[0])])
    fuel_array = (x - y.T)
    fuel_array = np.abs(fuel_array)
    for i in range(fuel_array.shape[0]):
        for j in range(fuel_array.shape[1]):
            fuel_array[i,j] = np.arange(fuel_array[i,j] + 1).sum()
    fuel_costs = fuel_array.sum(1)
    return fuel_costs.argmin(), fuel_costs.min()

crab_shifter_v2(test_case)
crab_shifter_v2(crabs)
