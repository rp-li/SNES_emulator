import numpy as np
import binascii
import sys
import threading
import time
from opcodes import *

ROMPATH="../SMW_rom.sfc"
#ROMPATH="../test.txt"
CPUMAXCYCLES=999999

class cpu:
    def __init__(self):
        self.opcodes=opcodes()
        self.debug=0
        self.vdebug=0
        self.speed=123
        self.emulationmode=1
        self.cycles=0
        self.isrunning=0
        #CPU REGISTERS
        self.reg_A='0000'  #accumulator(hex)
        self.reg_X='0000'  #index(hex)
        self.reg_Y='0000'  #index(hex)
        self.reg_S='0000'  #stack pointer(hex)
        self.reg_DB='00'   #data bank(hex)
        self.reg_D='0000'     #direct page(hex)
        self.reg_PB='00'     #program bank(hex)
        self.reg_P='00000000'     #processor status flags (binary)
        self.reg_PC='0000'   #program counter (memory address)
        print 'CPU Initialized'

    def increment_PC(self, counter):
        self.reg_PC=str(hex(dec(cpu.reg_PC)+counter)[2:]) #incrementing the program counter
        while len(self.reg_PC)<4:
            self.reg_PC='0'+self.reg_PC
        
    def start(self, reset=0):
        if reset==1:
            self.reg_PC=rom.reset_vector
            self.reg_S=mem.stackloc
            self.isrunning=1
        t=time.time()
        while self.isrunning==1:
            if self.debug==1:
                print time.time(), '0x'+cpu.reg_PC,
            self.run(mem.read(self.reg_PB,self.reg_PC,self.reg_PC))
            if self.cycles>=CPUMAXCYCLES:
                self.isrunning=0
            if self.vdebug==1:
                self.show()
        if self.vdebug==0:
            print cpu.cycles, 'CPU cycles completed in ', time.time()-t

    def show(self):
        print ''
        print '6502 emulation mode:', self.emulationmode
        print 'Accumulator register: ', self.reg_A
        print 'X index register: ', self.reg_X
        print 'Y index register: ', self.reg_Y
        print 'Stack Pointer register: ', self.reg_S
        print 'Data bank register: ', self.reg_DB
        print 'Direct Page register: ', self.reg_D
        print 'Program Bank register: ', self.reg_PB
        print 'Processor Flag register: ', self.reg_P
        print 'Program Counter register: ', self.reg_PC
        
    def run(self, bytecode=''):
        if bytecode=='':
            self.isrunning=1
            cpu.start()
        else:
            if bytecode in self.opcodes.dict:
                self.opcodes.dict[bytecode](self, mem)                        
            else:
                cpu.isrunning=0
                #print 'CPU halted: unknown opcode', bytecode
        
    def setflag(self, flag, clear=0):
        if 'N' in flag:
            temp=list(self.reg_P)
            temp[0]=str(int(not(clear)))
            self.reg_P="".join(temp)
            if self.debug==1 and clear==0:
                print 'N flag set'
        if 'V' in flag:
            temp=list(self.reg_P)
            temp[1]=str(int(not(clear)))
            self.reg_P="".join(temp)
        if 'Z' in flag:
            temp=list(self.reg_P)
            temp[6]=str(int(not(clear)))
            self.reg_P="".join(temp)
        if 'C' in flag:
            temp=list(self.reg_P)
            temp[7]=str(int(not(clear)))
            self.reg_P="".join(temp)
        if 'D' in flag:
            temp=list(self.reg_P)
            temp[4]=str(int(not(clear)))
            self.reg_P="".join(temp)
        if 'I' in flag:
            temp=list(self.reg_P)
            temp[5]=str(int(not(clear)))
            self.reg_P="".join(temp)
        if 'X' in flag:
            temp=list(self.reg_P)
            temp[3]=str(int(not(clear)))
            self.reg_P="".join(temp)
        if 'M' in flag:
            temp=list(self.reg_P)
            temp[2]=str(int(not(clear)))
            self.reg_P="".join(temp)
        if 'E' in flag:
            temp=list(self.reg_P)
            #6502 emulation mode
            temp[7]=str(int(not(clear)))
            self.reg_P="".join(temp)
        if 'B' in flag:
            #emulation mode only
            temp=list(self.reg_P)
            temp[3]=str(int(not(clear)))
            self.reg_P="".join(temp)

class mem:
    def __init__(self):
        self.stackloc='0100'
        #00 to FF memory banks
        print 'Building SNES memory map...'
        self.mem=[]
        for i in range(256):
            self.mem.append([])
            for j in range(65536):
                self.mem[i].append('00')
        if rom.mode=='hiROM':
            for b in range(dec('c0'),dec('ff')):
                self.write(b,'0000',rom.read(65536*(b-192),65536*(b-192)+dec('ffff')))                                             
            for b in range(dec('00'),dec('1f')):
                self.write(b,'8000',self.read(b+dec('c0'),'0000','7fff'))
                           
        elif rom.mode=='loROM':
            pass

    def read(self, bank, addr_start, addr_end):
        out=''
        for i in range(dec(addr_start),dec(addr_end)+1):
            out=out+str(self.mem[dec(bank)][i])
        return out
        
    def write(self, bank, addr, val):
        addr=dec(addr)
        if type(bank)==int:
            for i in range(len(val)/2):
                self.mem[bank][addr]=val[2*i:2*i+2]
                addr+=1
        elif type(bank)==str:
            
            for i in range(len(val)/2):
                self.mem[dec(bank)][addr]=val[2*i:2*i+2]
                addr+=1

class rom:
    def __init__(self): 
        with open(ROMPATH, 'rb') as r:
            content=r.read()
        self.buffer=binascii.hexlify(content)
        self.header=self.read('000015', '000015')
        if self.header=='20':
            rom.mode='loROM'
        elif self.header=='21':
            rom.mode='hiROM'
            self.title=self.read('7FC0','7FD0').decode('hex')
        self.reset_vector=self.read('7FFD','7FFD')+self.read('7FFC','7FFC')
        

    def read(self, start_addr, end_addr):
        if type(start_addr)==str and type(end_addr)==str:
            if len(self.buffer)<=2*dec(start_addr):
                return '00'
            return self.buffer[2*(int(start_addr, 16)):2*(int(end_addr, 16))+2]
        elif type(start_addr)==int and type(end_addr)==int:
            if len(self.buffer)<=2*start_addr:
                return '00'
            return self.buffer[2*start_addr:2*end_addr+2]
        
rom=rom()
cpu=cpu()
mem=mem()

#boot sequence
print 'SNES started'
cpu.start(reset=1)
