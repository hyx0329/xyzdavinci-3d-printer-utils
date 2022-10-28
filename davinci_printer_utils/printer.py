# -*- encoding: utf-8 -*-
__doc__ = '''
Printer interface and print protocol implementation.
'''

from typing import Union
from enum import Enum
from .constants import MODEL_NUMBER, GCODE_HEADER, \
        GCODE_TRANSFER_HEAD, GCODE_TRUNK_SIZE, \
        FILAMENT_ID

from .gcode_utils import gen_checksum_bytes
import time
import serial


class Filament:
    def __init__(self, text=None):
        self.text = None
        self.xyz_code = "5a"    # useless
        self.material = "ABS"
        self.color = (0,0,0)    # RGB
        self.manufacture_date = ""
        self.capacity = 0       # mm
        self.remaining = 0      # mm
        self.temperature_head = 210  # celsius
        self.temperature_bed = 90    # celsius
        self.mloc = ""
        self.dloc = ""
        self.serial_number = ""
        self.security_code = ""
        self.not_official = False

        if text is not None:
            self.parse(text)

    def parse(self, text: str):
        self.text = text
        raise NotImplementedError()


class Printer:
    def print_gcode(self, gcode: str):
        raise NotImplementedError()
    
    def print_gcode_file(self, path: str):
        raise NotImplementedError()

    def status_snapshot(self):
        raise NotImplementedError()

    def get_firmware_version(self):
        raise NotImplementedError()

    def get_model(self):
        raise NotImplementedError()


# on a XYZprinting da vinci 1.0, fw v1.2.3, supports partial V3 protocol
# so it's partial implemented
class PrinterProtoV2(Printer):
    def __init__(self, port=None, serial=None, timeout=5):
        self.port = port
        self.serial = serial
        self.timeout = timeout
        self.model = ""
        self.firmware_version = ""
        self.machine_id = ""
        self.filament = Filament()

    def serial_open(self) -> bool:
        self.serial_close()
        if self.port is None:
            return False
        self.serial = serial.Serial(
            port = self.port,
            baudrate = 115200,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            bytesize = serial.EIGHTBITS,
            timeout = self.timeout
        )
        return self.serial.is_open

    def serial_close(self):
        if isinstance(self.serial, serial.Serial):
            self.serial.close()
            self.serial = None

    def serial_write(self, data: [bytes, bytearray]):
        self.serial.write(data)

    def serial_wait_rx(self, timeout=5):
        if isinstance(self.serial, serial.Serial):
            while timeout > 0 and self.serial.inWaiting() == 0:
                timeout -= 1
                time.sleep(0.5)

    def serial_read(self, count=0) -> bytes:
        raise NotImplementedError("Not useful")

    def serial_readline(self) -> bytes:
        # has timeout itself
        return self.serial.readline()

    def serial_readlines(self) -> bytes:
        return self.serial.readlines()

    def serial_wait_for(self, *args) -> bool:
        res = self.serial_readline()
        for substring in args:
            if res.find(substring) > -1:
                # found
                return True
        # no, not found
        return False

    def status_snapshot(self) -> dict:
        # actually can be a serialization process
        return {}

    def update_all_info(self):
        self.serial_send(b"XYZ_@3D:0\r\n")
        self.serial_wait_rx(1)
        data = self.serial_readlines()

    def update_basic_info(self):
        pass

    def start_online_printing(self, *args, **kwargs):
        raise NotImplementedError("Not going to implement this")

    def inject_command(self, gcode: str):
        raise NotImplementedError("Not implemented yet")

    def update_lifetime_info(self):
        pass

    def send_offline_gcode(self):
        pass

    def update_all_info_v3(self):
        pass

    def parse_single_line(self, line: bytes):
        line = line.decode('utf-8').strip()
        if line.startswith("MDU"):
            pass
        elif line.startwith("FW_V"):
            pass
        elif line.startwith("MCH_ID"):
            pass
        elif line.startwith("EE1"):
            pass
        elif line.startwith("MCHLIFE"):
            pass
        elif line.startwith("MCHEXDUR"):
            pass
        elif line.startwith("WORK_PARSENT"):
            pass
        elif line.startwith("WORK_TIME"):
            pass
        elif line.startwith("EST_TIME"):
            pass
        elif line.startwith("FW_V"):
            pass
        else:
            pass

    def print_gcode(self, gcode: str, retry_count=5) -> bool:
        # anyway the code below will be a legacy implementation
        # send the gcode to the printer

        # some gcode meta data 
        print_time = [0,0,0]  # h,m,s, use when preparing the gcode metadata
        model_number = MODEL_NUMBER  # for the moment, hardcode it
        filament_length = 0
        filament_name = "abs"
        filament_id = FILAMENT_ID.get("ABS", 41)
        nozzle_diameter = 0.4
        layer_height = 0.3
        layer_count = 0

        # parse the data generated by slic3r/PrusaSlicer
        # they contains useful metadata
        # BTW XYZWare uses Slic3r's code but not open-sourced
        trunks = gcode.split('\n')
        for line in trunks:
            if line.startswith('G'):
                # maybe, speed up the process
                # as the most of lines are g-code start with 'G'
                continue
            elif line.startswith('; filament used [mm]'):
                # parse cost
                filament_length = float(line.split('=')[1].strip())
            elif line.startswith('; estimated printing time'):
                # parse time
                stats = line.split('=')[1].strip().split(' ')
                for i in stats:
                    if i.endswith('h'):
                        print_time[0] = int(i[:-1])
                    elif i.endswith('m'):
                        print_time[1] = int(i[:-1])
                    elif i.endswith('s'):
                        print_time[2] = int(i[:-1])
            elif line.startswith('; layer_height'):
                # layer height
                layer_height = float(line.split('=')[1].strip())
            elif line.startswith('; nozzle_diameter'):
                # nozzle diameter
                nozzle_diameter = float(line.split('=')[1].strip())
            elif line.startswith(';LAYER_CHANGE'):
                # count layer
                layer_count += 1
            elif line.startswith('; filament_type'):
                filament_name = line.split('=')[1].strip().lower()
                filament_id = FILAMENT_ID.get(filament_name.upper(), 41)
            else:
                pass
        
        # add a header
        print_time_in_sec = print_time[0] * 3600 + print_time[1] * 60 + print_time[2]
        gcode_with_header = GCODE_HEADER.format(
            print_time = print_time_in_sec, model_number = model_number,
            layer_count = layer_count, filament_length = filament_length,
            nozzle_diameter = nozzle_diameter, layer_height = layer_height,
            filament_name = filament_name, filament_id = filament_id
        ) + gcode

        gcode_with_header_bytes = gcode_with_header.replace('\n', '\r\n').encode('utf-8')

        # fill in the transfer head
        gcode_length = len(gcode_with_header_bytes)
        transfer_head_bytes = GCODE_TRANSFER_HEAD.format(
            length=gcode_length,
            h=print_time[0],
            m=print_time[1],
            s=print_time[2]
        ).encode('utf-8')

        # now have almost all data, to start printing:
        # send command to initiate the transfer and wait response
        # send some meta data and wait response
        # send gcode trunks
        #   - gcode(<= 10236 bytes) + checksum(4 bytes)
        #   - wait response each time, if error, resend
        # printing will start automatically after finishing the tranfer

        # issue tranfer command
        self.serial_write(b'XYZ_@3D:4\r\n')
        if not self.serial_wait_for(b'OFFLINE_OK', b'M1_OK'):
            return False

        # send transfer head
        self.serial_write(transfer_head_bytes)
        if not self.serial_wait_for(b'OFFLINE_OK', b'M1_OK'):
            return False

        # send gcode data
        cursor = 0
        while cursor < gcode_length:
            end_cursor = cursor + GCODE_TRUNK_SIZE
            if end_cursor > gcode_length:
                end_cursor = gcode_length
            piece = gcode_with_header_bytes[cursor:end_cursor]
            piece += gen_checksum_bytes(piece)
            while retry_count >= 0:
                self.serial_write(piece)
                if self.serial_wait_for(b'CheckSumOK', b'M2_OK'):
                    break
                else:
                    retry_count -= 1
            if retry_count < 0:
                return False

            cursor = end_cursor

        # all done, printing should start
        return True

