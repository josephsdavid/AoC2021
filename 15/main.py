import itertools as it
import numpy as np
from data import test_case, real_deal
from collections import deque, defaultdict
from rich import print
url = "https://blog.finxter.com/python-a-the-simple-guide-to-the-a-star-search-algorithm/"

def load_data(dat: str) -> np.ndarray:
   return np.array([list(map(int, x)) for x in dat.splitlines()])

def indices_graph(arr: np.ndarray):
    indices = list(it.product(*map(np.arange, arr.shape)))
    out = {}
    for (x,y) in indices:
        n = (x, y+1)
        s = (x, y-1)
        e = (x+1, y)
        w = (x-1, y)
        for case in [n,s,e,w]:
            if  case in indices:
                out.setdefault((x,y), []).append(case)
    return out

arr = load_data(test_case)
g = indices_graph(arr)

class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.distances = {}

    def add_node(self, node):
        self.nodes.add(node)

    def add_edge(self, fr, to, dist):
        self.edges[fr].append(to)
        self.distances[(fr, to)] = dist


def initialize_graph(g, arr):
    graph = Graph()
    for k in g.keys():
        graph.add_node(k)

    for k, v in g.items():
        for vv in v:
            weight = arr[vv]
            graph.add_edge(k, vv, weight)
    return graph

def dijkstra(graph, initial):
    visited = {initial : 0}
    path = defaultdict(list)

    nodes = set(graph.nodes)

    while nodes:
        minNode = None
        for node in nodes:
            if node in visited:
                if minNode is None:
                    minNode = node
                elif visited[node] < visited[minNode]:
                    minNode = node
        if minNode is None:
            break

        nodes.remove(minNode)
        currentWeight = visited[minNode]

        for edge in graph.edges[minNode]:
            weight = currentWeight + graph.distances[(minNode, edge)]
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                path[edge].append(minNode)

    return visited, path

def run(inp):
    arr = load_data(inp)
    g = indices_graph(arr)
    dj =  (dijkstra(initialize_graph(g, arr), (0,0)))
    score = dj[0]
    print(score[max(list(g.keys()))])

#run(real_deal)
def load_data_super(inp):
    arr = load_data(inp)
    target_arr = np.zeros((arr.shape[0] * 5, arr.shape[1]*5))
    for i in range(5):
        for j in range(5):
            for ii in range(arr.shape[0]):
                for jj in range(arr.shape[1]):
                    xpos = ii
                    ypos = jj
                    x_plus = arr.shape[0] * i
                    y_plus = arr.shape[1] * j
                    xpos += x_plus
                    ypos += y_plus
                    val = arr[ii, jj]
                    val += i+j
                    val = val % 9
                    if val == 0:
                        val = 9
                    target_arr[xpos, ypos] = val
    return target_arr





def run2(inp):
    arr = load_data_super(inp)
    print(arr.shape)
    g = indices_graph(arr)
    dj =  (dijkstra(initialize_graph(g, arr), (0,0)))
    score = dj[0]
    print(score[max(list(g.keys()))])

run2(real_deal)

