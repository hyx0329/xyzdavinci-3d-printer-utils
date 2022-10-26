# -*- encoding: utf-8 -*-

def gen_checksum(data: [bytes, bytearray]):
    # faster than sum(), avoid big number
    ans = 0
    for i in data:
        ans = ( ans + i ) & 0xFFFFFFFF
    return ans

def gen_checksum_bytes(data: [bytes, bytearray]):
    value = gen_checksum(data)
    chk = bytes([ (value >> (i * 8)) & 0xFF for i in range(3,-1,-1) ])
    return chk

