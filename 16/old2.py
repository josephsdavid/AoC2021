from rich import print
from collections import deque
from functools import partial
import itertools as it


binmap = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111"
}

bin2int = partial(int, base = 2)

def hex2bin(s):
    return "".join([binmap[x] for x in s])

class Packet(object):
    def __init__(self, bits: str):
        self.version = bin2int(bits[:3])
        self.type_id = bin2int(bits[3:6])
        self.bits = bits[6:]

def make_packet(inp: str):
    return Packet(hex2bin(inp))

def initialize(inp: str):
    return deque([make_packet(inp)])

def parse_literal(p: Packet):
    bits = p.bits
    q = deque(list(bits[idx: idx+5]) for idx in range(0,len(bits), 5))
    ret = ""
    remainder = ""
    while (len(q[0]) == 5):
        val = q.popleft()
        ret += "".join(val[1:])
        if val[0] == '0':
            break
    remainder = "".join(it.chain(*[x for x in q]))
    return bin2int(ret), remainder

# ???
# we need to grow the list
def parse(q):
    p = q.pop()
    if p.type_id == 4:
        value, bits = parse_literal(p)
        q.append((p, value))
        return q, bits
    else:
        bits = p.bits
        length_id = bits[0]
        bits = bits[1:]
        if length_id == '0':
            size = bin2int(bits[:15])
            bits = bits[15:15+size]
            print(bits)
            while len(bits) > 11:
                nextp = Packet(bits)
                q.append(p)
                q.append(nextp)
                q, bits = parse(q)
        else:
            n_packets = bin2int(bits[:11])
            bits = bits[11:]
            plist = []
            while len(plist) < n_packets:
                nextp = Packet(bits)
                plist.append(nextp)
                q.append(p)
                q.append(nextp)
                q, bits = parse(q)

    return q, bits


def sum_version_numbers(inp: str):
    init = initialize(inp)
    q, _ = parse(init)
    print(q)
    print(_)
    out = set()
    while q:
        x = q.pop()
        if isinstance(x, tuple):
            out.add(x[0])
        else:
            out.add(x)
    print([x.version for x in out])
    return sum(x.version for x in out)




print(sum_version_numbers("C0015000016115A2E0802F182340"))
# contains operator -> op -> op -> lit



