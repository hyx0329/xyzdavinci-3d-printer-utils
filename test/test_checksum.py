# -*- encoding: utf-8 -*-

def test_checksum():
    with open('test/minimal.gcode', 'r') as f:
        data = f.read().replace('\n', '\r\n')
    from davinci_printer_utils.gcode_utils import gen_checksum
    assert 0x0000b92e == gen_checksum(bytes(data, 'utf-8'))

def test_bytes():
    with open('test/minimal.gcode', 'r') as f:
        data = f.read().replace('\n', '\r\n')
    from davinci_printer_utils.gcode_utils import gen_checksum_bytes
    assert b'\x00\x00\xb9\x2e' == gen_checksum_bytes(bytes(data, 'utf-8'))

