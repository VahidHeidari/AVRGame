#******************************************************************************
#*                                                                            *
#*                      AVR Game Demo                                         *
#*                                                                            *
#* This is AVRGame project. AVRGame is a small, low cost, and open source     *
#* hand held console based on AVR microcontroller.                            *
#******************************************************************************

import os



AVR_INSTR_PATH = os.path.join('Docs', 'AVR_instr_set.txt')
TEST_AVR_INSTR_PATH = os.path.join('Datasets', 'AVR_instr_set_ADC_ANDI.txt')



#
# Returns a data structur in below format:
#
#   [ (menemonic, opcode_str), ... ]
#
def ReadInstructionFile(file_path):
    # Read all lines from instruction file.
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Read prefix strings.
    prefixes = []
    for l in lines:
        l = l.strip()
        menemonic = l[0:10].strip()
        opcode_str = l[10:].replace(' ', '')[0:16]
        if opcode_str.startswith('['):
            continue
        prefixes.append((menemonic, opcode_str))
    return prefixes


#
# Returns a data structure in below format:
#
#    [ (opc, opc_mask, oprd_mask), ... ]
#
def MakeMasks(prefixes):
    num_prefixes = len(prefixes)
    masks = []
    for i in range(num_prefixes):
        rec = prefixes[i]
        opc_str = ''.join([ '1' if c == '1' else '0' for c in rec[1] ])
        opc = int(opc_str, 2)

        opc_mask_str = ''.join([ '1' if c in [ '0', '1' ] else '0' for c in rec[1] ])
        opc_mask = int(opc_mask_str, 2)

        oprd_mask_str = ''.join([ '1' if c not in ['0', '1'] else '0' for c in rec[1] ])
        oprd_mask = int(oprd_mask_str, 2)

        masks.append((opc, opc_mask, oprd_mask))
    return masks


def PrintMenemonicsAndMasks(prefixes, masks):
    num_prefixes = len(prefixes)
    print('Num Prefixes: %d' % num_prefixes)

    mx_menem = max([ len(rec[0]) for rec in prefixes ])
    for i in range(len(masks)):
        pref_rec = prefixes[i]
        menem = pref_rec[0].ljust(mx_menem + 1)

        mask_rec = masks[i]
        opc = mask_rec[0]
        opc_mask = mask_rec[1]
        oprd_mask = mask_rec[2]
        if oprd_mask == 0:
            print('%s 0x%04x    0x%04x' % (menem, opc, opc_mask))
        else:
            print('%s 0x%04x    0x%04x    0x%04x' % (menem, opc, opc_mask, oprd_mask))


def IsEqualOpcode(mask_rec_1, mask_rec_2):
    opc_1 = mask_rec_1[0]
    opc_2 = mask_rec_2[0]
    return opc_1 == opc_2


def IsEqualMaskedOpcode(mask_rec_1, mask_rec_2):
    opc_2 = mask_rec_2[0]
    oprd_mask_2 = mask_rec_2[2]
    opc_oprd_2_bits = opc_2 | oprd_mask_2

    opc_1 = mask_rec_1[0]
    opc_1_mask = mask_rec_1[1]
    return (opc_1_mask & opc_oprd_2_bits) == opc_1


def RunSearch(prefixes, masks, eq_func, msg, is_check_beg=False):
    print(msg)
    num_prefixes = len(prefixes)
    for i in range(num_prefixes - 1):
        opc_i = masks[i]
        eq_str = ''
        chk_range = range(num_prefixes) if is_check_beg else range(i + 1, num_prefixes)
        for j in chk_range:
            if j == i:
                continue
            opc_j = masks[j]
            if eq_func(opc_i, opc_j):
                if not eq_str:
                    eq_str = '  ' + prefixes[i][0]
                eq_str += ',  ' + prefixes[j][0]
        if eq_str:
            print(eq_str)


def PrintEqualOpcodes(prefixes, masks):
    RunSearch(prefixes, masks, IsEqualOpcode, '\nEqual Opcodes:')


def PrintEqualMaskedOpcodes(prefixes, masks):
    RunSearch(prefixes, masks, IsEqualMaskedOpcode, '\nEqual Masked Opcodes:', True)


def ProcessInstructions(avr_instruction_path):
    prefixes = ReadInstructionFile(avr_instruction_path)
    masks = MakeMasks(prefixes)

    PrintMenemonicsAndMasks(prefixes, masks)
    PrintEqualOpcodes(prefixes, masks)
    PrintEqualMaskedOpcodes(prefixes, masks)



def DoMain():
    print('----------')
    print(' Test Instructions')
    ProcessInstructions(TEST_AVR_INSTR_PATH)

    print('\n\n----------')
    print(' All Instructions')
    ProcessInstructions(AVR_INSTR_PATH)


if __name__ == '__main__':
    DoMain()

