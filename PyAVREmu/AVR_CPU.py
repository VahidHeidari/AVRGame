#******************************************************************************
#*                                                                            *
#*                      AVR Game Demo                                         *
#*                                                                            *
#* This is AVRGame project. AVRGame is a small, low cost, and open source     *
#* hand held console based on AVR microcontroller.                            *
#******************************************************************************

import os

import ATmega8_regs
import AVR_disassemble
import draw_util



#IS_PRINT_ASM = True
IS_PRINT_ASM = False

IS_TRACK_JUMPS  = True
IS_LOG_READ_IO  = False
IS_LOG_WRITE_IO = False
IS_LOG_WRITE_RAM = False

SREG_I = 7
SREG_T = 6
SREG_H = 5
SREG_S = 4
SREG_V = 3
SREG_N = 2
SREG_Z = 1
SREG_C = 0

SP_MASK = (1 << 11) - 1

frame_num = 1
PortD_Data = []
OldPortD_Data = []



def ClearSREG(cpu, flg):
    cpu.SREG &= ~(1 << flg)
    cpu.SREG &= 0xff
    cpu.IO[ATmega8_regs.IO_NAMES.index('SREG')] = cpu.SREG


def SetSREG(cpu, flg):
    cpu.SREG |= (1 << flg)
    cpu.IO[ATmega8_regs.IO_NAMES.index('SREG')] = cpu.SREG


def SetSREGValue(cpu, flg, bit_val):
    cpu.SREG &= ~(1 << flg)
    cpu.SREG &= 0xff
    cpu.SREG |= (bit_val << flg)
    cpu.IO[ATmega8_regs.IO_NAMES.index('SREG')] = cpu.SREG


def GetSREG(cpu, flg):
    return (cpu.SREG & (1 << flg)) == (1 << flg)


#
# ADC, ADD:
#  ( Rd3 & Rr3) | (Rr3 & ~R3) | (~R3 & Rd3)
#
# CP, CPI, CPC, SBC, SBCI, SUB, SUBI:
#  (~Rd3 & Rr3) | (Rr3 &  R3) | (R3 & ~Rd3)
#  (~Rd3 &  K3) | ( K3 &  R3) | (R3 & ~Rd3)
#
def UpdateH(cpu, Rd, Rr, R):
    r = (~Rd & Rr) | (Rr & R) | (R & ~Rd)
    h = (r >> 3) & 1
    SetSREGValue(cpu, SREG_H, h)


#
# ADC, ADD:
#  ( Rd7 & Rr7) | (Rr7 & ~R7) | (~R7 &  Rd7)
#
# CP, CPI, CPC, SBC, SBCI, SUB, SUBI:
#  (~Rd7 & Rr7) | (Rr7 &  R7) | ( R7 & ~Rd7)
#  (~Rd7 &  K7) | ( K7 &  R7) | ( R7 & ~Rd7)
#
# ADIW:
#  ~R15 & Rdh7
#
# SBIW:
#  R15 & ~Rdh7
#
def UpdateC(cpu, Rd, Rr, R, num_bits=8):
    r = (~Rd & Rr) | (Rr & R) | (R & ~Rd)
    c = (r >> (num_bits - 1)) & 1
    SetSREGValue(cpu, SREG_C, c)


def UpdateC16bit(cpu, Pd, R):
    Pd15 = (Pd & (1 << 15)) == (1 << 15)
    R15  = (R  & (1 << 15)) == (1 << 15)
    c = ~R15 & Pd15
    SetSREGValue(cpu, SREG_C, c)


# CP:  N ^ V
# CPI: N ^ V
def UpdateS(cpu):
    n = GetSREG(cpu, SREG_N)
    v = GetSREG(cpu, SREG_V)
    s = n ^ v
    SetSREGValue(cpu, SREG_S, s)


#
# ADC, ADD:
#  (Rd7 &  Rr7 & ~R7) | (~Rd7 & ~Rr7 & R7)
#
# CP, CPI, CPC, SBC, SBCI, SUB, SUBI:
#  (Rd7 & ~Rr7 & ~R7) | (~Rd7 &  Rr7 & R7)
#  (Rd7 &  ~K7 & ~R7) | (~Rd7 &   K7 & R7)
#
# ADIW:
#  ~Rdh7 & R15
#
# DEC:
#  ~R7 & R6 & R5 & R4 & R3 & R2 & R1 & R0
#
# INC:
#  R7 & ~R6 & ~R5 & ~R4 & ~R3 & ~R2 & ~R1 & ~R0
#
# LSR:
#  N & C
#
# SBIW:
#  Rdh7 & ~R15
#
def UpdateV(cpu, Rd, Rr, R, num_bits=8):
    r = (Rd & ~Rr & ~R) | (~Rd & Rr & R)
    v = (r >> (num_bits - 1)) & 1
    SetSREGValue(cpu, SREG_V, v)


def UpdateV16bit(cpu, Pd, R):
    Pd15 = (Pd & (1 << 15)) == (1 << 15)
    R15  = (R  & (1 << 15)) == (1 << 15)
    c = R15 & ~Pd15
    SetSREGValue(cpu, SREG_V, c)


def UpdateN(cpu, R, num_bits=8):
    num_bits -= 1
    R7 = (R & (1 << num_bits)) == (1 << num_bits)
    SetSREGValue(cpu, SREG_N, R7)


def UpdateZ(cpu, R):
    z = R == 0
    SetSREGValue(cpu, SREG_Z, z)


def PushPCToStack(cpu):
    ret_addr = cpu.PC + 2
    cpu.ret_addrs.append(ret_addr)
    if cpu.is_PC_16_bits:               # PC is 16 bits.
        cpu.WriteRAM(cpu.SP, ret_addr & 0xff)
        cpu.SP -= 1
        cpu.WriteRAM(cpu.SP, (ret_addr >> 8) & 0xff)
        cpu.SP -= 1
    else:                               # PC is 22 bits.
        cpu.WriteRAM(cpu.SP, ret_addr & 0xff)
        cpu.SP -= 1
        cpu.WriteRAM(cpu.SP, (ret_addr >> 8) & 0xff)
        cpu.SP -= 1
        cpu.WriteRAM(cpu.SP, (ret_addr >> 16) & 0x3f)
        cpu.SP -= 1
    cpu.WriteSP(cpu.SP)


def PopPCFromStack(cpu):
    if cpu.is_PC_16_bits:
        cpu.SP += 1
        h = cpu.ReadRAM(cpu.SP)
        cpu.SP += 1
        l = cpu.ReadRAM(cpu.SP)
        ret_addr = (h << 8) | l
    else:
        cpu.SP += 1
        p = cpu.ReadRAM(cpu.SP)
        cpu.SP += 1
        h = cpu.ReadRAM(cpu.SP)
        cpu.SP += 1
        l = cpu.ReadRAM(cpu.SP)
        ret_addr = (m << 16) | (h << 8) | l
    cpu.PC = ret_addr
    cpu.WriteSP(cpu.SP)
    del cpu.ret_addrs[-1]


def IncPC(cpu, k=2):
    cpu.PC += k
    if (cpu.PC & 1) != 0:
        raise Exception('Error in PC: {}  0x{:04x}  {}!'.format(cpu.PC, cpu.PC, bin(cpu.PC)))


def SetPC(cpu, K):
    cpu.PC = K


def IncCycles(cpu, v=1):
    cpu.cycles += v


def ReadProgMem(hex_fmt, addr):
    wrd = hex_fmt.GetMemoryBytes()[addr]
    return wrd



# ADC: Add with Carry
#
# ROL: Rotate Left trough Carry
def ADC(cpu, Rd, Rr):
    c = 0 + GetSREG(cpu, SREG_C)
    R = (cpu.regs[Rd] + cpu.regs[Rr] + c) & 0xff
    UpdateH(cpu, ~cpu.regs[Rd], cpu.regs[Rr], ~R)
    UpdateC(cpu, ~cpu.regs[Rd], cpu.regs[Rr], ~R)
    UpdateV(cpu, cpu.regs[Rd], ~cpu.regs[Rr], R)
    UpdateN(cpu, R)
    UpdateZ(cpu, R)
    UpdateS(cpu)
    cpu.regs[Rd] = R
    IncPC(cpu)
    IncCycles(cpu)


# ADD: Add without Carry
#
# LSL: Logical Shift Left
def ADD(cpu, Rd, Rr):
    R = (cpu.regs[Rd] + cpu.regs[Rr]) & 0xff
    UpdateH(cpu, ~cpu.regs[Rd], cpu.regs[Rr], ~R)
    UpdateC(cpu, ~cpu.regs[Rd], cpu.regs[Rr], ~R)
    UpdateV(cpu, cpu.regs[Rd], ~cpu.regs[Rr], R)
    UpdateN(cpu, R)
    UpdateZ(cpu, R)
    UpdateS(cpu)
    cpu.regs[Rd] = R
    IncPC(cpu)
    IncCycles(cpu)


# Add Immediate to Word
def ADIW(cpu, Rd, K):
    Pd = (cpu.regs[Rd + 1] << 8) | cpu.regs[Rd]
    R = Pd + K
    UpdateC16bit(cpu, Pd, R)
    UpdateV16bit(cpu, Pd, R)
    UpdateN(cpu, R, 16)
    UpdateZ(cpu, R)
    UpdateS(cpu)
    cpu.regs[Rd] = R & 0xff
    cpu.regs[Rd + 1] = (R >> 8) & 0xff
    IncPC(cpu)
    IncCycles(cpu, 2)


# AND: Logical AND
#
# TST: Test for Zero or Minus
def AND(cpu, Rd, Rr):
    R = cpu.regs[Rd] & cpu.regs[Rr]
    ClearSREG(cpu, SREG_V)
    UpdateN(cpu, R)
    UpdateZ(cpu, R)
    UpdateS(cpu)
    cpu.regs[Rd] = R
    IncPC(cpu)
    IncCycles(cpu)


# ANDI: Logical AND with Immediate
#
# CBR: Clear Bits in Register
def ANDI(cpu, Rd, K):
    R = cpu.regs[Rd] & K
    ClearSREG(cpu, SREG_V)
    UpdateN(cpu, R)
    UpdateZ(cpu, R)
    UpdateS(cpu)
    cpu.regs[Rd] = R
    IncPC(cpu)
    IncCycles(cpu)


# Arithmetic Shift Right
def ASR(cpu, Rd):
    b7 = (cpu.regs[rd] & (1 << 7)) == (1 << 7)
    c = cpu.regs[Rd] & 1
    R = (b7 << 7) | (cpu.regs[Rd] >> 1)
    SetSREGValue(cpu, SREG_C, c)
    SetSREGValue(cpu, SREG_N, b7)
    UpdateZ(cpu, R)
    SetSREGValue(cpu, SREG_V, c ^ b7)
    UpdateS(cpu)
    cpu.regs[rd] = R
    IncPC(cpu)
    IncCycles(cpu)


# BCLR: Bit Clear in SREG
#
# CLC: Clear Carry Flag
# CLH: Clear Half Carry Flag
# CLI: Clear Global Interrupt Flag
# CLN: Clear Negative Flag
# CLS: Clear Signed Flag
# CLT: Clear T Flag
# CLV: Clear Overflow Flag
# CLZ: Clear Zero Flag
def BCLR(cpu, s):
    ClearSREG(cpu, s)
    IncPC(cpu)
    IncCycles(cpu)


# Bit Load from the T Flag in SREG to a Bit in Register
def BLD(cpu, Rd, b):
    t = GetSREG(cpu, SREG_T)
    cpu.regs[Rd] &= ~(1 << b)
    cpu.regs[Rd] |= (t << b)
    IncPC(cpu)
    IncCycles(cpu)


# BRBC: Branch if Bit in SREG is Cleared
#
# BRCC: Branch if Carry Cleared (C == 0)
# BRGE: Branch if Greater of Equal (Signed) (S = N ^ V == 0)
# BRHC: Branch if Half Carry Flag is Cleared (H == 0)
# BRID: Branch if Global Interrupt is Disabled (I == 0)
# BRNE: Branch if Not Equal (Z == 0)
# BRPL: Branch if Plus (N == 0)
# BRSH: Branch if Same or Higher (Unsigned) (C == 0)
# BRTC: Branch if the T Flag is Cleared (T == 0)
# BRVC: Branch if Overflow Cleared (V == 0)
def BRBC(cpu, s, k):
    b = GetSREG(cpu, s)
    if not b:
        IncPC(cpu, k + 2)
        IncCycles(cpu, 2)
    else:
        IncPC(cpu)
        IncCycles(cpu)


# BRBS: Branch if Bit in SREG is Set
#
# BRCS: Branch if Carry Set (C == 1)
# BREQ: Branch if Equal (Z == 1)
# BRHS: Branch if Half Carry Flag is Set (H == 1)
# BRIE: Branch if Global Interrupt is Enabled (I == 1)
# BRLO: Branch if Lower (Unsigned) (C == 1)
# BRLT: Branch if Less Than (Signed) (S = N ^ V == 1)
# BRMI: Branch if Minus (N == 1)
# BRTS: Branch if the T Flag is Set (T == 1)
# BRVS: Branch if Overflow Set (V == 1)
def BRBS(cpu, s, k):
    b = GetSREG(cpu, s)
    if b:
        IncPC(cpu, k + 2)
        IncCycles(cpu, 2)
    else:
        IncPC(cpu)
        IncCycles(cpu)


# Break
def BREAK(cpu):
    IncPC(cpu)
    IncCycles(cpu)


# BSET: Bit Set in SREG
#
# SEC: Set Carry Flag
# SEH: Set Half Carry Flag
# SEI: Set Global Interrupt Flag
# SEN: Set Negative Flag
# SES: Set Signed Flag
# SET: Set T Flag
# SEV: Set Overflow Flag
# SEZ: Set Zero Flag
def BSET(cpu, s):
    SetSREG(cpu, s)
    IncPC(cpu)
    IncCycles(cpu)


# Bit Store from Bit in Register to T Flag in SREG
def BST(cpu, Rd, b):
    Rdb = (cpu.regs[Rd] & (1 << b)) == (1 << b)
    SetSREGValue(cpu, SREG_T, Rdb)
    IncPC(cpu)
    IncCycles(cpu)


# Long Call to a Subroutine
def CALL(cpu, K):
    PushPCToStack(cpu)
    SetPC(cpu, K)
    IncCycles(cpu, 4 + (0 + (cpu.is_PC_16_bits == False)))


# Clear Bit in I/O Register
def CBI(cpu, A, b):
    cpu.WriteIO_ClearBit(A, b)
    IncPC(cpu)
    IncCycles(cpu, 2)


# One's Complement
def COM(cpu, Rd):
    R = (0xff - cpu.regs[Rd]) & 0xff
    SetSREG(cpu, SREG_C)
    ClearSREG(cpu, SREG_V)
    UpdateN(cpu, R)
    UpdateZ(cpu, R)
    UpdateS(cpu)
    cpu.regs[Rd] = R
    IncPC(cpu)
    IncCycles(cpu)


# Compare
def CP(cpu, Rd, Rr):
    R = (cpu.regs[Rd] - cpu.regs[Rr]) & 0xff
    UpdateH(cpu, cpu.regs[Rd], cpu.regs[Rr], R)
    UpdateC(cpu, cpu.regs[Rd], cpu.regs[Rr], R)
    UpdateV(cpu, cpu.regs[Rd], cpu.regs[Rr], R)
    UpdateN(cpu, R)
    UpdateZ(cpu, R)
    UpdateS(cpu)
    IncPC(cpu)
    IncCycles(cpu)


# Comare with Carry
def CPC(cpu, Rd, Rr):
    c = 0 + GetSREG(cpu, SREG_C)
    R = (cpu.regs[Rd] - cpu.regs[Rr] - c) & 0xff
    UpdateH(cpu, cpu.regs[Rd], cpu.regs[Rr], R)
    UpdateC(cpu, cpu.regs[Rd], cpu.regs[Rr], R)
    UpdateV(cpu, cpu.regs[Rd], cpu.regs[Rr], R)
    UpdateN(cpu, R)
    z = (R == 0) & GetSREG(cpu, SREG_Z)
    SetSREGValue(cpu, SREG_Z, z)
    UpdateS(cpu)
    IncPC(cpu)
    IncCycles(cpu)


# Compare with Immediate
def CPI(cpu, Rd, K):
    R = (cpu.regs[Rd] - K) & 0xff
    UpdateH(cpu, cpu.regs[Rd], K, R)
    UpdateC(cpu, cpu.regs[Rd], K, R)
    UpdateV(cpu, cpu.regs[Rd], K, R)
    UpdateN(cpu, R)
    UpdateZ(cpu, R)
    UpdateS(cpu)
    IncPC(cpu)
    IncCycles(cpu)


# Compare Skip if Equal
def CPSE(cpu, Rd, Rr):
    if cpu.regs[Rd] == cpu.regs[Rr]:
        cpu.is_next_skip = True
    IncPC(cpu)
    IncCycles(cpu)


# Decrement
def DEC(cpu, Rd):
    R = (cpu.regs[Rd] - 1) & 0xff
    v = (cpu.regs[Rd] & 0xff) == 0x80
    SetSREGValue(cpu, SREG_V, v)
    UpdateN(cpu, R)
    UpdateZ(cpu, R)
    UpdateS(cpu)
    cpu.regs[Rd] = R
    IncPC(cpu)
    IncCycles(cpu)


# Extended Indirect Call to Subroutine
def EICALL(cpu):
    raise NotImplementedError("EICALL not implemented!")


# Extended Indirect Jump
def EIJMP(cpu):
    raise NotImplementedError("EIJMP not implemented!")


# Extended Load Program Memory
def ELPM(cpu):
    raise NotImplementedError("ELPM not implemented!")


# Extended Load Program Memory
def ELPM_Z(cpu, Rd):
    raise NotImplementedError("ELPM Rd, Z not implemented!")


# Extended Load Program Memory
def ELPM_Z_Plus(cpu, Rd):
    raise NotImplementedError("ELPM Rd, Z+ not implemented!")


# EOR: Exclusive OR
#
# CLR: Clear Register
def EOR(cpu, Rd, Rr):
    R = cpu.regs[Rd] ^ cpu.regs[Rr]
    ClearSREG(cpu, SREG_V)
    UpdateN(cpu, R)
    UpdateZ(cpu, R)
    UpdateS(cpu)
    cpu.regs[Rd] = R
    IncPC(cpu)
    IncCycles(cpu)


# Fractional Multiply Unsiged
def FMUL(cpu, Rd, Rr):
    raise NotImplementedError("FMUL not implemented!")


# Fractional Multiply Signed
def FMULS(cpu, Rd, Rr):
    raise NotImplementedError("FMUL not implemented!")


# Fractional Multiply Signed with Unsigned
def FMULSU(cpu, Rd, Rr):
    raise NotImplementedError("FMULSU not implemented!")


# Indirect Call to Subroutine
def ICALL(cpu):
    PushPCToStack(cpu)
    SetPC(cpu, cpu.GetZ())
    IncCycles(cpu, 3 + (0 + (cpu.is_PC_16_bits == False)))


# Indirect Jump
def IJMP(cpu):
    SetPC(cpu, cpu.GetZ())
    IncCycles(cpu, 2)


# Load an I/O Location to Register
def IN(cpu, A, Rd):
    cpu.regs[Rd] = cpu.ReadIO(A)
    IncPC(cpu)
    IncCycles(cpu)


# Increment
def INC(cpu, Rd):
    R = (cpu.regs[Rd] + 1) & 0xff
    v = (cpu.regs[Rd] & 0xff) == 0x7f
    SetSREGValue(cpu, SREG_V, v)
    UpdateN(cpu, R)
    UpdateZ(cpu, R)
    UpdateS(cpu)
    IncPC(cpu)
    IncCycles(cpu)


def JMP(cpu, K):
    cpu.PC = K
    IncCycles(cpu, 3)


# Load Indirect from Data Space to Register using Index X (Unchanged)
def LD_X(cpu, Rd):
    cpu.regs[Rd] = cpu.ReadRAM(cpu.GetX())
    IncPC(cpu)
    IncCycles(cpu, 2)


# Load Indirect from Data Space to Register using Index X (Post Incremented)
def LD_X_Plus(cpu, Rd):
    cpu.regs[Rd] = cpu.ReadRAM(cpu.GetX())
    cpu.SetX(cpu.GetX() + 1)
    IncPC(cpu)
    IncCycles(cpu, 2)


# Load Indirect from Data Space to Register using Index X (Pre Decremented)
def LD_Minus_X(cpu, Rd):
    cpu.SetX(cpu.GetX() - 1)
    cpu.regs[Rd] = cpu.ReadRAM(cpu.GetX())
    IncPC(cpu)
    IncCycles(cpu, 2)


# Load Indirect from Data Space to Register using Index Y (Post Incremented)
def LD_Y_Plus(cpu, Rd):
    cpu.regs[Rd] = cpu.ReadRAM(cpu.GetY())
    cpu.SetY(cpu.GetY() + 1)
    IncPC(cpu)
    IncCycles(cpu, 2)


# Load Indirect from Data Space to Register using Index Y (Pre Decremented)
def LD_Minus_Y(cpu, Rd):
    cpu.SetY(cpu.GetY() - 1)
    cpu.regs[Rd] = cpu.ReadRAM(cpu.GetY())
    IncPC(cpu)
    IncCycles(cpu, 2)


# Load Indirect from Data Space to Register using Index Y (Y:Unchanged, q:Displacement)
#
# LD    Rd, Y
# LDD   Rd, Y+q
def LDD_Y_q(cpu, Rd, q):
    cpu.regs[Rd] = cpu.ReadRAM((cpu.GetY() + q)) & 0xff
    IncPC(cpu)
    IncCycles(cpu, 2)


# Load Indirect From Data Space to Register using Index Z (Post Incremented)
def LD_Z_Plus(cpu, Rd):
    cpu.regs[Rd] = cpu.ReadRAM(cpu.GetZ())
    cpu.SetZ(cpu.GetZ() + 1)
    IncPC(cpu)
    IncCycles(cpu, 2)


# Load Indirect From Data Space to Register using Index Z (Pre Decremented)
def LD_Minus_Z(cpu, Rd):
    cpu.SetZ(cpu.GetZ() - 1)
    cpu.regs[Rd] = cpu.ReadRAM(cpu.GetZ())
    IncPC(cpu)
    IncCycles(cpu, 2)


# Load Indirect From Data Space to Register using Index Z (Z:Unchanged, q:Displacement)
#
# LD    Rd, Z
# LDD   Rd, Z+q
def LDD_Z_q(cpu, Rd, q):
    cpu.regs[Rd] = cpu.ReadRAM((cpu.GetZ() + q))
    IncPC(cpu)
    IncCycles(cpu, 2)


# LDI: Load Immediate
#
# SER: Set all Bits in Register
def LDI(cpu, Rd, K):
    cpu.regs[Rd] = K
    IncPC(cpu)
    IncCycles(cpu)


# Load Direct from Data Space
def LDS(cpu, Rd, K):
    cpu.regs[Rd] = cpu.ReadRAM(K)
    IncPC(cpu, 4)
    IncCycles(cpu, 2)


# Load Program Memory, R0 impled (Z:Unchanged)
def LPM(cpu, hex_fmt):
    cpu.regs[0] = ReadProgMem(hex_fmt, cpu.GetZ())
    IncPC(cpu)
    IncCycles(cpu, 3)


# Load Program Memory (Z:Unchanged)
def LPM_Z(cpu, hex_fmt, Rd):
    cpu.regs[Rd] = ReadProgMem(hex_fmt, cpu.GetZ())
    IncPC(cpu)
    IncCycles(cpu, 3)


# Load Program Memory (Z:Post Increment)
def LPM_Z_Plus(cpu, hex_fmt, Rd):
    cpu.regs[Rd] = ReadProgMem(hex_fmt, cpu.GetZ())
    cpu.SetZ(cpu.GetZ() + 1)
    IncPC(cpu)
    IncCycles(cpu, 3)


# Logical Shift Right
def LSR(cpu, Rd):
    c = cpu.regs[Rd] & 1
    R = (cpu.regs[Rd] >> 1) & 0xff
    ClearSREG(cpu, SREG_N)              # N = 0
    SetSREGValue(cpu, SREG_C, c)        # C = Rd0
    UpdateZ(cpu, R)                     # Z
    n = GetSREG(cpu, SREG_N)
    SetSREGValue(cpu, SREG_V, n ^ c)    # V
    UpdateS(cpu)                        # S
    cpu.regs[Rd] = R
    IncPC(cpu)
    IncCycles(cpu)


# Copy Register
def MOV(cpu, Rd, Rr):
    cpu.regs[Rd] = cpu.regs[Rr]
    IncPC(cpu)
    IncCycles(cpu)


# Copy Register Word
def MOVW(cpu, Rd, Rr):
    cpu.regs[Rd] = cpu.regs[Rr]
    cpu.regs[Rd + 1] = cpu.regs[Rr + 1]
    IncPC(cpu)
    IncCycles(cpu, 1)


# Multiply Unsigned
def MUL(cpu, Rd, Rr):
    raise NotImplementedError("MUL not implemented!")
    #R = cpu.regs[Rd] * cpu.regs[Rr]
    #c = (R & (1 << 15)) == (1 << 15)
    #SetSREGValue(cpu, SREG_C, c)
    #UpdateZ(cpu, R)
    #cpu.regs[0] = R & 0xff
    #cpu.regs[1] = (R >> 8) & 0xff
    #IncPC(cpu)
    #IncCycles(cpu, 2)


# Multiply Signed
def MULS(cpu, Rd, Rr):
    raise NotImplementedError("MULS not implemented!")


# Multiply Signed with Unsigned
def MULSU(cpu, Rd, Rr):
    raise NotImplementedError("MULSU not implemented!")


# Two's Complement
def NEG(cpu, Rd):
    R = (0 - cpu.regs[Rd]) & 0xff
    h = ((R & (1 << 3)) == (1 << 3)) | ((cpu.regs[Rd] & (1 << 3)) == (1 << 3))
    c = R != 0
    v = R == 0x80
    SetSREGValue(cpu, SREG_H, h)
    SetSREGValue(cpu, SREG_V, v)
    UpdateN(cpu, R)
    UpdateZ(cpu, R)
    SetSREGValue(cpu, SREG_C, c)
    UpdateS(cpu)
    cpu.regs[Rd] = R
    IncPC(cpu)
    IncCycles(cpu)


# No Operation
def NOP(cpu):
    IncPC(cpu)
    IncCycles(cpu)


# Logical OR
def OR(cpu, Rd, Rr):
    R = cpu.regs[Rd] | cpu.regs[Rr]
    ClearSREG(cpu, SREG_V)
    UpdateN(cpu, R)
    UpdateZ(cpu, R)
    UpdateS(cpu)
    cpu.regs[Rd] = R
    IncPC(cpu)
    IncCycles(cpu)


# ORI: Logical OR with Immediate
#
# SBR: Set Bits in Register
def ORI(cpu, Rd, K):
    R = cpu.regs[Rd] | K
    ClearSREG(cpu, SREG_V)
    UpdateN(cpu, R)
    UpdateZ(cpu, R)
    UpdateS(cpu)
    cpu.regs[Rd] = R
    IncPC(cpu)
    IncCycles(cpu)


# Store Register to I/O Location
def OUT(cpu, A, Rr):
    cpu.WriteIO(A, cpu.regs[Rr])
    IncPC(cpu)
    IncCycles(cpu)



# Pop Register from Stack
def POP(cpu, Rd):
    cpu.WriteSP(cpu.SP + 1)
    cpu.regs[Rd] = cpu.ReadRAM(cpu.SP)
    IncPC(cpu)
    IncCycles(cpu, 2)


# Push Register on Stack
def PUSH(cpu, Rr):
    cpu.WriteRAM(cpu.SP, cpu.regs[Rr])
    cpu.WriteSP(cpu.SP - 1)
    IncPC(cpu)
    IncCycles(cpu, 2)


# Relative Call to Subroutine
def RCALL(cpu, k):
    PushPCToStack(cpu)
    IncPC(cpu, k + 2)
    off_bits = 0 + (cpu.is_PC_16_bits == False)
    IncCycles(cpu, 3 + off_bits)


# Return from Subroutine
def RET(cpu):
    PopPCFromStack(cpu)
    off_bits = 0 + (cpu.is_PC_16_bits == False)
    IncCycles(cpu, 4 + off_bits)


# Return from Interrupt
def RETI(cpu):
    SetSREG(cpu, SREG_I)
    RET(cpu)


# Relative Jump
def RJMP(cpu, k):
    IncPC(cpu, k + 2)
    IncCycles(cpu, 2)


# Rotate Right through Carry
def ROR(cpu, Rd):
    c_old = GetSREG(cpu, SREG_C)
    c_new = (cpu.regs[Rd] & 1)
    R = ((cpu.regs[Rd] >> 1) & 0x7f) | (c_old << 8)
    Rd3 = (cpu.regs[Rd] & (1 << 3)) == (1 << 3)
    SetSREGValue(cpu, SREG_H, Rd3)
    UpdateN(cpu, R)
    UpdateZ(cpu, R)
    SetSREGValue(cpu, SREG_C, c_new)
    n = GetSREG(cpu, SREG_N)
    SetSREGValue(cpu, SREG_V, n ^ c_new)
    UpdateS(cpu)
    cpu.regs[Rd] = R
    IncPC(cpu)
    IncCycles(cpu)


# Subtract with Carry
def SBC(cpu, Rd, Rr):
    c = 0 + GetSREG(cpu, SREG_C)
    R = (cpu.regs[Rd] - cpu.regs[Rd] - c) & 0xff
    UpdateH(cpu, cpu.regs[Rd], cpu.regs[Rr], R)
    UpdateC(cpu, cpu.regs[Rd], cpu.regs[Rr], R)
    UpdateV(cpu, cpu.regs[Rd], cpu.regs[Rr], R)
    UpdateN(cpu, R)
    z = (R == 0) & GetSREG(cpu, SREG_Z)
    SetSREGValue(cpu, SREG_Z, z)
    UpdateS(cpu)
    cpu.regs[Rd] = R
    IncPC(cpu)
    IncCycles(cpu)


# Subtract Immediate with Carry
def SBCI(cpu, Rd, K):
    c = 0 + GetSREG(cpu, SREG_C)
    R = (cpu.regs[Rd] - K - c) & 0xff
    UpdateH(cpu, cpu.regs[Rd], K, R)
    UpdateC(cpu, cpu.regs[Rd], K, R)
    UpdateV(cpu, cpu.regs[Rd], K, R)
    UpdateN(cpu, R)
    z = (R == 0) & GetSREG(cpu, SREG_Z)
    SetSREGValue(cpu, SREG_Z, z)
    UpdateS(cpu)
    cpu.regs[Rd] = R
    IncPC(cpu)
    IncCycles(cpu)


# Set Bit in I/O Register
def SBI(cpu, A, b):
    cpu.WriteIO_SetBit(A, b)
    IncPC(cpu)
    IncCycles(cpu, 2)


# Skip if Bit in I/O Register Cleared
def SBIC(cpu, A, b):
    io_bit = cpu.ReadIOBit(A, b)
    if not io_bit:
        cpu.is_next_skip = True
    IncPC(cpu)
    IncCycles(cpu)


# Skip if Bit in I/O Register is Set
def SBIS(cpu, A, b):
    io_bit = cpu.ReadIOBit(A, b)
    if io_bit:
        cpu.is_next_skip = True
    IncPC(cpu)
    IncCycles(cpu)


# Subtract Immediate from Word
def SBIW(cpu, Rd, K):
    R = (((cpu.regs[Rd + 1] << 8) | cpu.regs[Rd]) - K) & 0xffff
    Pd15 = (cpu.regs[Rd + 1] & 0x80) == 0x80
    R15 = (R & 0x8000) == 0x8000
    SetSREGValue(cpu, SREG_V, Pd15 & ~R15)
    UpdateN(cpu, R, 16)
    UpdateZ(cpu, R)
    SetSREGValue(cpu, SREG_C, R15 & ~Pd15)
    UpdateS(cpu)
    cpu.regs[Rd]     = R & 0xff
    cpu.regs[Rd + 1] = (R >> 8) & 0xff
    IncPC(cpu)
    IncCycles(cpu, 2)


# Skip if Bit in Register is Cleared
def SBRC(cpu, Rr, b):
    b_val = (cpu.regs[Rr] & (1 << b))
    if not b_val:
        cpu.is_next_skip = True
    IncPC(cpu)
    IncCycles(cpu)


# Skip if Bit in Register is Set
def SBRS(cpu, Rr, b):
    b_val = (cpu.regs[Rr] & (1 << b)) == (1 << b)
    if b_val:
        cpu.is_next_skip = True
    IncPC(cpu)
    IncCycles(cpu)


# Sleep
def SLEEP(cpu):
    self.is_sleep = True
    IncPC(cpu)
    IncCycles(cpu)


# Store Program Memory
def SPM(cpu):
    raise NotImplementedError("SPM not implemented!")


# Store Indirect From Register to Data Space using Index X (Unchanged)
def ST_X(cpu, Rr):
    cpu.WriteRAM(cpu.GetX(), cpu.regs[Rr])
    IncPC(cpu)
    IncCycles(cpu, 2)


# Store Indirect From Register to Data Space using Index X (Post Increment)
def ST_X_Plus(cpu, Rr):
    cpu.WriteRAM(cpu.GetX(), cpu.regs[Rr])
    cpu.SetX(cpu.GetX() + 1)
    IncPC(cpu)
    IncCycles(cpu, 2)


# Store Indirect From Register to Data Space using Index X (Pre Decremented)
def ST_Minus_X(cpu, Rr):
    cpu.SetX(cpu.GetX() - 1)
    cpu.WriteRAM(cpu.GetX(), cpu.regs[Rr])
    IncPC(cpu)
    IncCycles(cpu, 2)


# Store Indirect From Register to Data Space using Index Y (Post Increment)
def ST_Y_Plus(cpu, Rr):
    cpu.WriteRAM(cpu.GetY(), cpu.regs[Rr])
    cpu.SetY(cpu.GetY() + 1)
    IncPC(cpu)
    IncCycles(cpu, 2)


# Store Indirect From Register to Data Space using Index Y (Pre Decremented)
def ST_Minus_Y(cpu, Rr):
    cpu.SetY(cpu.GetY() - 1)
    cpu.WriteRAM(cpu.GetY(), cpu.regs[Rr])
    IncPC(cpu)
    IncCycles(cpu, 2)


# Store Indirect From Register to Data Space using Index Y (Y:Unchanged, q:Displacement)
#
# ST    Y, Rd
# STD   Y+q, Rd
def STD_Y_q(cpu, Rr, q):
    cpu.WriteRAM(cpu.GetY() + q, cpu.regs[Rr])
    IncPC(cpu)
    IncCycles(cpu, 2)


# Store Indirect From Register to Data Space using Index Z (Post Incremented)
def ST_Z_Plus(cpu, Rr):
    cpu.WriteRAM(cpu.GetZ(), cpu.regs[Rr])
    cpu.SetZ(cpu.GetZ() + 1)
    IncPC(cpu)
    IncCycles(cpu, 2)


# Store Indirect From Register to Data Space using Index Z (Pre Decremented)
def ST_Minus_Z(cpu, Rr):
    cpu.SetZ(cpu.GetZ() - 1)
    cpu.WriteRAM(cpu.GetZ(), cpu.regs[Rr])
    IncPC(cpu)
    IncCycles(cpu, 2)


# Store Indirect From Register to Data Space using Index Z (Z:Unchanged, q:Displacement)
#
# ST    Z, Rd
# STD   Z+q, Rd
def STD_Z_q(cpu, Rr, q):
    cpu.WriteRAM(cpu.GetZ() + q, cpu.regs[Rr])
    IncPC(cpu)
    IncCycles(cpu, 2)


# Store Direct to Data Space
def STS(cpu, Rr, K):
    cpu.WriteRAM(K, cpu.regs[Rr])
    IncPC(cpu, 4)
    IncCycles(cpu, 2)


# Subtract without Carry
def SUB(cpu, Rd, Rr):
    R = (cpu.regs[Rd] - cpu.regs[Rr]) & 0xff
    UpdateH(cpu, cpu.regs[Rd], cpu.regs[Rr], R)
    UpdateC(cpu, cpu.regs[Rd], cpu.regs[Rr], R)
    UpdateV(cpu, cpu.regs[Rd], cpu.regs[Rr], R)
    UpdateN(cpu, R)
    UpdateZ(cpu, R)
    UpdateS(cpu)
    cpu.regs[Rd] = R
    IncPC(cpu)
    IncCycles(cpu)


# Subtract Immediate
def SUBI(cpu, Rd, K):
    R = (cpu.regs[Rd] - K) & 0xff
    UpdateH(cpu, cpu.regs[Rd], K, R)
    UpdateC(cpu, cpu.regs[Rd], K, R)
    UpdateV(cpu, cpu.regs[Rd], K, R)
    UpdateN(cpu, R)
    UpdateZ(cpu, R)
    UpdateS(cpu)
    cpu.regs[Rd] = R
    IncPC(cpu)
    IncCycles(cpu)


# Swap Nibbles
def SWAP(cpu, Rd):
    hi = (cpu.regs[Rd] >> 4) & 0x0f
    lo = cpu.regs[Rd] & 0x0f
    cpu.regs[Rd] = (lo << 4) | hi
    IncPC(cpu)
    IncCycles(cpu)


# Watchdog Rest
def WDR(cpu):
    # TODO: Implement the watchdog reset operation!
    IncPC(cpu)
    IncCycles(cpu)



INSTRUCTIONS = [
    ( 'ADC\tR{d}, R{r}',    '0001 11rd dddd rrrr',                      ADC,            ('d', 'r') ),   # 0 <= d <= 31,         0 <= r <= 31
    ( 'ADD\tR{d}, R{r}',    '0000 11rd dddd rrrr',                      ADD,            ('d', 'r') ),   # 0 <= d <= 31,         0 <= r <= 31
    ( 'ADIW\tR{p}, {K}',    '1001 0110 KKpp KKKK',                      ADIW,           ('p', 'K') ),   # p \in {24,26,28,30},  0 <= K <= 63
    ( 'AND\tR{d}, R{r}',    '0010 00rd dddd rrrr',                      AND,            ('d', 'r') ),   # 0 <= d <= 31,         0 <= r <= 31
    ( 'ANDI\tR{h}, {K}',    '0111 KKKK hhhh KKKK',                      ANDI,           ('h', 'K') ),   # 16 <= h <= 31,        0 <= K <= 255
    ( 'ASR\tR{d}',          '1001 010d dddd 0101',                      ASR,            ('d',)     ),   # 0 <= d <= 31
    ( 'BCLR\t{s}',          '1001 0100 1sss 1000',                      BCLR,           ('s',)     ),   # 0 <= s <= 7
    ( 'BLD\tR{d}, {b}',     '1111 100d dddd 0bbb',                      BLD,            ('d', 'b') ),   # 0 <= d <= 31,         0 <= b <= 7
    ( 'BRBC\t{s}, {k}',     '1111 01kk kkkk ksss',                      BRBC,           ('s', 'k') ),   # 0 <= s <= 7,          -64 <= k <= +63
    ( 'BRBS\t{s}, {k}',     '1111 00kk kkkk ksss',                      BRBS,           ('s', 'k') ),   # 0 <= s <= 7,          -64 <= k <= +63
    ( 'BREAK',              '1001 0101 1001 1000',                      BREAK,          ()         ),
    ( 'BSET\t{s}',          '1001 0100 0sss 1000',                      BSET,           ('s',)     ),   # 0 <= s <= 7
    ( 'BST\tR{d}, {b}',     '1111 101d dddd 0bbb',                      BST,            ('d', 'b') ),   # 0 <= d <= 31,         0 <= b <= 7
    ( 'CALL\t{K}',          '1001 010K KKKK 111K KKKK KKKK KKKK KKKK',  CALL,           ('K',)     ),   # 0 <= K < 64K, 0 <= K < 4M
    ( 'CBI\t{A}, {b}',      '1001 1000 AAAA Abbb',                      CBI,            ('A', 'b') ),   # 0 <= A <= 31,         0 <= b <= 7
    ( 'COM\tR{d}',          '1001 010d dddd 0000',                      COM,            ('d',)     ),   # 0 <= d <= 31
    ( 'CP\tR{d}, R{r}',     '0001 01rd dddd rrrr',                      CP,             ('d', 'r') ),   # 0 <= d <= 31,         0 <= r <= 31
    ( 'CPC\tR{d}, R{r}',    '0000 01rd dddd rrrr',                      CPC,            ('d', 'r') ),   # 0 <= d <= 31,         0 <= r <= 31
    ( 'CPI\tR{h}, {K}',     '0011 KKKK hhhh KKKK',                      CPI,            ('h', 'K') ),   # 16 <= h <= 31,        0 <= K <= 255
    ( 'CPSE\tR{d}, R{r}',   '0001 00rd dddd rrrr',                      CPSE,           ('d', 'r') ),   # 0 <= d <= 31,         0 <= r <= 31
    ( 'DEC\tR{d}',          '1001 010d dddd 1010',                      DEC,            ('d',)     ),   # 0 <= d <= 31
    ( 'EICALL',             '1001 0101 0001 1001',                      EICALL,         ()         ),
    ( 'EIJMP',              '1001 0100 0001 1001',                      EIJMP,          ()         ),
    ( 'ELPM',               '1001 0101 1101 1000',                      ELPM,           ()         ),
    ( 'ELPM\tR{d}, Z',      '1001 000d dddd 0110',                      ELPM_Z,         ('d')      ),   # 0 <= d <= 31
    ( 'ELPM\tR{d}, Z+',     '1001 000d dddd 0111',                      ELPM_Z_Plus,    ('d')      ),   # 0 <= d <= 31
    ( 'EOR\tR{d}, R{r}',    '0010 01rd dddd rrrr',                      EOR,            ('d', 'r') ),   # 0 <= d <= 31,         0 <= r <= 31
    ( 'FMUL\tR{h}, R{H}',   '0000 0011 0hhh 1HHH',                      FMUL,           ('h', 'H') ),   # 16 <= h <= 23,        16 <= H <= 23
    ( 'FMULS\tR{h}, R{H}',  '0000 0011 1hhh 0HHH',                      FMULS,          ('h', 'H') ),   # 16 <= h <= 23,        16 <= H <= 23
    ( 'FMULSU\tR{h}, R{H}', '0000 0011 1hhh 1HHH',                      FMULSU,         ('h', 'H') ),   # 16 <= h <= 23,        16 <= H <= 23
    ( 'ICALL',              '1001 0101 0000 1001',                      ICALL,          ()         ),
    ( 'IJMP',               '1001 0100 0000 1001',                      IJMP,           ()         ),
    ( 'IN\tR{d}, ${A}',     '1011 0AAd dddd AAAA',                      IN,             ('A', 'd') ),   # 0 <= d <= 31,         0 <= A <= 63
    ( 'INC\tR{d}',          '1001 010d dddd 0011',                      INC,            ('d',)     ),   # 0 <= d <= 31
    ( 'JMP\t{K}',           '1001 010K KKKK 110K KKKK KKKK KKKK KKKK',  JMP,            ('K',)     ),   # 0 <= K < 4M
    ( 'LD\tR{d}, X',        '1001 000d dddd 1100',                      LD_X,           ('d',)     ),   # 0 <= d <= 31
    ( 'LD\tR{d}, X+',       '1001 000d dddd 1101',                      LD_X_Plus,      ('d',)     ),   # 0 <= d <= 31
    ( 'LD\tR{d}, -X',       '1001 000d dddd 1110',                      LD_Minus_X,     ('d',)     ),   # 0 <= d <= 31
    ( 'LD\tR{d}, Y+',       '1001 000d dddd 1001',                      LD_Y_Plus,      ('d',)     ),   # 0 <= d <= 31
    ( 'LD\tR{d}, -Y',       '1001 000d dddd 1010',                      LD_Minus_Y,     ('d',)     ),   # 0 <= d <= 31
    ( 'LDD\tR{d}, Y+q',     '10q0 qq0d dddd 1qqq',                      LDD_Y_q,        ('d',)     ),   # 0 <= d <= 31,         0 <= q <= 63
    ( 'LD\tR{d}, Z+',       '1001 000d dddd 0001',                      LD_Z_Plus,      ('d',)     ),   # 0 <= d <= 31
    ( 'LD\tR{d}, -Z',       '1001 000d dddd 0010',                      LD_Minus_Z,     ('d',)     ),   # 0 <= d <= 31
    ( 'LDD\tR{d}, Z+q',     '10q0 qq0d dddd 0qqq',                      LDD_Z_q,        ('d', 'q') ),   # 0 <= d <= 31,         0 <= q <= 63
    ( 'LDI\tR{h}, {K}',     '1110 KKKK hhhh KKKK',                      LDI,            ('h', 'K') ),   # 16 <= h <= 31,        0 <= K <= 255
    ( 'LDS\tR{r}, {K}',     '1001 000r rrrr 0000 KKKK KKKK KKKK KKKK',  LDS,            ('r', 'K') ),   # 0 <= d <= 31, 0 <= K <= 65535
    ( 'LPM',                '1001 0101 1100 1000',                      LPM,            ('F',)     ),   # R0 implied
    ( 'LPM\tR{d}, Z',       '1001 000d dddd 0100',                      LPM_Z,          ('F', 'd') ),   # 0 <= d <= 31
    ( 'LPM\tR{d}, Z+',      '1001 000d dddd 0101',                      LPM_Z_Plus,     ('F', 'd') ),   # 0 <= d <= 31
    ( 'LSR\tR{d}',          '1001 010d dddd 0110',                      LSR,            ('d')      ),   # 0 <= d <= 31
    ( 'MOV\tR{d}, R{r}',    '0010 11rd dddd rrrr',                      MOV,            ('d', 'r') ),   # 0 <= d <= 31,         0 <= r <= 31
    ( 'MOVW\tR{p}, R{P}',   '0000 0001 pppp PPPP',                      MOVW,           ('p', 'P') ),   # p \in {0,2,...,30},   P \in {0,2,...,30}
    ( 'MUL\tR{d}, R{r}',    '1001 11rd dddd rrrr',                      MUL,            ('d', 'r') ),   # 0 <= d <= 31,         0 <= r <= 31
    ( 'MULS\tR{h}, R{H}',   '0000 0010 hhhh HHHH',                      MULS,           ('h', 'H') ),   # 16 <= h <= 31,        16 <= H <= 31
    ( 'MULSU\tR{h}, R{H}',  '0000 0011 0hhh 0HHH',                      MULSU,          ('h', 'H') ),   # 16 <= h <= 23,        16 <= H <= 23
    ( 'NEG\tR{d}',          '1001 010d dddd 0001',                      NEG,            ('d',)     ),   # 0 <= d <= 31
    ( 'NOP',                '0000 0000 0000 0000',                      NOP,            ()         ),
    ( 'OR\tR{d}, R{r}',     '0010 10rd dddd rrrr',                      OR,             ('d', 'r') ),   # 0 <= d <= 31,         0 <= r <= 31
    ( 'ORI\tR{h}, {K}',     '0110 KKKK hhhh KKKK',                      ORI,            ('h', 'K') ),   # 16 <= h <= 31,        0 <= K <= 255
    ( 'OUT\t${A}, R{r}',    '1011 1AAr rrrr AAAA',                      OUT,            ('A', 'r') ),   # 0 <= r <= 31,         0 <= A <= 63
    ( 'POP\tR{d}',          '1001 000d dddd 1111',                      POP,            ('d',)     ),   # 0 <= d <= 31
    ( 'PUSH\tR{r}',         '1001 001r rrrr 1111',                      PUSH,           ('r',)     ),   # 0 <= r <= 31
    ( 'RCALL\t.{k:+}',      '1101 kkkk kkkk kkkk',                      RCALL,          ('k',)     ),   # -2K <= k < 2K
    ( 'RET',                '1001 0101 0000 1000',                      RET,            ()         ),
    ( 'RETI',               '1001 0101 0001 1000',                      RETI,           ()         ),
    ( 'RJMP\t.{k:+}',       '1100 kkkk kkkk kkkk',                      RJMP,           ('k',)     ),   # -2K <= k <= 2K
    ( 'ROR\tR{d}',          '1001 010d dddd 0111',                      ROR,            ('d',)     ),   # 0 <= d <= 31
    ( 'SBC\tR{d}, R{r}',    '0000 10rd dddd rrrr',                      SBC,            ('d', 'r') ),   # 0 <= d <= 31,         0 <= r <= 31
    ( 'SBCI\tR{h}, {K}',    '0100 KKKK hhhh KKKK',                      SBCI,           ('h', 'K') ),   # 16 <= h <= 31,        0 <= K <= 255
    ( 'SBI\t{A}, {b}',      '1001 1010 AAAA Abbb',                      SBI,            ('A', 'b') ),   # 0 <= A <= 31,         0 <= b <= 7
    ( 'SBIC\t{A}, {b}',     '1001 1001 AAAA Abbb',                      SBIC,           ('A', 'b') ),   # 0 <= A <= 31,         0 <= b <= 7
    ( 'SBIS\t{A}, {b}',     '1001 1011 AAAA Abbb',                      SBIS,           ('A', 'b') ),   # 0 <= A <= 31,         0 <= b <= 7
    ( 'SBIW\tR{p}, {K}',    '1001 0111 KKpp KKKK',                      SBIW,           ('p', 'K') ),   # p \in {24,26,28,30},  0 <= K <= 63
    ( 'SBRC\tR{r}, {b}',    '1111 110r rrrr 0bbb',                      SBRC,           ('r', 'b') ),   # 0 <= r <= 31,         0 <= b <= 7
    ( 'SBRS\tR{r}, {b}',    '1111 111r rrrr 0bbb',                      SBRS,           ('r', 'b') ),   # 0 <= r <= 31,         0 <= b <= 7
    ( 'SLEEP',              '1001 0101 1000 1000',                      SLEEP,          ()         ),
    ( 'SPM',                '1001 0101 1110 1000',                      SPM,            ()         ),
    ( 'ST\tX, R{r}',        '1001 001r rrrr 1100',                      ST_X,           ('r',)     ),   # 0 <= r <= 31
    ( 'ST\tX+, R{r}',       '1001 001r rrrr 1101',                      ST_X_Plus,      ('r',)     ),   # 0 <= r <= 31
    ( 'ST\t-X, R{r}',       '1001 001r rrrr 1110',                      ST_Minus_X,     ('r',)     ),   # 0 <= r <= 31
    ( 'ST\tY+, R{r}',       '1001 001r rrrr 1001',                      ST_Y_Plus,      ('r',)     ),   # 0 <= r <= 31
    ( 'ST\t-Y, R{r}',       '1001 001r rrrr 1010',                      ST_Minus_Y,     ('r',)     ),   # 0 <= r <= 31
    ( 'STD\tY+{q}, R{r}',   '10q0 qq1r rrrr 1qqq',                      STD_Y_q,        ('r', 'q') ),   # 0 <= r <= 31,         0 <= q <= 63
    ( 'ST\tZ+, R{r}',       '1001 001r rrrr 0001',                      ST_Z_Plus,      ('r',)     ),   # 0 <= r <= 31
    ( 'ST\t-Z, R{r}',       '1001 001r rrrr 0010',                      ST_Minus_Z,     ('r',)     ),   # 0 <= r <= 31
    ( 'STD\tZ+{q}, R{r}',   '10q0 qq1r rrrr 0qqq',                      STD_Z_q,        ('r', 'q') ),   # 0 <= r <= 31          0 <= q <= 63
    ( 'STS\t{K}, R{r}',     '1001 001r rrrr 0000 KKKK KKKK KKKK KKKK', STS,             ('r', 'K') ),   # 0 <= r <= 31, 0 <= K <= 65535
    ( 'SUB\tR{d}, R{r}',    '0001 10rd dddd rrrr', SUB,                                 ('d', 'r') ),   # 0 <= d <= 31,         0 <= r <= 31
    ( 'SUBI\tR{h}, {K}',    '0101 KKKK hhhh KKKK', SUBI,                                ('h', 'K') ),   # 16 <= h <= 31,        0 <= K <= 255
    ( 'SWAP\tR{d}',         '1001 010d dddd 0010', SWAP,                                ('d',)     ),   # 0 <= d <= 31
    ( 'WDR',                '1001 0101 1010 1000', WDR,                                 ()         ),
]



def GetOperand(opc_str, oprd_chr, word):
    if 'K' == oprd_chr:
        k, num_bits = AVR_disassemble.MkAbsoluteOperand('K', opc_str, word)
        return k

    if 'k' == oprd_chr:
        k, num_bits = AVR_disassemble.MkAbsoluteOperand('k', opc_str, word)
        rel_k = AVR_disassemble.GetRelative7bit(k) if num_bits == 7 else AVR_disassemble.GetRelative12bit(k)
        return rel_k

    if 'A' == oprd_chr:
        a, num_bits = AVR_disassemble.MkAbsoluteOperand('A', opc_str, word)
        return a

    if oprd_chr in AVR_disassemble.ABS_OPRDS:
        idx = AVR_disassemble.ABS_OPRDS.index(oprd_chr)
        oprd_chr = AVR_disassemble.ABS_OPRDS[idx]
        v, num_bits = AVR_disassemble.MkAbsoluteOperand(oprd_chr, opc_str, word)
        return v

    if oprd_chr in [ 'p', 'P' ]:
        oprd_chr = oprd_chr if 'p' in oprd_chr else 'P'
        p, num_bits = AVR_disassemble.MkAbsoluteOperand(oprd_chr, opc_str, word)
        p = p * 2 + ((num_bits == 2) * 24)
        return p

    if oprd_chr in [ 'h', 'H' ]:
        oprd_chr = 'h' if 'h' in oprd_chr else 'H'
        h, num_bits = AVR_disassemble.MkAbsoluteOperand(oprd_chr, opc_str, word)
        h += 16
        return h

    return None


def Disassemble(instr_rec, word):
    disasm  = instr_rec[0]
    oprds   = instr_rec[3]
    if len(oprds) == 0:
        return disasm

    opr_str = instr_rec[1].replace(' ', '')
    if len(oprds) == 1:
        if oprds[0] == 'F':
            return disasm

        v = GetOperand(opr_str, oprds[0], word)
        if oprds[0] == 'K':
            return disasm.format(K=v)
        if oprds[0] == 'k':
            return disasm.format(k=v)
        if oprds[0] == 's':
            return disasm.format(s=v)
        if oprds[0] == 'd':
            return disasm.format(d=v)
        if oprds[0] == 'r':
            return disasm.format(r=v)
        raise Exception('Could not find signle operand!')

    if len(oprds) == 2:
        if oprds == ('F', 'd'):
            v = GetOperand(opr_str, oprds[1], word)
            return disasm.format(d=v)

        v1 = GetOperand(opr_str, oprds[0], word)
        v2 = GetOperand(opr_str, oprds[1], word)
        if oprds == ('A', 'r'):
            return disasm.format(A=v1, r=v2)
        if oprds == ('A', 'd'):
            return disasm.format(A=v1, d=v2)
        if oprds == ('A', 'b'):
            return disasm.format(A=v1, b=v2)
        if oprds == ('d', 'r'):
            return disasm.format(d=v1, r=v2)
        if oprds == ('d', 'q'):
            return disasm.format(d=v1, q=v2)
        if oprds == ('r', 'q'):
            return disasm.format(r=v1, q=v2)
        if oprds == ('d', 'b'):
            return disasm.format(d=v1, b=v2)
        if oprds == ('h', 'K'):
            return disasm.format(h=v1, K=v2)
        if oprds == ('p', 'K'):
            return disasm.format(p=v1, K=v2)
        if oprds == ('r', 'K'):
            return disasm.format(r=v1, K=v2)
        if oprds == ('h', 'H'):
            return disasm.format(h=v1, H=v2)
        if oprds == ('p', 'P'):
            return disasm.format(p=v1, P=v2)
        if oprds == ('s', 'k'):
            return disasm.format(s=v1, k=v2)
        raise Exception('Could not find double operands!\n  0x{:04x}\n  {}'.format(word, instr_rec))

    raise Exception('Could recognize more than two operands!')



class AVR8BitCPU:
    def __init__(self, RAM_size, is_PC_16_bits=True):
        self.regs = [ 0 for i in range(32) ]
        self.cycles = 0
        self.SREG = 0
        self.PC = 0
        self.SP = 0
        self.RAM = [ 0 for i in range(RAM_size) ]
        self.IO = [ 0 for i in range(64) ]
        self.is_PC_16_bits = is_PC_16_bits

        self.is_next_skip = False           # TODO: Implement in execute function.
        self.is_sleep = False               # TODO: Implement sleep functionality.

        self.is_print_asm = IS_PRINT_ASM
        self.ret_addrs = []

        self.hex_fmt = None
        self.decoded_flash = []


    def GetX(self):
        x = (self.regs[27] << 8) | self.regs[26]
        return x


    def SetX(self, val):
        self.regs[26] = val & 0xff
        self.regs[27] = (val >> 8) & 0xff


    def GetY(self):
        y = (self.regs[29] << 8) | self.regs[28]
        return y


    def SetY(self, val):
        self.regs[28] = val & 0xff
        self.regs[29] = (val >> 8) & 0xff


    def GetZ(self):
        z = (self.regs[31] << 8) | self.regs[30]
        return z


    def SetZ(self, val):
        self.regs[30] = val & 0xff
        self.regs[31] = (val >> 8) & 0xff


    def GetSREGStrCompact(self):
        SREG_FLAGS = 'ITHSVNZC'
        sreg_str = ''.join([ SREG_FLAGS[b] if GetSREG(self, 7 - b) else '-' for b in range(8) ])
        return sreg_str


    def GetSREGStr(self):
        sreg_str = ''
        sreg_str +=  'I:{}'.format('1' if self.SREG & 0x80 else '0')
        sreg_str += ' T:{}'.format('1' if self.SREG & 0x40 else '0')
        sreg_str += ' H:{}'.format('1' if self.SREG & 0x20 else '0')
        sreg_str += ' S:{}'.format('1' if self.SREG & 0x10 else '0')
        sreg_str += ' V:{}'.format('1' if self.SREG & 0x08 else '0')
        sreg_str += ' N:{}'.format('1' if self.SREG & 0x04 else '0')
        sreg_str += ' Z:{}'.format('1' if self.SREG & 0x02 else '0')
        sreg_str += ' C:{}'.format('1' if self.SREG & 0x01 else '0')
        return sreg_str


    def ReadIO(self, addr):
        # TODO: Call registered hook function!
        IO_name = ATmega8_regs.IO_NAMES[addr]

        if IS_LOG_READ_IO:
            print('********** READ IO  %s  A:%02x' % (IO_name, addr))
        return self.IO[addr]


    def ReadIOBit(self, addr, b):
        # TODO: Call registered hook function!
        IO_name = ATmega8_regs.IO_NAMES[addr]

        if IS_LOG_READ_IO:
            print('********** READ IO BIT  %s  A:%02x  b:%d' % (IO_name, addr, b))
        return ((self.IO[addr] & (1 << b)) == (1 << b))


    def WriteIO(self, addr, val):
        IO_name = ATmega8_regs.IO_NAMES[addr]
        if IS_LOG_WRITE_IO:
            print('********** WRITE IO   %s  A:%02x  V:%02x' % (IO_name, addr, val))
        if IO_name == 'SPH':
            self.SP = (val << 8) | (self.SP & 0xff)
        if IO_name == 'SPL':
            self.SP = (self.SP & 0xff00) | val
        if IO_name == 'SREG':
            self.SREG = val

        # TODO: Call registered hook function!
        global PortD_Data, OldPortD_Data, frame_num
        if IO_name == 'PORTD':
            data_str = ''.join(['*' if (val & (0x80 >> i)) else ' ' for i in range(8)])
            PortD_Data.append(data_str)
        if IO_name == 'PORTB':
            prev_val = self.IO[addr]
            if (prev_val == 0x7f) and (val == 0xff):
                frame_num += 1
                frame_data = PortD_Data[-8:]
                if not OldPortD_Data == frame_data:
                    if not os.path.isdir('Frames'):
                        os.makedirs('Frames')
                    out_path = os.path.join('Frames', 'device-%07d.jpg' % frame_num)
                    draw_util.DrawDevice(frame_data, '-----', out_path)
                    PortD_Data = []
                    OldPortD_Data = frame_data
        self.IO[addr] = val


    def WriteIO_ClearBit(self, addr, b):
        # TODO: Call registered hook function!
        IO_name = ATmega8_regs.IO_NAMES[addr]
        if IS_LOG_WRITE_IO:
            print('********** WRITE IO CLR BIT  %s  A:%02x   V:%d' % (IO_name, addr, b))
        self.IO[addr] &= ~(1 << b)


    def WriteIO_SetBit(self, addr, b):
        # TODO: Call registered hook function!
        IO_name = ATmega8_regs.IO_NAMES[addr]
        if IS_LOG_WRITE_IO:
            print('********** WRITE IO SET BIT  %s  %02x   %d' % (IO_name, addr, b))
        self.IO[addr] != (1 << b)


    def WriteSP(self, val):
        val = val & SP_MASK
        self.SP = val
        self.IO[ATmega8_regs.IO_NAMES.index('SPL')] = val & 0xff
        self.IO[ATmega8_regs.IO_NAMES.index('SPH')] = (val >> 8) & 0xff


    def ReadRAM(self, addr):
        if addr < 32:
            return self.regs[addr]

        if addr < (32 + 64):
            return self.ReadIO(addr - 32)

        ram_addr = (addr - 32 - 64) & (len(self.RAM) - 1)
        return self.RAM[ram_addr]


    def WriteRAM(self, addr, val):
        if addr < 32:
            self.regs[addr] = val
        elif addr < (32 + 64):
            self.WriteIO(addr - 32, val)
        elif addr < (32 + 64 + len(self.RAM)):
            ram_addr = (addr - 32 - 64) & (len(self.RAM) - 1)
            self.RAM[ram_addr] = val
            if IS_LOG_WRITE_RAM:
                print(('WriteRAM    0x%04x <- `' % addr) + ''.join(['*' if val & (0x80 >> b) else ' ' for b in range(8)]) + '\'')


    def FindInstructionRecord(self, hex_fmt, PC):
        hex_word = AVR_disassemble.Get16ByteOpcSafe(hex_fmt, PC)
        if hex_word == None:
            return None, None

        for inst_rec in INSTRUCTIONS:
            opc, opc_mask, oprd_set, oprd_masks = AVR_disassemble.GetMasks(inst_rec)
            word = hex_word
            num_words = 1
            if opc_mask > 0xffff:
                word_2 = AVR_disassemble.Get16ByteOpcSafe(hex_fmt, PC + 2)
                if word_2 == None:
                    continue

                num_words = 2
                word = (word << 16) | word_2
            if (word & opc_mask) == opc:
                return inst_rec, word

        return None, hex_word


    def DecodeFlash(self, hex_fmt):
        self.hex_fmt = hex_fmt
        num_words = self.hex_fmt.GetNumBytes() // 2
        for i in range(num_words):
            instr_rec, hex_word = self.FindInstructionRecord(self.hex_fmt, i * 2)
            if instr_rec:
                oprd_str = instr_rec[1].replace(' ', '')
                instr_args = [ GetOperand(oprd_str, oprd_chr, hex_word) for oprd_chr in instr_rec[3] ]
                instr_idx = INSTRUCTIONS.index(instr_rec)
                self.decoded_flash.append((instr_idx, instr_args, hex_word))
            else:
                self.decoded_flash.append((-1, None, hex_word))


    def Exec(self):
        pc_idx = self.PC // 2
        (instr_idx, instr_args, word) = self.decoded_flash[pc_idx]
        if instr_idx == -1:
            raise Exception('Unknown instruction!\n  PC: 0x{:04x}\n   W: 0x{:04x}'.format(self.PC, word))

        instr_rec = INSTRUCTIONS[instr_idx]
        if self.is_print_asm:
            print('{:>7x}  {}'.format(self.PC, Disassemble(instr_rec, word)))
        if self.is_next_skip:
            raise RuntimeError('Skip Next in the start of Exec()!')

        func    = instr_rec[2]
        oprds   = instr_rec[3]
        if 'F' in oprds:
            if len(oprds) == 1:
                func(self, self.hex_fmt)
            else:
                func(self, self.hex_fmt, instr_args[1])
            return

        if len(oprds) == 0:
            func(self)
        elif len(oprds) == 1:
            func(self, instr_args[0])
        elif len(oprds) == 2:
            func(self, instr_args[0], instr_args[1])

        # Skip next instruction.
        if self.is_next_skip:
            self.is_next_skip = False
            (nxt_instr_idx, nxt_instr_args, nxt_word) = self.decoded_flash[pc_idx + 1]
            if nxt_instr_idx == -1:
                raise RuntimeError('Coud not jump from unknown instruction!')

            nxt_instr = INSTRUCTIONS[nxt_instr_idx]
            nxt_str = nxt_instr[1].replace(' ', '')
            num_words = len(nxt_str) // 16
            IncPC(self, 2 + (2 * (num_words == 2)))
            IncCycles(self, 1 + (num_words == 2))


    def Print(self):
        # Print cycles.
        s = 'Cycles   {}\n'.format(self.cycles)
        s += '\n'

        # Print working registers.
        str_fmt = 'R{:<2d} 0x{:02x}          R{:<2d} 0x{:02x}\n'
        num_regs = len(self.regs) / 2
        for i in range(num_regs):
            s += str_fmt.format(i, self.regs[i], (i + num_regs), self.regs[i + num_regs])
        s += '\n'

        s += 'X 0x{:04x} {:02x} {:02x}\n'.format(self.GetX(), self.regs[26], self.regs[27])
        s += 'Y 0x{:04x} {:02x} {:02x}\n'.format(self.GetY(), self.regs[28], self.regs[29])
        s += 'Z 0x{:04x} {:02x} {:02x}\n'.format(self.GetZ(), self.regs[30], self.regs[31])
        s += '\n'

        # Print program status.
        sreg_str = self.GetSREGStrCompact()
        s += 'SREG     0x{:02x}   ({})\n'.format(self.SREG, sreg_str)
        s += 'PC       0x{:04x}\n'.format(self.PC)
        s += 'SP       0x{:04x}\n'.format(self.SP)
        s += '\n'

        # Print IO.
        s += 'IO:\n'
        i = 0
        while i < len(self.IO):
            s += ''.join(['{} {:02x}'.format('   ' if j == 8 else '', self.IO[i + j]) for j in range(16)])
            s += '\n'
            i += 16
        s += '\n'

        # Print RAM.
        s += 'RAM:\n'
        i = 0
        while i < len(self.RAM):
            s += ''.join(['{} {:02x}'.format('   ' if j == 8 else '', self.RAM[i + j]) for j in range(16)])
            s += '\n'
            i += 16
        return s

