def dec(addr):
    if type(addr)==int:
        return addr
    elif type(addr)==str:
        return int(addr,16)

class opcodes: 
    def __init__(self):
        self.dict={}
        #self.dict['00']=self.BRK
        self.dict['78']=self.SEI
        self.dict['9c']=self.STZ_addr
        self.dict['a9']=self.LDA_const

    #def BRK(self,cpu, mem):
        #should have emulation mode for 6502
     #   cpu.tick()
     #   cpu.reg_PC=cpu.reg_S
        
    def SEI(self,cpu, mem):
        if cpu.debug==1:
            print cpu.cycles,'SEI'
        cpu.tick()
        cpu.setflag('I')
    
    def STZ_addr(self,cpu, mem):
        if cpu.debug==1:
            print cpu.cycles, 
        cpu.tick()
        cpu.reg_S=cpu.reg_S[0:2]+mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC))[2:],hex(dec(cpu.reg_PC))[2:])
        cpu.tick()
        cpu.reg_S=mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC))[2:],hex(dec(cpu.reg_PC))[2:])+cpu.reg_S[2:4]
        if cpu.debug==1:
            print 'STZ(absolute) at ', cpu.reg_PB, cpu.reg_S
        cpu.tick()
        mem.write(cpu.reg_PB, cpu.reg_S, '00')

    def LDA_const(self,cpu, mem):
        if cpu.debug==1:
            print cpu.cycles,
        if cpu.reg_P[2]=='1':
            cpu.tick()
            cpu.reg_A=cpu.reg_A[0:2]+mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC))[2:],hex(dec(cpu.reg_PC))[2:])
        elif cpu.reg_P[2]=='0':
            cpu.tick()
            cpu.reg_A=cpu.reg_A[0:2]+mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC))[2:],hex(dec(cpu.reg_PC))[2:])
            cpu.tick()
            cpu.reg_A=mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC))[2:],hex(dec(cpu.reg_PC))[2:])+cpu.reg_A[2:4]
        cpu.tick()
        cpu.setflag('MNZ')
        if cpu.debug==1:
            print 'LDA(immediate)'

            
