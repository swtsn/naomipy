"""Triforce Tools for Naomi, Chihiro, and Triforce systems.

The contents of this file are from the commonly distributed Triforce Netfirm
Toolbox (`triforcetools.py`). I have done some minor refactoring as well as
touched up the comments and style, but the majority of the logic is as it was.
"""
import os
import socket
import struct
import sys
import zlib

from Crypto.Cipher import DES

import utils


IP_ADDRESSES = ["192.168.88.90", "192.168.88.91"]
PORT = 10703


def _display_failure(lcd, msg):
    lcd.set_color(1.0, 0.0, 0.0)
    lcd.clear()
    lcd.message("Failure! \x02\n{}".format(msg))
    time.sleep(2)
    lcd.clear()
    lcd.message("Failure! \x02\nSelect a DIMM")

    # Wait until user presses SELECT
    while True:
        if lcd.is_pressed(LCD.SELECT):
            return


class TriforceUploader:
    class __TriforceUploader:
        def __init__(self, ip_address, display):
            self.ip = ip_address
            self.display = display
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        def __str__(self):
            return repr(self) + self.ip

    instance = None

    def __init__(self, ip_address, display):
        # Ping DIMM
        ping_test = os.system("ping -c 1 -w1 {} > /dev/null 2>&1".format(ip_address))

        if ping_test != 0:
            current_bg = utils.get_bg_colors(display)
            _display_failure(display, "Can't ping IP")

        if not TriforceUploader.instance:
            if not ip_address:
                ip_address = IP_ADDRESSES[0]

            TriforceUploader.instance = TriforceUploader.__TriforceUploader(ip_address, display)

        else:
            TriforceUploader.instance.ip_address = ip_address
            TriforceUploader.instance.display = display

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def upload_game(self, filepath):
        """Manages upload of the game to the target device."""
        try:
            # Note that this port is only open on:
            # - All Type-3 triforces
            # - Pre-type3 triforces jumpered to satellite mode
            # - Naomi
            # - It *should* work on chihiro, but due to lack of hardware, I didn't try
            self.sock = socket.create_connection((self.ip, PORT))
        except Exception as e:
            # log.error("Failed to connect to socket: %s", str(e))
            print("Failed to connect to socket: {}".format(str(e)))
            raise e
    
        self._set_host_mode(0, 1)
        self._set_security_keycode()

        self._upload_file_to_DIMM(filepath)
        
        # Restart host, this will boot into game
        self._restart_host()
        # set time limit to 10h. According to some reports, this does not work.
        # TIME_SetLimit(10*60*1000)

        self.sock.close()

    def _set_host_mode(self, v_and, v_or):
        """Puts device into receive mode"""
        self.sock.send(struct.pack("<II", 0x07000004, (v_and << 8) | v_or))
        # return readsocket(0x8)

    def _set_security_keycode(self):
        """Sets the security keycode on the target device to the zero-key"""
        self.sock.send(struct.pack("<I", 0x7F000008) + b"\x00\x00\x00\x00\x00\x00\x00\x00")

    def _upload_file_to_DIMM(self, filepath):
        """Upload a file into DIMM memory."""
        crc = 0
        addr = 0
    
        game_bin = open(filepath, "rb")
    
        while True:
            sys.stderr.write("%08x\r" % addr)
            data = game_bin.read(0x8000)
    
            if not len(data):
                break
    
            self._upload_data(addr, data, 0)
            crc = zlib.crc32(data, crc)
            addr += len(data)
    
        crc = ~crc
        self._upload_data(addr, b"12345678", 1)
        self._set_DIMM_information(crc, addr)

    def _upload_data(self, addr, data, mark):
        self.sock.send(struct.pack("<IIIH", 0x04800000 | (len(data) + 0xA) | (mark << 16), 0, addr, 0) + data)

    def _set_DIMM_information(self, crc, length):
        self.sock.send(struct.pack("<IIII", 0x1900000C, crc & 0xFFFFFFFF, length, 0))

    def _restart_host(self):
        self.sock.send(struct.pack("<I", 0x0A000000))
