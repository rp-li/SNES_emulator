def dec(addr):
    if type(addr)==int:
        return addr
    elif type(addr)==str:
        return int(addr,16)

def hextobcd_decimal(val):
    #val in big endian
    val=bin(int(val, base=16))[2:].zfill(16)
    bcds={'0000':'0','0001':'1','0010':'2','0011':'3','0100':'4','0101':'5',
          '0110':'6','0111':'7','1000':'8','1001':'9'}
    out=''
    for i in range(0,len(val),4):
        out=out+bcds[val[i:i+4]]
    return int(out, base=10)

def dectobcd_binary(val):
    bcds=['0000','0001','0010','0011','0100','0101',
          '0110','0111','1000','1001']
    val=str(val)
    out=''
    for i in range(len(val)):
        out=out+bcds[int(val[i],base=10)]
    return out

def reverse_endian(val):
    if type(val)==str and len(val)>=4:
        return val[2:]+val[:2]

def checkborrow(a,b):
    mask=0xffff
    not_a=~a&mask
    if not_a&(a^b)!=0:
        return True
    else:
        return False
    
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
        self.dict['a2']=self.LDX_const
        self.dict['a0']=self.LDY_const
        self.dict['8f']=self.STA_long
        self.dict['9f']=self.STA_long_X
        self.dict['98']=self.TYA
        self.dict['38']=self.SEC
        self.dict['e9']=self.SBC_const
        self.dict['a8']=self.TAY
        self.dict['ca']=self.DEX

    def DEX(self,cpu,mem):
        cpu.cycles+=2
        if cpu.debug==1:
            print cpu.cycles, 'DEX'
        if cpu.reg_P[2]=='0':
            cpu.reg_X=hex(dec(cpu.reg_X)-1)[2:].zfill(4)
            if bin(int(cpu.reg_X, base=16))[2:].zfill(4)[0]=='1':
                cpu.setflag('N')
            elif int(cpu.reg_X, base=16)==0:
                cpu.setflag('Z')
        elif cpu.reg_P[2]=='1':
            cpu.reg_X=cpu.reg_X[:2]+hex(dec(cpu.reg_X[2:])-1)[2:].zfill(2)
            if bin(int(cpu.reg_X[2:], base=16))[2:].zfill(2)[0]=='1':
                cpu.setflag('N')
            elif int(cpu.reg_X[2:], base=16)==0:
                cpu.setflag('Z')
        cpu.increment_PC(1)

    def SBC_const(self,cpu,mem): #this is broken for BCD mode
        cpu.cycles+=2
        if cpu.debug==1:
            print cpu.cycles, 'SBC(immediate)'
        if cpu.reg_P[2]=='0':
            if cpu.reg_P[4]=='0': #non decimal
                temp_a=dec(cpu.reg_A)
                temp_b=dec(reverse_endian(mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC)+1)[2:],hex(dec(cpu.reg_PC)+2)[2:])))
                cpu.reg_A=hex(temp_a-temp_b)[2:].zfill(4)[-4:]
            elif cpu.reg_P[4]=='1':
                temp_a=hextobcd_decimal(cpu.reg_A)
                temp_b=hextobcd_decimal(reverse_endian(mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC)+1)[2:],hex(dec(cpu.reg_PC)+2)[2:])))
                cpu.reg_A=hex(int(dectobcd_binary(temp_a-temp_b),base=2)).zfill(4)[-4:]
            if checkborrow(temp_a, temp_b):
                cpu.setflag('B')
            if bin(dec(cpu.reg_A))[2]==1:
                cpu.setflag('N')
            elif dec(cpu.reg_A)==0:
                cpu.setflag('Z')
            #might need to recheck overflow and negative condition
            if temp_a-temp_b>32767 or temp_a-temp_b<-32768:
                cpu.setflag('V')                   
            cpu.increment_PC(3)
        elif cpu.reg_P[2]=='1':
            if cpu.reg_P[4]=='0':
                temp_a=dec(cpu.reg_A[2:])
                temp_b=dec(mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC)+1)[2:],hex(dec(cpu.reg_PC)+1)[2:]))
                cpu.reg_A=cpu.reg_A[:2]+hex(temp_a-temp_b)[2:].zfill(2)[-2:]   
            if cpu.reg_P[4]=='1':
                temp_a=hextobcd_decimal(cpu.reg_A[2:])
                temp_b=hextobcd_decimal(reverse_endian(mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC)+1)[2:],str(hex(dec(cpu.reg_PC)+1))[2:])))
                cpu.reg_A=cpu.reg_A[:2]+hex(int(dectobcd_binary(temp_a-temp_b),base=2)).zfill(2)[-2:]
            if checkborrow(temp_a, temp_b):
                cpu.setflag('B')            
            if bin(dec(cpu.reg_A[2:]))[2]==1:
                cpu.setflag('N')
            elif dec(cpu.reg_A[2:])==0:
                cpu.setflag('Z')
            if temp_a-temp_b>127 or temp_a-temp_b<-128:
                cpu.setflag('V')
            cpu.increment_PC(2)

    def TYA(self,cpu,mem):
        cpu.cycles+=2
        if cpu.debug==1:
            print cpu.cycles, 'TYA'
        if cpu.reg_P[2]=='1':
            if cpu.reg_P[3]=='1':
                cpu.reg_A[2:]=cpu.reg_Y[2:]
                if "{0:08b}".format(int(cpu.reg_Y[2:],16))[0]=='1':
                    cpu.setflag('N')
                if dec(cpu.reg_Y[2:])==0:
                    cpu.setflag('Z')
            elif cpu.reg_P[3]=='0':
                cpu.reg_A[2:]=cpu.reg_Y[2:]
                if "{0:08b}".format(int(cpu.reg_Y[2:],16))[0]=='1':
                    cpu.setflag('N')
                if dec(cpu.reg_Y[2:])==0:
                    cpu.setflag('Z')
        elif cpu.reg_P[2]=='0':
            if cpu.reg_P[3]=='1':
                cpu.reg_A[2:]=cpu.reg_Y[2:]
                cpu.reg_A[:2]='00'
                if "{0:08b}".format(int(cpu.reg_Y[2:],16))[0]=='1':
                    cpu.setflag('N')
                if dec(cpu.reg_Y[2:])==0:
                    cpu.setflag('Z')
            elif cpu.reg_P[3]=='0':
                cpu.reg_A=cpu.reg_Y
                if "{0:016b}".format(int(cpu.reg_Y,16))[0]=='1':
                    cpu.setflag('N')
                if dec(cpu.reg_Y)==0:
                    cpu.setflag('Z')
        cpu.increment_PC(1)

    def TAY(self,cpu,mem):
        cpu.cycles+=2
        if cpu.debug==1:
            print cpu.cycles, 'TAY'
        if cpu.reg_P[2]=='1':
            if cpu.reg_P[3]=='1':
                cpu.reg_Y[2:]=cpu.reg_A[2:]
                if "{0:08b}".format(int(cpu.reg_A[2:],16))[0]=='1':
                    cpu.setflag('N')
                if dec(cpu.reg_A[2:])==0:
                    cpu.setflag('Z')
            elif cpu.reg_P[3]=='0':
                cpu.reg_Y=cpu.reg_A
                if "{0:08b}".format(int(cpu.reg_A,16))[0]=='1':
                    cpu.setflag('N')
                if dec(cpu.reg_A)==0:
                    cpu.setflag('Z')
        elif cpu.reg_P[2]=='0':
            if cpu.reg_P[3]=='1':
                cpu.reg_Y[2:]=cpu.reg_A[2:]
                if "{0:08b}".format(int(cpu.reg_A[2:],16))[0]=='1':
                    cpu.setflag('N')
                if dec(cpu.reg_A[2:])==0:
                    cpu.setflag('Z')
            elif cpu.reg_P[3]=='0':
                cpu.reg_A=cpu.reg_Y
                if "{0:016b}".format(int(cpu.reg_Y,16))[0]=='1':
                    cpu.setflag('N')
                if dec(cpu.reg_Y)==0:
                    cpu.setflag('Z')
        cpu.increment_PC(1)

    def STA_long_X(self,cpu,mem):
        cpu.cycles+=5
        temp_pb=mem.read(cpu.reg_PB, str(hex(dec(cpu.reg_PC)+3))[2:],str(hex(dec(cpu.reg_PC)+3)[2:]))
        temp_addr=reverse_endian(mem.read(cpu.reg_PB, str(hex(dec(cpu.reg_PC)+1))[2:],str(hex(dec(cpu.reg_PC)+2)[2:])))
        temp_addr=hex(dec(temp_addr)+dec(cpu.reg_X))[2:]
        mem.write(temp_pb, temp_addr, reverse_endian(cpu.reg_A))
        if cpu.debug==1:
            print cpu.cycles, 'STA(abs,long,X) at', temp_pb, temp_addr
        if cpu.reg_P[2]=='0':
            cpu.cycles+=1
        cpu.increment_PC(4)

    def STA_long(self,cpu,mem):
        cpu.cycles+=5
        temp_pb=mem.read(cpu.reg_PB, str(hex(dec(cpu.reg_PC)+3))[2:],str(hex(dec(cpu.reg_PC)+3)[2:]))
        temp_addr=reverse_endian(mem.read(cpu.reg_PB, str(hex(dec(cpu.reg_PC)+1))[2:],str(hex(dec(cpu.reg_PC)+2)[2:])))
        mem.write(temp_pb, temp_addr, reverse_endian(cpu.reg_A))
        if cpu.debug==1:
            print cpu.cycles, 'STA(abs,long) at', temp_pb, temp_addr
        if cpu.reg_P[2]=='0':
            cpu.cycles+=1
        cpu.increment_PC(4)
        
    def LDX_const(self,cpu,mem):
        cpu.cycles+=2
        if cpu.debug==1:
            print cpu.cycles, 'LDX(immediate)'
        if cpu.reg_P[2]=='1':
            temp=mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC)+1)[2:],hex(dec(cpu.reg_PC)+1)[2:])
            cpu.reg_X=cpu.reg_X[:2]+temp
            cpu.increment_PC(2)
        elif cpu.reg_P[2]=='0':
            temp=reverse_endian(mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC)+1)[2:],hex(dec(cpu.reg_PC)+2)[2:]))
            cpu.reg_X=temp
            cpu.increment_PC(3)
        if dec(temp)==0:
            cpu.setflag('Z')
        elif "{0:016b}".format(int(temp,16))[0]=='1':
            cpu.setflag('N')

    def LDY_const(self,cpu,mem):
        cpu.cycles+=2
        if cpu.debug==1:
            print cpu.cycles, 'LDY(immediate)'
        if cpu.reg_P[2]=='1':
            temp=mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC)+1)[2:],hex(dec(cpu.reg_PC)+1)[2:])
            cpu.reg_Y=cpu.reg_Y[:2]+temp
            cpu.increment_PC(2)
        elif cpu.reg_P[2]=='0':
            temp=reverse_endian(mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC)+1)[2:],hex(dec(cpu.reg_PC)+2)[2:]))
            cpu.reg_Y=temp
            cpu.increment_PC(3)
        if dec(temp)==0:
            cpu.setflag('Z')
        elif "{0:016b}".format(int(temp,16))[0]=='1':
            cpu.setflag('N')

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
        temp=reverse_endian(mem.read(cpu.reg_PB, str(hex(dec(cpu.reg_PC)+1))[2:],str(hex(dec(cpu.reg_PC)+2)[2:])))
        print temp, cpu.reg_A
        cpu.reg_A=hex(int(temp, 16) | int(cpu.reg_A, 16))[2:].zfill(4)
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
            cpu.reg_PC=reverse_endian(mem.read(cpu.reg_PB, 'FFE6', 'FFE7'))
        elif cpu.emulationmode==1:
            cpu.reg_PC=str(hex(dec(cpu.reg_PC)+2)[2:])
            self.stackpush(cpu, mem, cpu.reg_PC[2:])
            self.stackpush(cpu, mem, cpu.reg_PC[:2])
            cpu.setflag('B')
            self.stackpush(cpu, mem, hex(int(cpu.reg_P,2))[2:])
            cpu.setflag('I')
            cpu.increment_PC(2)
            cpu.reg_PC=reverse_endian(mem.read(cpu.reg_PB, 'FFFE', 'FFFF'))

    def SEI(self,cpu, mem):
        cpu.cycles+=2
        if cpu.debug==1:
            print cpu.cycles,'SEI'
        cpu.setflag('I')
        cpu.increment_PC(1)

    def SEC(self,cpu, mem):
        cpu.cycles+=2
        if cpu.debug==1:
            print cpu.cycles,'SEC'
        cpu.setflag('C')
        cpu.increment_PC(1)    
    
    def STZ_addr(self,cpu, mem):
        cpu.cycles+=4
        if cpu.debug==1:
            print cpu.cycles,
        addr=reverse_endian(mem.read(cpu.reg_PB, str(hex(dec(cpu.reg_PC)+1))[2:],str(hex(dec(cpu.reg_PC)+2))[2:]))
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
            temp=reverse_endian(mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC)+1)[2:],hex(dec(cpu.reg_PC)+2)[2:]))
            cpu.reg_A=reverse_endian(mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC)+1)[2:],hex(dec(cpu.reg_PC)+2)[2:]))
            cpu.increment_PC(3)
        if dec(temp)==0:
            cpu.setflag('Z')
        elif bin(dec(temp))[2]==1:
            cpu.setflag('N')
        if cpu.debug==1:
            print 'LDA(immediate)'
        
    def stackpush(self, cpu, mem, val):
        mem.write('00', cpu.reg_S, val) #stack push
        if cpu.debug==1:
            print val, 'pushed to ', cpu.reg_S
        cpu.reg_S=hex(dec(cpu.reg_S)-1)[2:].zfill(4)
        while len(cpu.reg_S)<4:
            cpu.reg_S='0'+cpu.reg_S

    def stackpull(self, cpu, mem):
        cpu.reg_S=hex(dec(cpu.reg_S)+1)[2:].zfill(4)
        val=mem.read('00', cpu.reg_S, cpu.reg_S)
        if cpu.debug==1:
            print val, 'pulled from ', cpu.reg_S
        return val
