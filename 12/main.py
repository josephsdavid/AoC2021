# Python3 program to print all paths of
# source to destination in given graph
from rich import print
from typing import List, Dict
from collections import deque, Counter


def construct_graph(data: str) -> Dict[str, List[str]]:
    out = {}
    for row in data.splitlines():
        splitrow = row.split('-')
        x = splitrow[0]
        y = splitrow[1]
        out.setdefault(x, []).append(y)
        out.setdefault(y, []).append(x)
    return out

def printpath(path: List[str]) -> None:
    print(",".join(path))

def visited(x: str, path: List[str]) -> bool:
    size = len(path)
    for i in range(size):
        if path[i] == x and x != x.upper():
            return True
    return False


def supervisited(x: str, path: List[str]) -> bool:
    cc = Counter(path)
    size = len(path)
    for i in range(size):
        if path[i] == x and x != x.upper():
            if cc[x] < 2 and x not in ["start", "end"] and max([c for k, c in cc.items() if k != k.upper() and k != x]) < 2:
                return False
            else:
                return True

    return False



def pathfinder(g: Dict[str, List[str]], src: str, dst: str, fn = visited) -> List[List[str]]:
    ret = []
    q = deque()
    path = []
    path.append(src)
    q.append(path.copy())

    while q:
        path = q.popleft()
        last = path[-1]
        if (last == dst):
            printpath(path)
            ret.append(path)

        for i in range(len(g[last])):
            if not fn(g[last][i], path):
                newpath = path.copy()
                newpath.append(g[last][i])
                q.append(newpath)
    return ret

if __name__ == "__main__":
    from data import smallest_example, medium_example, large_example, real_deal
    print(construct_graph(smallest_example))
    #xx = pathfinder(construct_graph(smallest_example), 'start', 'end')
    #print(len(xx))
    #xx = pathfinder(construct_graph(medium_example), 'start', 'end')
    #print(len(xx))
    #xx = pathfinder(construct_graph(large_example), 'start', 'end')
    #print(len(xx))
    #xx = pathfinder(construct_graph(real_deal), 'start', 'end')
    #print(len(xx))

    #xx = pathfinder(construct_graph(smallest_example), 'start', 'end', supervisited)
    #print(len(xx))
    #xx = pathfinder(construct_graph(medium_example), 'start', 'end', supervisited)
    #print(len(xx))
    #xx = pathfinder(construct_graph(large_example), 'start', 'end', supervisited)
    #print(len(xx))
    xx = pathfinder(construct_graph(real_deal), 'start', 'end', supervisited)
    print(len(xx))
