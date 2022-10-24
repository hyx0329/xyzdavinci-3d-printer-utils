# -*- encoding: utf-8 -*-

# All commands should be prefixed using the prefix.
# They are separated by ":"
# e.g. "XYZ_@3D:0"
# note only useful or tested commands are kept
COMMAND_PREFIX = "XYZ_@3D"
COMMANDS = (
    ( "0", "Connect to the device, get basic info" ),
    ( "1", "Initiate online printing" ),
    ( "2", "Test print or inject manual commands, end on M84" ),
    ( "3", "Upload firmware binary" ),
    ( "4", "Initiate offline job transfering(G-Code). Receive 'OFFLINE_OK' to proceed" ),
    ( "5", "Get MCHLIFE and MCHEXDUR_LIFE" ),
    ( "6", "Get EE1(Filament info)" ),
    ( "7", "Get EE2(Filament info)" ),
    ( "8", "Get WORK_PARSENT, WORK_TIME, EST_TIME, ET0, BT, MCH_STATE" ),
    ( "9", "? Send build sample" ),
)

# prefix, explaination, type, unit
CODES = (
    ( "MDU", "Model number", "string", "" ),
    ( "FW_V", "Firmware version", "string", "" ),
    ( "MCH_ID", "Machine serial number", "string", "" ),
    ( "EE1", "Filament 1 info, see v2-protocol-notes", "csv", "" ),
    ( "EE2", "Filament 2 info, see v2-protocol-notes", "csv", "" ),
    ( "MCHLIFE", "Machine total work time", "integer", "" ),
    ( "MCHEXDUR_LIFE", "Extruder total work time", "integer", "" ),
    ( "WORK_PARSENT", "Perhaps misspelled `work percent'", "integer", "" ),
    ( "WORK_TIME", "Time spent on current job", "integer", "" ),
    ( "EST_TIME", "Estimated total time for current job", "integer", "" ),
    ( "ET0", "Unknown", "", "" ),
    ( "BT", "Unknown", "", "" ),
    ( "MCH_STATE", "Machine state", "", "" ),
)

# named constants
GCODE_TRUNK_SIZE = 10236  # the checksum takes 4 bytes, total 10240 bytes
SERIAL_BAUDRATE = 115200
MODEL_NUMBER = "daVinciF10"

# Formated text
GCODE_TRANSFER_HEAD = "M1:MyTest,{length},{h}.{m}.{s},EE1_OK,EE2_OK"
# header for one extruder model
GCODE_HEADER = """; filename = Task.3w
; print_time = {print_time}
; machine = {model_number}
; total_layers = {layer_count}
; version = 15062609
; total_filament = {filament_length:.2f}
; nozzle_diameter = {nozzle_diameter:.2f}
; layer_height = {layer_height:.2f}
; support_material = 0
; support_material_extruder = 1
; extruder_filament = {filament_length:.2f}:0.00
; extruder = 1
; filamentid = 41,41,
; materialid = 0,
; fill_density = 0.10
; raft_layers = 0
; support_density = 0.20
; shells = 2
; speed = 45
; brim_width = 0
; dimension = 10.00:10.00:9.95
"""


