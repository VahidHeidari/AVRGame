#******************************************************************************
#*                                                                            *
#*                      AVR Game Demo                                         *
#*                                                                            *
#* This is AVRGame project. AVRGame is a small, low cost, and open source     *
#* hand held console based on AVR microcontroller.                            *
#******************************************************************************

import os
import sys

import ATmega8
import Intel_hex



def PrintLicense():
    print('******************************************************************************')
    print('*                                                                            *')
    print('*                      AVR Game Demo                                         *')
    print('*                                                                            *')
    print('* This is AVRGame project. AVRGame is a small, low cost, and open source     *')
    print('* hand held console based on AVR microcontroller.                            *')
    print('******************************************************************************')
    print('')



def DoMain():
    PrintLicense()

    # Check number of command line arguments.
    if len(sys.argv) < 2:
        print('Usage: %s HEX_FILE' % os.path.basename(sys.argv[0]))
        exit(1)

    # Get hex file path.
    hex_path = sys.argv[1]
    print('Emulating `%s\' file . . .' % hex_path)
    if not os.path.isfile(hex_path):
        print('Emulation failed, because hex file does not exist!')
        exit(2)

    # Read hex file.
    hex_fmt = Intel_hex.IntelHexReader()
    if not hex_fmt.ReadFromFile(hex_path):
        print('Some error occured in reading Hex file!')
        print(hex_fmt.GetErrorMessage())
        exit(3)

    mega8 = ATmega8.ATmega8()
    mega8.DecodeFlash(hex_fmt)
    CYCLES = 20200100
    while mega8.cpu.cycles < CYCLES:
        if (mega8.cpu.cycles % 10) == 0:
            percent = float(mega8.cpu.cycles) / float(CYCLES) * 100.0
            print('%d of %d (%0.1f%%)         \r' % (mega8.cpu.cycles, CYCLES, percent)),
        mega8.cpu.Exec()
    print('')
    #print(mega8.Print())


if __name__ == '__main__':
    DoMain()

