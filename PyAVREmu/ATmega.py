#******************************************************************************
#*                                                                            *
#*                      AVR Game Demo                                         *
#*                                                                            *
#* This is AVRGame project. AVRGame is a small, low cost, and open source     *
#* hand held console based on AVR microcontroller.                            *
#******************************************************************************

import ATmega8_defs
import ATmega168_defs
import AVR_CPU



class ATmega8:
    def __init__(self):
        self.cpu = AVR_CPU.AVR8BitCPU(1024,         # SRAM size
                8192,                               # Flash size
                0,                                  # Extended IO size
                ATmega8_defs.IO_NAMES,              # IO names
                None)                               # Extended IO names


    def RegisterIOWriteFunc(self, io_write_func):
        self.cpu.io_write_func = io_write_func


    def RegisterIOReadFunc(self, io_read_func):
        self.cpu.io_read_func = io_read_func


    def DecodeFlash(self, hex_fmt):
        self.cpu.DecodeFlash(hex_fmt)


    def Exec(self):
        self.cpu.Exec()


    def Print(self):
        return self.cpu.Print()



class ATmega168:
    def __init__(self):
        self.cpu = AVR_CPU.AVR8BitCPU(1024,         # SRAM size
                16384,                              # Flash size
                160,                                # Extended IO size
                ATmega168_defs.IO_NAMES,            # IO names
                ATmega168_defs.EXT_IO_NAMES)        # Extended IO names


    def RegisterIOWriteFunc(self, io_write_func):
        self.cpu.io_write_func = io_write_func


    def RegisterIOReadFunc(self, io_read_func):
        self.cpu.io_read_func = io_read_func


    def DecodeFlash(self, hex_fmt):
        self.cpu.DecodeFlash(hex_fmt)


    def Exec(self):
        self.cpu.Exec()


    def Print(self):
        return self.cpu.Print()

