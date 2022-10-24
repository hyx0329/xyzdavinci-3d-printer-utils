# -*- encoding: utf-8 -*-

from davinci_printer_utils.printer import PrinterProtoV2

printer = PrinterProtoV2(port="/dev/ttyACM0")

with open("../cube/Unnamed-Cube-slicer.gcode", 'r') as f:
    gcode = f.read()

print(printer.serial_open())
print(printer.print_gcode(gcode))

