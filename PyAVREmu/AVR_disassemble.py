#******************************************************************************
#*                                                                            *
#*                      AVR Game Demo                                         *
#*                                                                            *
#* This is AVRGame project. AVRGame is a small, low cost, and open source     *
#* hand held console based on AVR microcontroller.                            *
#******************************************************************************

import os
import sys

import Intel_hex



#DEFAULT_HEX_FILE = os.path.join('Datasets', 'GameDemoSelect(Any_168).hex')
DEFAULT_HEX_FILE = os.path.join('Datasets', 'GameAVR.hex')

ABS_OPRDS = [ 'b', 'q', 's', 'r', 'd' ]

INSTRUCTIONS = [
    ( 'ADC       Rd, Rr',           '0001 11rd dddd rrrr' ),        # 0 <= d <= 31,         0 <= r <= 31
    ( 'ADD       Rd, Rr',           '0000 11rd dddd rrrr' ),        # 0 <= d <= 31,         0 <= r <= 31
    ( 'ADIW      Rp+1:Rp, K',       '1001 0110 KKpp KKKK' ),        # p \in {24,26,28,30},  0 <= K <= 63
    ( 'AND       Rd, Rr',           '0010 00rd dddd rrrr' ),        # 0 <= d <= 31,         0 <= r <= 31
    ( 'ANDI      Rh, K',            '0111 KKKK hhhh KKKK' ),        # 16 <= h <= 31,        0 <= K <= 255
    ( 'ASR       Rd',               '1001 010d dddd 0101' ),        # 0 <= d <= 31
    #( 'BCLR      s',                '1001 0100 1sss 1000' ),        # 0 <= s <= 7
    ( 'BLD       Rd, b',            '1111 100d dddd 0bbb' ),        # 0 <= d <= 31,         0 <= b <= 7
    #( 'BRBC      s, k',             '1111 01kk kkkk ksss' ),        # 0 <= s <= 7,          -64 <= k <= +63
    #( 'BRBS      s, k',             '1111 00kk kkkk ksss' ),        # 0 <= s <= 7,          -64 <= k <= +63
    ( 'BRCC      .k',               '1111 01kk kkkk k000' ),        # -64 <= k <= +63
    ( 'BRCS      .k',               '1111 00kk kkkk k000' ),        # -64 <= k <= +63
    ( 'BREAK',                      '1001 0101 1001 1000' ),
    ( 'BREQ      .k',               '1111 00kk kkkk k001' ),        # -64 <= k <= +63
    ( 'BRGE      .k',               '1111 01kk kkkk k100' ),        # -64 <= k <= +63
    ( 'BRHC      .k',               '1111 01kk kkkk k101' ),        # -64 <= k <= +63
    ( 'BRHS      .k',               '1111 00kk kkkk k101' ),        # -64 <= k <= +63
    ( 'BRID      .k',               '1111 01kk kkkk k111' ),        # -64 <= k <= +63
    ( 'BRIE      .k',               '1111 00kk kkkk k111' ),        # -64 <= k <= +63
    #( 'BRLO      .k',               '1111 00kk kkkk k000' ),        # -64 <= k <= +63
    ( 'BRLT      .k',               '1111 00kk kkkk k100' ),        # -64 <= k <= +63
    ( 'BRMI      .k',               '1111 00kk kkkk k010' ),        # -64 <= k <= +63
    ( 'BRNE      .k',               '1111 01kk kkkk k001' ),        # -64 <= k <= +63
    ( 'BRPL      .k',               '1111 01kk kkkk k010' ),        # -64 <= k <= +63
    #( 'BRSH      .k',               '1111 01kk kkkk k000' ),        # -64 <= k <= +63
    ( 'BRTC      .k',               '1111 01kk kkkk k110' ),        # -64 <= k <= +63
    ( 'BRTS      .k',               '1111 00kk kkkk k110' ),        # -64 <= k <= +63
    ( 'BRVC      .k',               '1111 01kk kkkk k011' ),        # -64 <= k <= +63
    ( 'BRVS      .k',               '1111 00kk kkkk k011' ),        # -64 <= k <= +63
    #( 'BSET      s',                '1001 0100 0sss 1000' ),        # 0 <= s <= 7
    ( 'BST       Rd, b',            '1111 101d dddd 0bbb' ),        # 0 <= d <= 31,         0 <= b <= 7
    ( 'CALL      K',                '1001 010K KKKK 111K KKKK KKKK KKKK KKKK' ),# 0 <= K < 64K, 0 <= K < 4M
    ( 'CBI       A, b',             '1001 1000 AAAA Abbb' ),        # 0 <= A <= 31,         0 <= b <= 7
    #CBR       Rd, K             [AND]                              # 16 <= d <= 31,        0 <= K <= 255
    ( 'CLC',                        '1001 0100 1000 1000' ),
    ( 'CLH',                        '1001 0100 1101 1000' ),
    ( 'CLI',                        '1001 0100 1111 1000' ),
    ( 'CLN',                        '1001 0100 1010 1000' ),
    #CLR       Rd                [EOR]                              # 0 <= d <= 31
    ( 'CLS',                        '1001 0100 1100 1000' ),
    ( 'CLT',                        '1001 0100 1110 1000' ),
    ( 'CLV',                        '1001 0100 1011 1000' ),
    ( 'CLZ',                        '1001 0100 1001 1000' ),
    ( 'COM       Rd',               '1001 010d dddd 0000' ),        # 0 <= d <= 31
    ( 'CP        Rd, Rr',           '0001 01rd dddd rrrr' ),        # 0 <= d <= 31,         0 <= r <= 31
    ( 'CPC       Rd, Rr',           '0000 01rd dddd rrrr' ),        # 0 <= d <= 31,         0 <= r <= 31
    ( 'CPI       Rh, K',            '0011 KKKK hhhh KKKK' ),        # 16 <= h <= 31,        0 <= K <= 255
    ( 'CPSE      Rd, Rr',           '0001 00rd dddd rrrr' ),        # 0 <= d <= 31,         0 <= r <= 31
    ( 'DEC       Rd',               '1001 010d dddd 1010' ),        # 0 <= d <= 31
    ( 'EICALL',                     '1001 0101 0001 1001' ),
    ( 'EIJMP',                      '1001 0100 0001 1001' ),
    ( 'ELPM',                       '1001 0101 1101 1000' ),
    ( 'ELPM      Rd, Z',            '1001 000d dddd 0110' ),        # 0 <= d <= 31
    ( 'ELPM      Rd, Z+',           '1001 000d dddd 0111' ),        # 0 <= d <= 31
    ( 'EOR       Rd, Rr',           '0010 01rd dddd rrrr' ),        # 0 <= d <= 31,         0 <= r <= 31
    ( 'FMUL      Rh, RH',           '0000 0011 0hhh 1HHH' ),        # 16 <= h <= 23,        16 <= H <= 23
    ( 'FMULS     Rh, RH',           '0000 0011 1hhh 0HHH' ),        # 16 <= h <= 23,        16 <= H <= 23
    ( 'FMULSU    Rh, RH',           '0000 0011 1hhh 1HHH' ),        # 16 <= h <= 23,        16 <= H <= 23
    ( 'ICALL',                      '1001 0101 0000 1001' ),
    ( 'IJMP',                       '1001 0100 0000 1001' ),
    ( 'IN        Rd, A',            '1011 0AAd dddd AAAA' ),        # 0 <= d <= 31,         0 <= A <= 63
    ( 'INC       Rd',               '1001 010d dddd 0011' ),        # 0 <= d <= 31
    ( 'JMP       K',                '1001 010K KKKK 110K KKKK KKKK KKKK KKKK' ),# 0 <= K < 4M
    ( 'LD        Rd, X',            '1001 000d dddd 1100' ),        # 0 <= d <= 31
    ( 'LD        Rd, X+',           '1001 000d dddd 1101' ),        # 0 <= d <= 31
    ( 'LD        Rd, -X',           '1001 000d dddd 1110' ),        # 0 <= d <= 31
    ( 'LD        Rd, Y',            '1000 000d dddd 1000' ),        # 0 <= d <= 31
    ( 'LD        Rd, Y+',           '1001 000d dddd 1001' ),        # 0 <= d <= 31
    ( 'LD        Rd, -Y',           '1001 000d dddd 1010' ),        # 0 <= d <= 31
    ( 'LDD       Rd, Y+q',          '10q0 qq0d dddd 1qqq' ),        # 0 <= d <= 31,         0 <= q <= 63
    ( 'LD        Rd, Z',            '1000 000d dddd 0000' ),        # 0 <= d <= 31
    ( 'LD        Rd, Z+',           '1001 000d dddd 0001' ),        # 0 <= d <= 31
    ( 'LD        Rd, -Z',           '1001 000d dddd 0010' ),        # 0 <= d <= 31
    ( 'LDD       Rd, Z+q',          '10q0 qq0d dddd 0qqq' ),        # 0 <= d <= 31,         0 <= q <= 63
    ( 'LDI       Rh, K',            '1110 KKKK hhhh KKKK' ),        # 16 <= h <= 31,        0 <= K <= 255
    ( 'LDS       Rr, K',            '1001 000r rrrr 0000 KKKK KKKK KKKK KKKK' ),# 0 <= d <= 31, 0 <= K <= 65535
    ( 'LPM',                        '1001 0101 1100 1000' ),        # R0 implied
    ( 'LPM       Rd, Z',            '1001 000d dddd 0100' ),        # 0 <= d <= 31
    ( 'LPM       Rd, Z+',           '1001 000d dddd 0101' ),        # 0 <= d <= 31
    #LSL       Rd                [ADD]                              # 0 <= d <= 31
    ( 'LSR       Rd',               '1001 010d dddd 0110' ),        # 0 <= d <= 31
    ( 'MOV       Rd, Rr',           '0010 11rd dddd rrrr' ),        # 0 <= d <= 31,         0 <= r <= 31
    ( 'MOVW      Rp+1:Rp, RP+1:RP', '0000 0001 pppp PPPP' ),        # p \in {0,2,...,30},   P \in {0,2,...,30}
    ( 'MUL       Rd, Rr',           '1001 11rd dddd rrrr' ),        # 0 <= d <= 31,         0 <= r <= 31
    ( 'MULS      Rh, RH',           '0000 0010 hhhh HHHH' ),        # 16 <= h <= 31,        16 <= H <= 31
    ( 'MULSU     Rh, RH',           '0000 0011 0hhh 0HHH' ),        # 16 <= h <= 23,        16 <= H <= 23
    ( 'NEG       Rd',               '1001 010d dddd 0001' ),        # 0 <= d <= 31
    ( 'NOP',                        '0000 0000 0000 0000' ),
    ( 'OR        Rd, Rr',           '0010 10rd dddd rrrr' ),        # 0 <= d <= 31,         0 <= r <= 31
    ( 'ORI       Rh, K',            '0110 KKKK hhhh KKKK' ),        # 16 <= h <= 31,        0 <= K <= 255
    ( 'OUT       A, Rr',            '1011 1AAr rrrr AAAA' ),        # 0 <= r <= 31,         0 <= A <= 63
    ( 'POP       Rd',               '1001 000d dddd 1111' ),        # 0 <= d <= 31
    ( 'PUSH      Rr',               '1001 001r rrrr 1111' ),        # 0 <= r <= 31
    ( 'RCALL     .k',               '1101 kkkk kkkk kkkk' ),        # -2K <= k < 2K
    ( 'RET',                        '1001 0101 0000 1000' ),
    ( 'RETI',                       '1001 0101 0001 1000' ),
    ( 'RJMP      .k',               '1100 kkkk kkkk kkkk' ),        # -2K <= k <= 2K
    #ROL       Rd                [ADC]                              # 0 <= d <= 31
    ( 'ROR       Rd',               '1001 010d dddd 0111' ),        # 0 <= d <= 31
    ( 'SBC       Rd, Rr',           '0000 10rd dddd rrrr' ),        # 0 <= d <= 31,         0 <= r <= 31
    ( 'SBCI      Rh, K',            '0100 KKKK hhhh KKKK' ),        # 16 <= h <= 31,        0 <= K <= 255
    ( 'SBI       A, b',             '1001 1010 AAAA Abbb' ),        # 0 <= A <= 31,         0 <= b <= 7
    ( 'SBIC      A, b',             '1001 1001 AAAA Abbb' ),        # 0 <= A <= 31,         0 <= b <= 7
    ( 'SBIS      A, b',             '1001 1011 AAAA Abbb' ),        # 0 <= A <= 31,         0 <= b <= 7
    ( 'SBIW      Rp+1:Rp, K',       '1001 0111 KKpp KKKK' ),        # p \in {24,26,28,30},  0 <= K <= 63
    ( 'SBR       Rh, K',            '0110 KKKK hhhh KKKK' ),        # 16 <= h <= 31,        0 <= K <= 255
    ( 'SBRC      Rr, b',            '1111 110r rrrr 0bbb' ),        # 0 <= r <= 31,         0 <= b <= 7
    ( 'SBRS      Rr, b',            '1111 111r rrrr 0bbb' ),        # 0 <= r <= 31,         0 <= b <= 7
    ( 'SEC',                        '1001 0100 0000 1000' ),
    ( 'SEH',                        '1001 0100 0101 1000' ),
    ( 'SEI',                        '1001 0100 0111 1000' ),
    ( 'SEN',                        '1001 0100 0010 1000' ),
    #( 'SER       Rh',               '1110 1111 hhhh 1111' ),        # [LDI] 16 <= d <= 31
    ( 'SES',                        '1001 0100 0100 1000' ),
    ( 'SET',                        '1001 0100 0110 1000' ),
    ( 'SEV',                        '1001 0100 0011 1000' ),
    ( 'SEZ',                        '1001 0100 0001 1000' ),
    ( 'SLEEP',                      '1001 0101 1000 1000' ),
    ( 'SPM',                        '1001 0101 1110 1000' ),
    ( 'ST        X, Rr',            '1001 001r rrrr 1100' ),        # 0 <= r <= 31
    ( 'ST        X+, Rr',           '1001 001r rrrr 1101' ),        # 0 <= r <= 31
    ( 'ST        -X, Rr',           '1001 001r rrrr 1110' ),        # 0 <= r <= 31
    ( 'ST        Y, Rr',            '1000 001r rrrr 1000' ),        # 0 <= r <= 31
    ( 'ST        Y+, Rr',           '1001 001r rrrr 1001' ),        # 0 <= r <= 31
    ( 'ST        -Y, Rr',           '1001 001r rrrr 1010' ),        # 0 <= r <= 31
    ( 'STD       Y+q, Rr',          '10q0 qq1r rrrr 1qqq' ),        # 0 <= r <= 31,         0 <= q <= 63
    ( 'ST        Z, Rr',            '1000 001r rrrr 0000' ),        # 0 <= r <= 31
    ( 'ST        Z+, Rr',           '1001 001r rrrr 0001' ),        # 0 <= r <= 31
    ( 'ST        -Z, Rr',           '1001 001r rrrr 0010' ),        # 0 <= r <= 31
    ( 'STD       Z+q, Rr',          '10q0 qq1r rrrr 0qqq' ),        # 0 <= r <= 31          0 <= q <= 63
    ( 'STS       K, Rr',            '1001 001r rrrr 0000 KKKK KKKK KKKK KKKK' ),# 0 <= r <= 31, 0 <= K <= 65535
    ( 'SUB       Rd, Rr',           '0001 10rd dddd rrrr' ),        # 0 <= d <= 31,         0 <= r <= 31
    ( 'SUBI      Rh, K',            '0101 KKKK hhhh KKKK' ),        # 16 <= h <= 31,        0 <= K <= 255
    ( 'SWAP      Rd',               '1001 010d dddd 0010' ),        # 0 <= d <= 31
    #TST       Rd                [AND]                              # 0 <= d <= 31
    ( 'WDR',                        '1001 0101 1010 1000' ),
]



def FindStartEnd(oprd_chr, oprd_str, end_idx):
    # Find start of operand string.
    st = end_idx
    while st >= 0 and oprd_str[st] != oprd_chr:
        st -= 1
        continue

    # Find end of oprand string.
    ed = st
    while ed >= 0 and oprd_str[ed] == oprd_chr:
        ed -= 1
        continue

    return st, ed


def MkAbsoluteOperand(oprd_chr, oprd_str, word):
    val = shifts = num_zeros = total_num_ones = 0
    end_idx = len(oprd_str) - 1
    while end_idx > 0:
        st, ed = FindStartEnd(oprd_chr, oprd_str, end_idx)
        num_ones = st - ed
        total_num_ones += num_ones
        if num_ones <= 0:
            break
        mask = int('1' * num_ones, 2) << (len(oprd_str) - st - 1)
        num_zeros = end_idx - st
        shifts += num_zeros
        val |= (word & mask) >> shifts
        end_idx = ed
    return val, total_num_ones


def Get16ByteOpc(hex_fmt, address):
    l = hex_fmt.GetMemoryBytes()[address]
    h = hex_fmt.GetMemoryBytes()[address + 1]
    opc = (h << 8) | l
    return opc


def Get16ByteOpcSafe(hex_fmt, address):
    if hex_fmt.GetNumBytes() < address + 2:
        return None
    return Get16ByteOpc(hex_fmt, address)


def GetMasks(opc_rec):
    opc_str = opc_rec[1].replace(' ', '')
    opc = int(''.join([ '1' if c == '1' else '0' for c in opc_str ]), 2)
    opc_mask = int(''.join([ '1' if c in '01' else '0' for c in opc_str ]), 2)
    oprd_set = set([ c for c in opc_str if c not in '01' ])
    oprd_masks = [ int(''.join([ '1' if c == s else '0' for c in opc_str ]), 2) for s in oprd_set ]
    return opc, opc_mask, oprd_set, oprd_masks


def GetRelative7bit(word):
    k = (word & 0x7f) << 1
    # Convert address to two's complement for negative values.
    k = k - (((k & 0x80) == 0x80) * ((0xff - 1) + 2))
    return k


def GetRelative12bit(word):
    k = (word & 0x0fff) << 1
    # Convert address to two's complement for negative values.
    k = k - (((k & 0x1000) == 0x1000) * ((0x1fff - 1) + 2))
    return k


def Disassemble(hex_fmt, pc, is_verbose_paired_regs=False):
    hex_word = Get16ByteOpcSafe(hex_fmt, pc)
    for inst_rec in INSTRUCTIONS:
        opc, opc_mask, oprd_set, oprd_masks = GetMasks(inst_rec)
        word = hex_word
        num_words = 1
        if opc_mask > 0xffff:
            word_2 = Get16ByteOpcSafe(hex_fmt, pc + 2)
            if word_2 == None:
                continue

            num_words = 2
            word = (word << 16) | word_2

        if (word & opc_mask) == opc:
            if not oprd_set:
                return num_words, inst_rec[0]

            comment = ''
            inst_fmt = inst_rec[0]
            for oprd in oprd_set:
                if 'K' == oprd:
                    k, num_bits = MkAbsoluteOperand('K', inst_rec[1].replace(' ', ''), word)
                    num_hex_digits = str(min(4, ((num_bits + 7) // 8) * 2))
                    inst_fmt = inst_fmt.replace('K', '0x{:0' + num_hex_digits + 'x}').format(k)
                elif 'k' == oprd:
                    k, num_bits = MkAbsoluteOperand('k', inst_rec[1].replace(' ', ''), word)
                    rel_k = GetRelative7bit(k) if num_bits == 7 else GetRelative12bit(k)
                    inst_fmt = inst_fmt.replace('k', '{:+d}').format(rel_k)
                    comment = '\t; 0x{:x}'.format(pc + rel_k + 2)
                elif 'A' == oprd:
                    a, num_bits = MkAbsoluteOperand('A', inst_rec[1].replace(' ', ''), word)
                    num_hex_digits = str(((num_bits + 7) // 8) * 2)
                    inst_fmt = inst_fmt.replace('A', '${:0' + num_hex_digits + 'x}').format(a)
                elif oprd in ABS_OPRDS:
                    oprd_chr = ABS_OPRDS[ABS_OPRDS.index(oprd)]
                    v, num_bits = MkAbsoluteOperand(oprd_chr, inst_rec[1].replace(' ', ''), word)
                    inst_fmt = inst_fmt.replace(oprd_chr, '{}').format(v)
                elif oprd in [ 'p', 'P' ]:
                    oprd_chr = oprd if 'p' in oprd else 'P'
                    p, num_bits = MkAbsoluteOperand(oprd_chr, inst_rec[1].replace(' ', ''), word)
                    p = p * 2 + ((num_bits == 2) * 24)
                    if is_verbose_paired_regs:
                        inst_fmt = inst_fmt.replace(oprd_chr + '+1', '{}')
                        inst_fmt = inst_fmt.replace(oprd_chr, '{}').format(p + 1, p)
                    else:
                        inst_fmt = inst_fmt.replace(oprd_chr + '+1:R' + oprd_chr, '{}').format(p)
                elif oprd in [ 'h', 'H' ]:
                    oprd_chr = 'h' if 'h' in oprd else 'H'
                    h, num_bits = MkAbsoluteOperand(oprd_chr, inst_rec[1].replace(' ', ''), word)
                    h += 16
                    inst_fmt = inst_fmt.replace(oprd_chr, '{}').format(h)

            if inst_fmt.startswith('LDI'):
                k, num_bits = MkAbsoluteOperand('K', inst_rec[1].replace(' ', ''), word)
                if k == 0xff and num_bits == 8:
                    h, num_bits = MkAbsoluteOperand('h', inst_rec[1].replace(' ', ''), word)
                    h += 16
                    inst_fmt = 'SER       R{}'.format(h)

            return num_words, inst_fmt + comment

    return 1, '.dw 0x{:04x}'.format(hex_word)



def DoMain():
    sys.argv.append(DEFAULT_HEX_FILE)

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

    pc = 0
    hex_num_bytes = hex_fmt.GetNumBytes()
    while pc < hex_num_bytes:
        num_words, menem = Disassemble(hex_fmt, pc)
        hex_mem = ''
        for i in range(2 * num_words):
            b = hex_fmt.GetMemoryBytes()[pc + 2 * num_words - i - 1]
            hex_mem += '{}{:02x}'.format(' ' if hex_mem else '', b)
        print('{:>4x}:\t{:<9s}\t{}'.format(pc, hex_mem, menem))
        pc += num_words * 2


if __name__ == '__main__':
    DoMain()

