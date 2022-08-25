#******************************************************************************
#*                                                                            *
#*                      AVR Game Demo                                         *
#*                                                                            *
#* This is AVRGame project. AVRGame is a small, low cost, and open source     *
#* hand held console based on AVR microcontroller.                            *
#******************************************************************************

import os
import sys

import ATmega
import Intel_hex
import draw_util



#MAX_CYCLES = 26200100
#MAX_CYCLES = 20200100
#MAX_CYCLES = 18200100
#MAX_CYCLES = 10200100
#MAX_CYCLES = 2200100
MAX_CYCLES = 1200100
#MAX_CYCLES = 800100
#MAX_CYCLES = 50100

IS_DRAW_ALL_FRAMES = False

# Frame data
frame_num     = 0
PortD_Data    = []
OldPortD_Data = []

# Input stream
input_idx    = 0
input_stream = []
in_data      = '-----'
inv_in_data  = 'XXXXX'



def PrintLicense():
    print('******************************************************************************')
    print('*                                                                            *')
    print('*                      AVR Game Demo                                         *')
    print('*                                                                            *')
    print('* This is AVRGame project. AVRGame is a small, low cost, and open source     *')
    print('* hand held console based on AVR microcontroller.                            *')
    print('******************************************************************************')
    print('')


def PrintHelp():
    print('  Usage: %s CPU HEX_FILE [INPUT_STREAM]' % os.path.basename(sys.argv[0]))
    print('')
    print('    CPU          : CPU type is `ATmega8\' or `ATmega168\'')
    print('    HEX_FILE     : Input hex file')
    print('    INPUT_STREAM : Joystick input stream file')
    print('')


def IOWriteFunc(cpu, IO_name, addr, val):
    global frame_num, PortD_Data, OldPortD_Data
    global input_idx, input_stream, in_data, inv_in_data

    #if IO_name == 'PORTB':
    #    print('PORTB |' + ''.join([' ' if val & (0x80 >> i) else '*' for i in range(8)]) + '|')
    #if IO_name == 'PORTD':
    #    print('PORTD |' + ''.join(['*' if val & (0x80 >> i) else ' ' for i in range(8)]) + '|')
    #    if val == 0x80:
    #        print('')
    # Save screen data.
    if IO_name == 'PORTD':
        data_str = ''.join(['*' if (val & (0x80 >> i)) else ' ' for i in range(8)])
        PortD_Data.append(data_str)
        return

    # Check line data.
    if IO_name == 'PORTB':
        is_input_changed = False
        prev_val = cpu.IO[addr]
        if (prev_val == 0x7f) and (val == 0xff):
            # Increment frame number.
            frame_num += 1

            # Get input data put to appropriate port.
            while input_idx < len(input_stream):
                frm = input_stream[input_idx][0]
                if frame_num < frm:
                    break

                # Check current frame.
                if frm == frame_num:
                    in_data = ''.join(reversed(input_stream[input_idx][1]))
                    inv_in_data = ''.join(['-' if c == 'X' else 'X' for c in in_data])
                    in_byte = ''.join(['1' if c == 'X' else '0' for c in reversed(in_data)])
                    cpu.IO[cpu.IO_names.index('PINC')] = int(in_byte, 2) & 0xff
                    is_input_changed = True
                    print('Input changed', frame_num, in_data, inv_in_data, in_byte)
                    break

                input_idx += 1

            # Check whether screen has changed or not.
            frame_data = PortD_Data[-8:]
            if IS_DRAW_ALL_FRAMES or is_input_changed or OldPortD_Data != frame_data:
                if not os.path.isdir('Frames'):
                    os.makedirs('Frames')
                out_path = os.path.join('Frames', 'device-%07d.jpg' % frame_num)
                draw_util.DrawDevice(frame_data, inv_in_data, out_path)
                PortD_Data = []
                OldPortD_Data = frame_data



def DoMain():
    PrintLicense()

    # Check number of command line arguments.
    if len(sys.argv) < 3:
        PrintHelp()
        exit(1)

    # Get CPU type.
    cpu_type = sys.argv[1]
    if not cpu_type in [ 'ATmega8', 'ATmega168' ]:
        print('CPU type `%s\' is unknown!' % cpu_type)
        PrintHelp()
        exit(2)

    # Get hex file path.
    hex_path = sys.argv[2]
    print('Reading hex file `%s\' . . .' % hex_path)
    if not os.path.isfile(hex_path):
        print('Emulation failed, because hex file does not exist!')
        exit(3)

    # Read hex file.
    hex_fmt = Intel_hex.IntelHexReader()
    if not hex_fmt.ReadFromFile(hex_path):
        print('Some error occured in reading Hex file!')
        print(hex_fmt.GetErrorMessage())
        exit(4)

    # Try to read input stream file path.
    if len(sys.argv) > 3:
        input_path = sys.argv[3]
        print('Reading input file `%s\' . . .' % input_path)
        if not os.path.isfile(input_path):
            print('Could not find input file! Continue without input stream.')
        else:
            with open(input_path, 'r') as f:
                for l in f:
                    l = l.strip()
                    if not l or l.startswith('#'):
                        continue
                    sp = l.split()
                    frm = int(sp[0])
                    inpt = sp[1]
                    input_stream.append((frm, inpt))

    # Clear previouse frames.
    if os.path.isdir('Frames'):
        for fl in os.listdir('Frames'):
            os.remove(os.path.join('Frames', fl))

    # Start emulation.
    mega = ATmega.ATmega8() if cpu_type == 'ATmega8' else ATmega.ATmega168()
    mega.RegisterIOWriteFunc(IOWriteFunc)
    mega.DecodeFlash(hex_fmt)
    while mega.cpu.cycles < MAX_CYCLES:
        if (mega.cpu.cycles % 10) == 0:
            percent = float(mega.cpu.cycles) / float(MAX_CYCLES) * 100.0
            fmt_tpl = (mega.cpu.cycles, MAX_CYCLES, percent, frame_num)
            #print('%d of %d (%0.1f%%)  frm: %d        \r' % fmt_tpl),
        mega.cpu.Exec()
    print('')
    #print(mega.Print())
    #draw_util.MakeGIFAnimation('Frames', os.path.join('Frames', 'animation.gif'))


if __name__ == '__main__':
    DoMain()

