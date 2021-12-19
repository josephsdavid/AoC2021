from rich import print
from collections import deque
from functools import partial
import itertools as it
import json


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
        self.value = None

    def __repr__(self):
        return json.dumps(self.__dict__, indent=2)


def make_packet(inp: str):
    return Packet(hex2bin(inp))


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

def parse_packet(p: Packet):
    q = deque()
    q.append(p)
    seen = []
    while q:
        packet = q.popleft()
        if packet.type_id == 4:
            val, remainder = parse_literal(packet)
            if len(remainder) > 11:
                q.append(Packet(remainder))
            packet.value = val
            seen.append(packet)
        else:
            bits = packet.bits
            length_id = bits[0]
            bits = bits[1:]
            if length_id == '0':
                size = bin2int(bits[:15])
                bits = bits[15:15+size]
                if len(bits) > 11:
                    nextp = Packet(bits)
                    seen.append(packet)
                    q.append(nextp)
            elif length_id == "1":
                n_packets = bin2int(bits[:11])
                bits = bits[11:]
                plist = []
                while len(plist) < n_packets:
                    nextp = Packet(bits)
                    plist.append(nextp)
                    q.append(nextp)
                seen.append(packet)
            else:
                pass
        print(len(seen))
    return seen

def run(inp: str):
    return parse_packet(make_packet(inp))


#print(run("38006F45291200"))
(run("EE00D40C823060"))
