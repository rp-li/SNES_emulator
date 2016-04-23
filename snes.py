import numpy as np
import binascii
import sys

ROMPATH="../SMW_rom.sfc"
#ROMPATH="../test.txt"

class cpu:
    def __init__(self, speed):
        self.debug=1
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

    def debug(self):
        print 'Accumulator register: ', self.reg_A
        print 'X index register: ', self.reg_A
        print 'Y index register: ', self.reg_A
        print 'Stack Pointer register: ', self.reg_A
        print 'Data Bank register: ', self.reg_A
        print 'Direct Page register: ', self.reg_A
        print 'Program Bank register: ', self.reg_A
        print 'Processor Flag register: ', self.reg_A
        print 'Program counter register: ', self.reg_A

    def readrom(self, addr):
        self.romaddr=2*addr
        return rom.buffer[self.romaddr:self.romaddr+2]
        
    def run(self, bytecode):
        if bytecode=='78':
            if self.debug==1:
                print 'SEI'
            self.setflag('I')
            
        elif bytecode=='9C':
            if self.debug==1:
                print 'STZ(absolute)'
            arg=cpu.readrom(self.romaddr+1)+cpu.readrom(self.romaddr+2)
            mem.write(arg, '00')

    def setflag(self,flag):
        if 'N' in flag:
            temp=list(self.reg_P)
            temp[0]='1'
            self.reg_P="".join(temp)
        if 'V' in flag:
            temp=list(self.reg_P)
            temp[1]='1'
            self.reg_P="".join(temp)
        if 'Z' in flag:
            temp=list(self.reg_P)
            temp[6]='1'
            self.reg_P="".join(temp)
        if 'C' in flag:
            temp=list(self.reg_P)
            temp[7]='1'
            self.reg_P="".join(temp)
        if 'D' in flag:
            temp=list(self.reg_P)
            temp[4]='1'
            self.reg_P="".join(temp)
        if 'I' in flag:
            temp=list(self.reg_P)
            temp[5]='1'
            self.reg_P="".join(temp)
        if 'X' in flag:
            temp=list(self.reg_P)
            temp[3]='1'
            self.reg_P="".join(temp)
        if 'M' in flag:
            temp=list(self.reg_P)
            temp[2]='1'
            self.reg_P="".join(temp)
        if 'E' in flag:
            temp=list(self.reg_P)
            #6502 emulation mode
            self.reg_P="".join(temp)
        if 'B' in flag:
            #emulation mode only
            temp=list(self.reg_P)
            temp[3]='1'
            self.reg_P="".join(temp)

class mem:
    def __init__(self):
        self.mem={}
    def write(self, addr, val):
        if type(addr)==str and type(val)==str:
            self.mem[addr]=str(val)
    def read(self, addr):
        if type(addr)==str:
            if not addr in self.mem:
                return '00'
            return self.mem[addr]

class rom:
    def __init__(self):
        with open(ROMPATH, 'rb') as r:
            content=r.read()
        self.buffer=binascii.hexlify(content)
        self.buffer=self.buffer.upper()
        
rom=rom()
cpu=cpu(3580000)
mem=mem()
