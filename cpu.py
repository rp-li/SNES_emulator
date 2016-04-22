import numpy as np
import binascii
import sys

class cpu:
    def __init__(self, speed):
        self.speed=speed
        self.cycles=0
        #CPU REGISTERS
        self.reg_A='0000000000000000'  #accumulator
        self.reg_X='0000000000000000'  #index
        self.reg_Y='0000000000000000'  #index
        self.reg_S='0000000000000000'  #stack pointer
        self.reg_DB='00000000'   #data bank
        self.reg_D='0000000000000000'     #direct page
        self.reg_PB='00000000'     #program bank
        self.reg_P='00000000'     #processor status flags
        self.reg_PC='0000000000000000'   #program counter (memory address)

    #P REGISTER FLAGS
    #N='10000000'
    #V='01000000'
    #Z='00000010'
    #C='00000001'
    #D='00001000'
    #I='00000100'
    #X='00010000'
    #M='00100000'
    #E='00000000'
    #B='00010000'

    #ADDRESSING MODES

    #'imp': Implied
    #'immemflag': ImmediateMemoryFlag
    #'imindexflag': ImmediateIndexFlag
    #'im8bit': Immediate8-Bit
    #'rel': Relative
    #'rellong': Relative long
    #'d': Direct
    #'dix': Direct indexed (with X)
    #'diy': Direct indexed (with Y)
    #'di': Direct indirect
    #'dindxi': Direct indexed indirect
    #'diindx': Direct indirect indexed
    #'dil': Direct indirect long
    #'diindxl': Direct indirect indexed long
    #'abs': Absolute
    #'absindxx': Absolute indexed (with X)
    #'absindxy': Absolute indexed (with Y)
    #'absl': Absolute long
    #'absindl': Absolute indexed long
    #'sr': Stack relative
    #'sriindx': Stack relative indirect indexed
    #'absi': Absolute indirect
    #'absil': Absolute indirect long
    #'absindi': Absolute indexed indirect
    #'impacc': Implied accumulator
    #'bm': Block move

    #OPCODES
    def ADC(self, addr_mode, ):
        if addr_mode==1:
            return
        self.temp=list(self.reg_P)
        self.temp[0]='1'
        self.temp[1]='1'
        self.temp[6]='1'
        self.temp[7]='1'
        self.reg_P="".join(self.temp)

    def AND(self, addr_mode, ):
        return

    def ASL(self, addr_mode, ):
        return

    def BCC(self, addr_mode, ):
        return

    def BCS(self, addr_mode, ):
        return

    def BEQ(addr_mode, ):
        return

    def BIT(addr_mode, ):
        return

    def BMI(addr_mode, ):
        return

    def BNE(addr_mode, ):
        return

    def BPL(addr_mode, ):
        return

    def BRA(addr_mode, ):
        return

    def BRK(addr_mode, ):
        return

    def BRL(addr_mode, ):
        return

    def BVC(addr_mode, ):
        return

    def BVS(addr_mode, ):
        return

    def CLC(addr_mode, ):
        return

    def CLD(addr_mode, ):
        return

    def CLI(addr_mode, ):
        return

    def CLV(addr_mode, ):
        return

    def CMP(addr_mode, ):
        return

    def COP(addr_mode, ):
        return

    def CPX(addr_mode, ):
        return

    def CPY(addr_mode, ):
        return

    def DEC(addr_mode, ):
        return

    def DEX(addr_mode, ):
        return

    def DEY(addr_mode, ):
        return

    def EOR(addr_mode, ):
        return

    def INC(addr_mode, ):
        return

    def INX(addr_mode, ):
        return

    def INY(addr_mode, ):
        return

    def JML(addr_mode, ):
        return

    def JMP(addr_mode, ):
        return

    def JSL(addr_mode, ):
        return

    def JSR(addr_mode, ):
        return

    def LDA(addr_mode, ):
        return

    def LDX(addr_mode, ):
        return

    def LDY(addr_mode, ):
        return

    def LSR(addr_mode, ):
        return

    def MVN(addr_mode, ):
        return

    def MVP(addr_mode, ):
        return

    def NOP(addr_mode, ):
        return

    def ORA(addr_mode, ):
        return

    def PEA(addr_mode, ):
        return

    def PEI(addr_mode, ):
        return

    def PER(addr_mode, ):
        return

    def PHA(addr_mode, ):
        return

    def PHB(addr_mode, ):
        return

    def PHD(addr_mode, ):
        return

    def PHK(addr_mode, ):
        return

    def PHP(addr_mode, ):
        return

    def PHX(addr_mode, ):
        return

    def PHY(addr_mode, ):
        return

    def PLA(addr_mode, ):
        return

    def PLB(addr_mode, ):
        return

    def PLD(addr_mode, ):
        return

    def PLP(addr_mode, ):
        return

    def PLX(addr_mode, ):
        return

    def PLY(addr_mode, ):
        return

    def REP(addr_mode, ):
        return

    def ROL(addr_mode, ):
        return

    def ROR(addr_mode, ):
        return

    def RTI(addr_mode, ):
        return

    def RTL(addr_mode, ):
        return

    def RTS(addr_mode, ):
        return

    def SBC(addr_mode, ):
        return

    def SEP(addr_mode, ):
        return

    def SEC(addr_mode, ):
        return

    def SED(addr_mode, ):
        return

    def SEI(addr_mode, ):
        return

    def STA(addr_mode, ):
        return

    def STP(addr_mode, ):
        return

    def STX(addr_mode, ):
        return

    def STY(addr_mode, ):
        return

    def STZ(addr_mode, ):
        return

    def TAX(addr_mode, ):
        return

    def TAY(addr_mode, ):
        return

    def TCD(addr_mode, ):
        return

    def TCS(addr_mode, ):
        return

    def TDC(addr_mode, ):
        return

    def TRB(addr_mode, ):
        return

    def TSB(addr_mode, ):
        return

    def TSC(addr_mode, ):
        return

    def TSX(addr_mode, ):
        return

    def TXA(addr_mode, ):
        return

    def TXS(addr_mode, ):
        return

    def TXY(addr_mode, ):
        return

    def TYA(addr_mode, ):
        return

    def TYX(addr_mode, ):
        return

    def WAI(addr_mode, ):
        return

    def WDM(addr_mode, ):
        return

    def XBA(addr_mode, ):
        return

    def XCE(addr_mode, ):
        return

cpu
