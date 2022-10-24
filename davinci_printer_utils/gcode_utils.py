# -*- encoding: utf-8 -*-

def gen_checksum(data: [bytes, bytearray]):
    return sum(data) & 0xFFFFFFFF

def gen_checksum_bytes(data: [bytes, bytearray]):
    value = sum(data) & 0xFFFFFFFF
    chk = bytes([ (value >> (i * 8)) & 0xFF for i in range(3,-1,-1) ])
    return chk

