from rich import print
from collections import deque
from functools import partial
class Packet(object):
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

    def __init__(self, message: str, from_bits = False):
        self.bits = self.decode(message) if not from_bits else message
        print(self.bits)
        self.version = self.bin2int(self.bits[:3])
        self.type_id = self.bin2int(self.bits[3:6])
        info = self.bits[6:]
        if self.type_id == 4:
            self.result = self.parse_literal(info)
        else:
            self.result = self.parse_operator(info)

    def decode(self, s: str) -> str:
        return "".join([self.binmap[x] for x in s])

    def parse_literal(self, info: str, ret: str = '')  -> int:
        print(info[0])
        if info[0] == '0':
            ret += info[:5][1:]
            info = info[5:]
            self.remainder = info
            return self.bin2int(ret)
        else:
            ret += info[:5][1:]
            info = info[5:]
            return self.parse_literal(info, ret)

    def parse_operator(self, info: str):
        self.length_id = info[0]
        info = info[1:]
        if int(self.length_id) == 0:
            self.parse_total_packets(info)

    def parse_total_packets(self, info: str):
        size = self.bin2int(info[:15])
        info = info[15:size]
        xx = Packet(info, True)







if __name__ == "__main__":
    p = Packet("38006F45291200")
    p = Packet("D2FE28")
    print(p.result)
