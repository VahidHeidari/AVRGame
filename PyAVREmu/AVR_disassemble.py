#******************************************************************************
#*                                                                            *
#*                      AVR Game Demo                                         *
#*                                                                            *
#* This is AVRGame project. AVRGame is a small, low cost, and open source     *
#* hand held console based on AVR microcontroller.                            *
#******************************************************************************

import os
import sys

import AVR_CPU
import AVR_emu
import Intel_hex



def Disassemble(hex_fmt, PC):
    instr_rec, word = AVR_CPU.FindInstructionRecord(hex_fmt, PC)
    if instr_rec == None:
        return 1, '.dw 0x{:04x}'.format(word)       # Unknown instruction.

    # Disassemble word(s).
    disasm = AVR_CPU.Disassemble(instr_rec, word)
    num_words = len(instr_rec[1].replace(' ', '')) // 16

    # Replace more readable menemonics.
    if disasm.startswith('LDI'):
        opc_str = instr_rec[1].replace(' ', '')
        k, num_bits = AVR_CPU.MkAbsoluteOperand('K', opc_str, word)
        if k == 0xff and num_bits == 8:
            h, num_bits = AVR_CPU.MkAbsoluteOperand('h', opc_str, word)
            disasm = 'SER\tR{}'.format(h + 16)
    elif disasm.startswith('BCLR'):
        s, num_bits = AVR_CPU.MkAbsoluteOperand('s', instr_rec[1].replace(' ', ''), word)
        disasm = 'CL' + 'CZNVSHTI'[s]
    elif disasm.startswith('BSET'):
        s, num_bits = AVR_CPU.MkAbsoluteOperand('s', instr_rec[1].replace(' ', ''), word)
        disasm = 'SE' + 'CZNVSHTI'[s]
    elif disasm.startswith('BRBC'):
        opc_str = instr_rec[1].replace(' ', '')
        s, num_bits = AVR_CPU.MkAbsoluteOperand('s', opc_str, word)
        k, num_bits = AVR_CPU.MkAbsoluteOperand('k', opc_str, word)
        rel_k = AVR_CPU.GetRelative7bit(k) if num_bits == 7 else AVR_CPU.GetRelative12bit(k)
        menem = ['BRCC', 'BRNE', 'BRPL', 'BRVC', 'BRGE', 'BRHC', 'BRTC', 'BRID'][s]
        disasm = '{}\t.{:+}'.format(menem, rel_k * 2)
    elif disasm.startswith('BRBS'):
        opc_str = instr_rec[1].replace(' ', '')
        s, num_bits = AVR_CPU.MkAbsoluteOperand('s', opc_str, word)
        k, num_bits = AVR_CPU.MkAbsoluteOperand('k', opc_str, word)
        rel_k = AVR_CPU.GetRelative7bit(k) if num_bits == 7 else AVR_CPU.GetRelative12bit(k)
        menem = ['BRCS', 'BREQ', 'BRMI', 'BRVS', 'BRLT', 'BRHS', 'BRTS', 'BRIE'][s]
        disasm = '{}\t.{:+}'.format(menem, rel_k * 2)
    elif disasm.startswith('STD\tZ+0'):
        r, num_bits = AVR_CPU.MkAbsoluteOperand('r', instr_rec[1].replace(' ', ''), word)
        disasm = 'ST\tZ, R{}'.format(r)
    elif disasm.startswith('STD\tY+0'):
        r, num_bits = AVR_CPU.MkAbsoluteOperand('r', instr_rec[1].replace(' ', ''), word)
        disasm = 'ST\tY, R{}'.format(r)
    elif disasm.startswith('LDD') and disasm.endswith('Z+0'):
        r, num_bits = AVR_CPU.MkAbsoluteOperand('d', instr_rec[1].replace(' ', ''), word)
        disasm = 'LD\tR{}, Z'.format(r)
    elif disasm.startswith('LDD') and disasm.endswith('Y+0'):
        r, num_bits = AVR_CPU.MkAbsoluteOperand('d', instr_rec[1].replace(' ', ''), word)
        disasm = 'LD\tR{}, Y'.format(r)

    # Add comments.
    if 'k' in instr_rec[3]:
        k, num_bits = AVR_CPU.MkAbsoluteOperand('k', instr_rec[1].replace(' ', ''), word)
        rel_k = AVR_CPU.GetRelative7bit(k) if num_bits == 7 else AVR_CPU.GetRelative12bit(k)
        disasm += '\t; 0x{:x}'.format((PC + 2 + rel_k * 2) & 0xffffffff)
    return num_words, disasm



def DoMain():
    # Check number of command line arguments.
    if len(sys.argv) < 2:
        AVR_emu.PrintLicense()
        print('Usage: %s HEX_FILE' % sys.argv[0])
        exit(1)

    # Get hex file path.
    hex_path = sys.argv[1]
    if not os.path.isfile(hex_path):
        print('Emulation failed, because hex file does not exist!')
        exit(2)

    # Read hex file.
    hex_fmt = Intel_hex.IntelHexReader()
    if not hex_fmt.ReadFromFile(hex_path):
        print('Some error occured in reading Hex file!')
        print(hex_fmt.GetErrorMessage())
        exit(3)

    PC = 0
    hex_num_bytes = hex_fmt.GetNumBytes()
    while PC < hex_num_bytes:
        num_words, menem = Disassemble(hex_fmt, PC)
        hex_mem = ''
        for i in range(2 * num_words):
            b = hex_fmt.GetMemoryBytes()[PC + 2 * num_words - i - 1]
            hex_mem += '{}{:02x}'.format(' ' if hex_mem else '', b)
        print('{:>4x}:\t{:<9s}\t{}'.format(PC, hex_mem, menem))
        PC += num_words * 2


if __name__ == '__main__':
    DoMain()

