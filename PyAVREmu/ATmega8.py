#******************************************************************************
#*                                                                            *
#*                      AVR Game Demo                                         *
#*                                                                            *
#* This is AVRGame project. AVRGame is a small, low cost, and open source     *
#* hand held console based on AVR microcontroller.                            *
#******************************************************************************

import AVR_CPU



class ATmega8:
    def __init__(self):
        self.cpu = AVR_CPU.AVR8BitCPU(1024)


    def DecodeFlash(self, hex_fmt):
        self.cpu.DecodeFlash(hex_fmt)


    def Exec(self):
        self.cpu.Exec()


    def Print(self):
        return self.cpu.Print()

