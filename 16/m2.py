from rich import print
from collections import deque
from functools import partial, reduce
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

def get_value(packet):
    value = ""
    while packet[0] == "1":
        value += packet[1:5]
        packet = packet[5:]
    value  += packet[1:5]
    packet = packet[5:]
    return bin2int(value), packet

packet_map = {0: lambda x: sum(x), 1: lambda x: reduce(lambda a,b: a*b, x), 2: lambda x: min(x), 3: lambda y: max(y), 5: lambda x: int(x[0] > x[1]), 6: lambda x: int(x[0] < x[1]), 7: lambda x: int(x[0] == x[1])}

def decode_packet(packet):
    version = bin2int(packet[:3])
    type_id = bin2int(packet[3:6])
    packet = packet[6:]
    value = 0
    if type_id == 4:
        value, packet = get_value(packet)
    else:
        length_id = bin2int(packet[0])
        packet = packet[1:]
        number_packets = []
        if length_id == 0:
            size = bin2int(packet[:15])
            packet = packet[15:]
            nextp = packet[:size]
            packet = packet[size:]
            while nextp:
                nextver, nextval, nextp = decode_packet(nextp)
                version += nextver
                number_packets.append(nextval)
        else:
            n_packets = bin2int(packet[:11])
            packet = packet[11:]
            for _ in range(n_packets):
                nextver, nextval, packet = decode_packet(packet)
                version += nextver
                number_packets.append(nextval)
        value = packet_map[type_id](number_packets)
    return version, value, packet

print(decode_packet(hex2bin("8A004A801A8002F478")))

real_deal = 'E0525D9802FA00B80021B13E2D4260004321DC648D729DD67B2412009966D76C0159ED274F6921402E9FD4AC1B0F652CD339D7B82240083C9A54E819802B369DC0082CF90CF9280081727DAF41E6A5C1B9B8E41A4F31A4EF67E2009834015986F9ABE41E7D6080213931CB004270DE5DD4C010E00D50401B8A708E3F80021F0BE0A43D9E460007E62ACEE7F9FB4491BC2260090A573A876B1BC4D679BA7A642401434937C911CD984910490CCFC27CC7EE686009CFC57EC0149CEFE4D135A0C200C0F401298BCF265377F79C279F540279ACCE5A820CB044B62299291C0198025401AA00021D1822BC5C100763A4698FB350E6184C00A9820200FAF00244998F67D59998F67D5A93ECB0D6E0164D709A47F5AEB6612D1B1AC788846008780252555097F51F263A1CA00C4D0946B92669EE47315060081206C96208B0B2610E7B389737F3E2006D66C1A1D4ABEC3E1003A3B0805D337C2F4FA5CD83CE7DA67A304E9BEEF32DCEF08A400020B1967FC2660084BC77BAC3F847B004E6CA26CA140095003900BAA3002140087003D40080022E8C00870039400E1002D400F10038C00D100218038F400B6100229500226699FEB9F9B098021A00800021507627C321006E24C5784B160C014A0054A64E64BB5459DE821803324093AEB3254600B4BF75C50D0046562F72B1793004667B6E78EFC0139FD534733409232D7742E402850803F1FA3143D00042226C4A8B800084C528FD1527E98D5EB45C6003FE7F7FCBA000A1E600FC5A8311F08010983F0BA0890021F1B61CC4620140EC010100762DC4C8720008641E89F0866259AF460C015D00564F71ED2935993A539C0F9AA6B0786008D80233514594F43CDD31F585005A25C3430047401194EA649E87E0CA801D320D2971C95CAA380393AF131F94F9E0499A775460'

print(decode_packet(hex2bin(real_deal)))

