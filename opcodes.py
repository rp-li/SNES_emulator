def dec(addr):
    if type(addr)==int:
        return addr
    elif type(addr)==str:
        return int(addr,16)

class opcodes:
    def __init__(self):
        self.dict={}
        self.dict['00']=self.BRK
        self.dict['78']=self.SEI
        self.dict['9c']=self.STZ_addr
        self.dict['a9']=self.LDA_const
        self.dict['40']=self.RTI
        self.dict['18']=self.CLC
        self.dict['fb']=self.XCE
        self.dict['c2']=self.REP
        self.dict['5b']=self.TCD
        self.dict['01']=self.ORA_dp_X_indirect
        self.dict['1b']=self.TCS
        self.dict['8f']=self.STA_long
        self.dict['a2']=self.LDX_const
        self.dict['a0']=self.LDY_const
        
    def stackpush(self, cpu, mem, val):
        mem.write('00', cpu.reg_S, val) #stack push
        if cpu.debug==1:
            print val, 'pushed to ', cpu.reg_S
        cpu.reg_S=str(hex(dec(cpu.reg_S)-1)[2:])
        while len(cpu.reg_S)<4:
            cpu.reg_S='0'+cpu.reg_S

    def stackpull(self, cpu, mem):
        cpu.reg_S=str(hex(dec(cpu.reg_S)+1)[2:])
        val=mem.read('00', cpu.reg_S, cpu.reg_S)
        while len(cpu.reg_S)<4:
            cpu.reg_S='0'+cpu.reg_S
        if cpu.debug==1:
            print val, 'pulled from ', cpu.reg_S
        return val

    def LDX_const(self,cpu,mem):
        cpu.cycles+=2
        if cpu.debug==1:
            print cpu.cycles, 'LDX(immediate)'
        if cpu.reg_P[2]=='1':
            temp=mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC)+1)[2:],hex(dec(cpu.reg_PC)+1)[2:])
            cpu.reg_X=cpu.reg_X[0:2]+temp
            cpu.increment_PC(2)
        elif cpu.reg_P[2]=='0':
            temp=mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC)+2)[2:],hex(dec(cpu.reg_PC)+2)[2:])+mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC)+1)[2:],hex(dec(cpu.reg_PC)+1)[2:])
            cpu.reg_X=mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC)+2)[2:],hex(dec(cpu.reg_PC)+2)[2:])+mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC)+1)[2:],hex(dec(cpu.reg_PC)+1)[2:])
            cpu.increment_PC(3)
        if dec(temp)==0:
            cpu.setflag('Z')
        elif bin(dec(temp))[2]==1:
            cpu.setflag('N')

    def LDY_const(self,cpu,mem):
        cpu.cycles+=2
        if cpu.debug==1:
            print cpu.cycles, 'LDY(immediate)'
        if cpu.reg_P[2]=='1':
            temp=mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC)+1)[2:],hex(dec(cpu.reg_PC)+1)[2:])
            cpu.reg_Y=cpu.reg_Y[0:2]+temp
            cpu.increment_PC(2)
        elif cpu.reg_P[2]=='0':
            temp=mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC)+2)[2:],hex(dec(cpu.reg_PC)+2)[2:])+mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC)+1)[2:],hex(dec(cpu.reg_PC)+1)[2:])
            cpu.reg_Y=mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC)+2)[2:],hex(dec(cpu.reg_PC)+2)[2:])+mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC)+1)[2:],hex(dec(cpu.reg_PC)+1)[2:])
            cpu.increment_PC(3)
        if dec(temp)==0:
            cpu.setflag('Z')
        elif bin(dec(temp))[2]==1:
            cpu.setflag('N')

    def STA_long(self,cpu,mem):
        cpu.cycles+=5
        if cpu.reg_P[2]=='0':
            cpu.cycles+=1
        if cpu.debug==1:
            print cpu.cycles, 'STA(abs,long)'
        temp_pb=mem.read(cpu.reg_PB, str(hex(dec(cpu.reg_PC)+3))[2:],str(hex(dec(cpu.reg_PC)+3)[2:]))
        mem.write(temp_pb, mem.read(cpu.reg_PB, str(hex(dec(cpu.reg_PC)+2))[2:],str(hex(dec(cpu.reg_PC)+2)[2:]))+mem.read(cpu.reg_PB, str(hex(dec(cpu.reg_PC)+1))[2:],str(hex(dec(cpu.reg_PC)+1)[2:])), cpu.reg_A)
        cpu.increment_PC(4)

    def TCS(self,cpu,mem):
        cpu.cycles+=2
        if cpu.debug==1:
            print cpu.cycles, 'TCS'
        cpu.reg_S=cpu.reg_A
        cpu.increment_PC(1)

    def ORA_dp_X_indirect(self,cpu,mem):
        cpu.cycles+=6
        if cpu.debug==1:
            print cpu.cycles, 'ORA(dp,X,indir)'
        temp=mem.read(cpu.reg_PB, str(hex(dec(cpu.reg_PC)+2))[2:],str(hex(dec(cpu.reg_PC)+2)[2:]))+mem.read(cpu.reg_PB, str(hex(dec(cpu.reg_PC)+1))[2:],str(hex(dec(cpu.reg_PC)+1)[2:]))
        print temp, cpu.reg_A
        cpu.reg_A=hex(int(temp, 16) | int(cpu.reg_A, 16))[2:]
        while len(cpu.reg_A)<4:
            cpu.reg_A='0'+cpu.reg_A
        cpu.increment_PC(2)
        
    def TCD(self,cpu, mem):
        cpu.cycles+=2
        if cpu.debug==1:
            print cpu.cycles, 'TCD'
        cpu.reg_D==cpu.reg_A
        if dec(cpu.reg_D)==0:
            cpu.setflag('Z')
        else:
            cpu.setflag('Z', clear=1)
        if "{0:016b}".format(int(cpu.reg_D,16))[0]=='1':
            cpu.setflag('N')
        else:
            cpu.setflag('N', clear=1)
        cpu.increment_PC(1)
            
    def REP(self,cpu, mem):
        cpu.cycles+=3
        if cpu.debug==1:
            print cpu.cycles, 'REP'
        temp=mem.read(cpu.reg_PB, str(hex(dec(cpu.reg_PC)+1)), str(hex(dec(cpu.reg_PC)+1)))
        temp="{0:08b}".format(int(temp,16))
        temp_regP=list(cpu.reg_P)
        for i in range(len(temp)):
            if temp[i]=='1':
                temp_regP[i]='0'
        cpu.reg_P=''.join(temp_regP)
        cpu.increment_PC(2)

    def CLC(self,cpu, mem):
        cpu.cycles+=2
        if cpu.debug==1:
            print cpu.cycles, 'CLC'
        cpu.setflag('C', clear=1)
        cpu.increment_PC(1)

    def XCE(self,cpu, mem):
        cpu.cycles+=2
        if cpu.debug==1:
            print cpu.cycles, 'XCE'
        if cpu.reg_P[7]==1:
            self.emulationmode=1
        elif cpu.reg_P[7]==0:
            self.emulationmode=0
            cpu.setflag('MX')
        cpu.increment_PC(1)
    
    def RTI(self,cpu, mem):
        cpu.cycles+=6
        if cpu.debug==1:
            print cpu.cycles, 'RTI'
        cpu.reg_P="{0:08b}".format(int(self.stackpull(cpu,mem),16))
        cpu.increment_PC(1)
        cpu.reg_PC=self.stackpull(cpu,mem)+self.stackpull(cpu,mem)
        if cpu.emulationmode==0:
            cpu.reg_PB=self.stackpull(cpu,mem)
            cpu.cycles+=1

    def BRK(self,cpu, mem):
        #should have emulation mode for 6502
        cpu.cycles+=7        
        if cpu.debug==1:
            print cpu.cycles, 'BRK'
        if cpu.emulationmode==0:
            cpu.cycles+=1
            self.stackpush(cpu, mem, cpu.reg_PB)
            cpu.reg_PC=str(hex(dec(cpu.reg_PC)+2)[2:])
            self.stackpush(cpu, mem, cpu.reg_PC[2:])
            self.stackpush(cpu, mem, cpu.reg_PC[:2])
            self.stackpush(cpu, mem, hex(int(cpu.reg_P,2))[2:])
            cpu.setflag('I')
            cpu.setflag('D', clear=1)
            cpu.reg_PB='00'
            cpu.increment_PC(2)
            cpu.reg_PC=mem.read(cpu.reg_PB, 'FFE7', 'FFE7')+mem.read(cpu.reg_PB, 'FFE6', 'FFE6')
        elif cpu.emulationmode==1:
            cpu.reg_PC=str(hex(dec(cpu.reg_PC)+2)[2:])
            self.stackpush(cpu, mem, cpu.reg_PC[2:])
            self.stackpush(cpu, mem, cpu.reg_PC[:2])
            cpu.setflag('B')
            self.stackpush(cpu, mem, hex(int(cpu.reg_P,2))[2:])
            cpu.setflag('I')
            cpu.increment_PC(2)
            cpu.reg_PC=mem.read(cpu.reg_PB, 'FFFF', 'FFFF')+mem.read(cpu.reg_PB, 'FFFE', 'FFFE')

    def SEI(self,cpu, mem):
        cpu.cycles+=2
        if cpu.debug==1:
            print cpu.cycles,'SEI'
        cpu.setflag('I')
        cpu.increment_PC(1)
    
    def STZ_addr(self,cpu, mem):
        cpu.cycles+=4
        if cpu.debug==1:
            print cpu.cycles,
        addr=mem.read(cpu.reg_PB, str(hex(dec(cpu.reg_PC)+2))[2:],str(hex(dec(cpu.reg_PC)+2))[2:])+mem.read(cpu.reg_PB, str(hex(dec(cpu.reg_PC)+1))[2:],str(hex(dec(cpu.reg_PC)+1))[2:])
        if cpu.debug==1:
            print 'STZ(absolute) at ', cpu.reg_PB, addr
        mem.write(cpu.reg_PB, addr, '00')
        cpu.increment_PC(3)

    def LDA_const(self,cpu, mem):
        cpu.cycles+=2
        if cpu.debug==1:
            print cpu.cycles,
        if cpu.reg_P[2]=='1':
            temp=mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC)+1)[2:],hex(dec(cpu.reg_PC)+1)[2:])
            cpu.reg_A=cpu.reg_A[0:2]+temp
            cpu.increment_PC(2)
        elif cpu.reg_P[2]=='0':
            temp=mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC)+2)[2:],hex(dec(cpu.reg_PC)+2)[2:])+mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC)+1)[2:],hex(dec(cpu.reg_PC)+1)[2:])
            cpu.reg_A=mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC)+2)[2:],hex(dec(cpu.reg_PC)+2)[2:])+mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC)+1)[2:],hex(dec(cpu.reg_PC)+1)[2:])
            cpu.increment_PC(3)
        if dec(temp)==0:
            cpu.setflag('Z')
        elif bin(dec(temp))[2]==1:
            cpu.setflag('N')
        if cpu.debug==1:
            print 'LDA(immediate)'

            
