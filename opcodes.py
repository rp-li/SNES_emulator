#################################################################
#  file containing 65816 CPU opcodes
#  also includes a few useful bit manipulation functions
##################################################################

        
def stackpush(cpu, mem, val):    #only pushes 1 byte at a time, normally stackpushes high byte first then low
    mem.write('00', cpu.reg_S, val) #stack push
    if cpu.debug==1:
        print val, 'pushed to ', cpu.reg_S
    cpu.reg_S=hex(dec(cpu.reg_S)-1)[2:].zfill(4)
    while len(cpu.reg_S)<4:
        cpu.reg_S='0'+cpu.reg_S

def stackpull(cpu, mem):
    cpu.reg_S=hex(dec(cpu.reg_S)+1)[2:].zfill(4)
    val=mem.read('00', cpu.reg_S, cpu.reg_S)
    if cpu.debug==1:
        print val, 'pulled from ', cpu.reg_S
    return val

def binary(val): #hex to bin
    return "{0:00b}".format(int(val,16))

def dec(addr):  #hex to dec
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

def twos_to_dec(a, nbits):  #a in binary string, unsigned
    a=a.zfill(nbits)
    if a[0]=='1':
        a=int(a,base=2)
        mask=2**nbits-1
        a=~a&mask
        a+=1
        return -int(bin(a)[-(nbits-1):],base=2)
    elif a[0]=='0':
        return int(a,base=2)
   

def binsubtract(a,b): #a and b are binary strings, two's complement
    mask=0xffff
    b=int(b,base=2)
    b=bin(int(bin(b^mask),base=2)+1)[2:]
    return bin(int(a,2) + int(b,2))[-16:]
    
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
        self.dict['8d']=self.STA_addr
        self.dict['98']=self.TYA
        self.dict['38']=self.SEC
        self.dict['e9']=self.SBC_const
        self.dict['a8']=self.TAY
        self.dict['ca']=self.DEX
        self.dict['10']=self.BPL
        self.dict['d0']=self.BNE
        self.dict['80']=self.BRA
        self.dict['e2']=self.SEP
        self.dict['20']=self.JSR_addr
        self.dict['08']=self.PHP
        self.dict['48']=self.PHA
        self.dict['cd']=self.CMP_addr
        self.dict['b7']=self.LDA_dp_Y_long
        self.dict['c8']=self.INY
        self.dict['aa']=self.TAX

    def INY(self,cpu,mem):
        cpu.cycles+=2
        cpu.reg_Y=hex(dec(cpu.reg_Y)+1)[2:].zfill(4)
        cpu.increment_PC(1)
        if cpu.debug==1:
            print cpu.cycles, 'INY'
        if dec(cpu.reg_Y)==0:
            cpu.setflag('Z')
        elif "{0:016b}".format(int(cpu.reg_Y,16))[0]=='1':
            cpu.setflag('N')
        
    def CMP_addr(self,cpu,mem):
        cpu.cycles+=4
        temp_addr=reverse_endian(mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC)+1)[2:],hex(dec(cpu.reg_PC)+2)[2:]))
        if cpu.debug==1:
            print cpu.cycles, 'CMP(abs) at', temp_addr
        if cpu.reg_P[2]=='0':
            cpu.cycles+=1
            temp_val=reverse_endian(mem.read(cpu.reg_PB,dec(temp_addr),dec(temp_addr)+1))
            temp_res=dec(cpu.reg_A)-dec(temp_val)
            temp_res=hex(temp_res)[2:].zfill(4)
            if bin(int(temp_res,base=16)).zfill(16)[2:][0]=='1':
                cpu.setflag('N')
            elif int(temp_res, base=16)==0:
                cpu.setflag('Z')
            if int(cpu.reg_A,base=16)<int(temp_val, base=16):
                cpu.setflag('C', clear=1)
            else:
                cpu.setflag('C')                
        elif cpu.reg_P[2]=='1':
            temp_val=mem.read(cpu.reg_PB,dec(temp_addr),dec(temp_addr))
            temp_res=dec(cpu.reg_A[2:])-dec(temp_val)
            temp_res=hex(temp_res)[2:].zfill(2)
            if bin(int(temp_res,base=16)).zfill(8)[2:][0]=='1':
                cpu.setflag('N')
            elif int(temp_res, base=16)==0:
                cpu.setflag('Z')
            if int(cpu.reg_A[2:],base=16)<int(temp_val, base=16):
                cpu.setflag('C', clear=1)
            else:
                cpu.setflag('C')               
        #print temp_val, temp_res, cpu.reg_A
        cpu.increment_PC(3)
        
    def PHA(self,cpu,mem):
        if cpu.debug==1:
            print cpu.cycles, 'PHA'
        cpu.cycles+=3
        if cpu.emulationmode==1 or cpu.reg_P[2]=='1':
            stackpush(cpu,mem,cpu.reg_A[2:])
            #print '8bit'
        else:
            cpu.cycles+=1
            stackpush(cpu,mem,cpu.reg_A[:2])
            stackpush(cpu,mem,cpu.reg_A[2:])
        cpu.increment_PC(1)

    def PHP(self,cpu,mem):
        cpu.cycles+=3
        if cpu.debug==1:
            print cpu.cycles, 'PHP'
        temp=hex(int(cpu.reg_P,base=2))[2:]
        stackpush(cpu,mem,temp)
        cpu.increment_PC(1)

    def JSR_addr(self,cpu,mem):
        cpu.cycles+=6
        if cpu.debug==1:
            print cpu.cycles, 'JSR(abs)'
        stackpush(cpu, mem, cpu.reg_PC[:2])
        stackpush(cpu, mem, cpu.reg_PC[2:])
        cpu.reg_PC=reverse_endian(mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC)+1)[2:],hex(dec(cpu.reg_PC)+2)[2:]))

    def BRA(self,cpu,mem):  #branching might have issues if crossing page boundary
        cpu.cycles+=3
        #print cpu.reg_PC
        cpu.cycles+=1
        temp=mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC)+1)[2:],hex(dec(cpu.reg_PC)+1)[2:])  
        temp=temp.zfill(4)
        #print temp
        cpu.increment_PC(2)
        cpu.reg_PC=hex(dec(cpu.reg_PC)+twos_to_dec(binary(temp),8))[2:]
        if cpu.debug==1:
            print cpu.cycles, 'BRA of (dec)', twos_to_dec(binary(temp),8)
                
    def BNE(self,cpu,mem):
        cpu.cycles+=2
        #print cpu.reg_PC
        if cpu.reg_P[6]=='0':
            cpu.cycles+=1
            temp=mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC)+1)[2:],hex(dec(cpu.reg_PC)+1)[2:])  
            temp=temp.zfill(4)
            #print temp
            cpu.increment_PC(2)
            cpu.reg_PC=hex(dec(cpu.reg_PC)+twos_to_dec(binary(temp),8))[2:]
            if cpu.debug==1:
                print cpu.cycles, 'BNE of (dec)', twos_to_dec(binary(temp),8)
        else:
            cpu.increment_PC(2)
            if cpu.debug==1:
                print cpu.cycles, 'BNE (no branch)'

    def BPL(self,cpu,mem):
        cpu.cycles+=2
        #print cpu.reg_PC
        if cpu.emulationmode==1:
            cpu.cycles+=1
        if cpu.reg_P[0]=='0':
            cpu.cycles+=1
            temp=mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC)+1)[2:],hex(dec(cpu.reg_PC)+1)[2:])  
            temp=temp.zfill(4)
            #print temp
            cpu.increment_PC(2)
            cpu.reg_PC=hex(dec(cpu.reg_PC)+twos_to_dec(binary(temp),8))[2:]
            if cpu.debug==1:
                print cpu.cycles, 'BPL of (dec)', twos_to_dec(binary(temp),8)
        else:
            cpu.increment_PC(2)
            if cpu.debug==1:
                print cpu.cycles, 'BPL (no branch)'

    def DEX(self,cpu,mem):
        #print cpu.reg_X
        cpu.cycles+=2
        if cpu.debug==1:
            print cpu.cycles, 'DEX'
        if cpu.reg_P[2]=='0':
            if cpu.reg_X=='0000':
                cpu.reg_X='ffff'
            else:
                cpu.reg_X=hex(dec(cpu.reg_X)-1)[2:].zfill(4)
            if bin(int(cpu.reg_X, base=16))[2:].zfill(16)[0]=='1':
                cpu.setflag('N')
            elif int(cpu.reg_X, base=16)==0:
                cpu.setflag('Z')
        elif cpu.emulationmode==1 or cpu.reg_P[2]=='1':
            if cpu.reg_X=='0000':
                cpu.reg_X='ffff'
            else:
                cpu.reg_X=cpu.reg_X[:2]+hex(dec(cpu.reg_X[2:])-1)[2:].zfill(2)
            if bin(int(cpu.reg_X[2:], base=16))[2:].zfill(8)[0]=='1':
                cpu.setflag('N')
            elif int(cpu.reg_X[2:], base=16)==0:
                cpu.setflag('Z')
        cpu.increment_PC(1)

    def SBC_const(self,cpu,mem): #this is broken for negative results, need to recheck borrow bit C
        cpu.cycles+=2
        if cpu.debug==1:
            print cpu.cycles, 'SBC(immediate)'
        if cpu.reg_P[2]=='0':
            if cpu.reg_P[4]=='0': #non decimal
                temp_a=dec(cpu.reg_A)
                temp_b=dec(reverse_endian(mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC)+1)[2:],hex(dec(cpu.reg_PC)+2)[2:])))
                if temp_a<temp_b:
                    print '###subtraction just wewnt negative here, expect problems'
                cpu.reg_A=hex(temp_a-temp_b)[2:].zfill(4)[-4:]
            elif cpu.reg_P[4]=='1':
                temp_a=hextobcd_decimal(cpu.reg_A)
                temp_b=hextobcd_decimal(reverse_endian(mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC)+1)[2:],hex(dec(cpu.reg_PC)+2)[2:])))
                cpu.reg_A=hex(int(dectobcd_binary(temp_a-temp_b),base=2)).zfill(4)[-4:]
                if temp_a<temp_b:
                    print '###subtraction just wewnt negative here, expect problems'
            #if checkborrow(temp_a, temp_b):
            #    cpu.setflag('B')
            if bin(dec(cpu.reg_A))[2]==1:
                cpu.setflag('N')
            elif dec(cpu.reg_A)==0:
                cpu.setflag('Z')
            #might need to recheck overflow and negative condition
            if temp_a-temp_b>32767 or temp_a-temp_b<-32768:
                cpu.setflag('V')                   
            cpu.increment_PC(3)
        elif cpu.emulationmode==1 or cpu.reg_P[2]=='1':
            if cpu.reg_P[4]=='0':
                temp_a=dec(cpu.reg_A[2:])
                temp_b=dec(mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC)+1)[2:],hex(dec(cpu.reg_PC)+1)[2:]))
                cpu.reg_A=cpu.reg_A[:2]+hex(temp_a-temp_b)[2:].zfill(2)[-2:]   
                if temp_a<temp_b:
                    print '###subtraction just wewnt negative here, expect problems'
            if cpu.reg_P[4]=='1':
                temp_a=hextobcd_decimal(cpu.reg_A[2:])
                temp_b=hextobcd_decimal(reverse_endian(mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC)+1)[2:],str(hex(dec(cpu.reg_PC)+1))[2:])))
                if temp_a<temp_b:
                    print '###subtraction just wewnt negative here, expect problems'
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
                cpu.reg_Y=cpu.reg_A
                if "{0:016b}".format(int(cpu.reg_A,16))[0]=='1':
                    cpu.setflag('N')
                if dec(cpu.reg_A)==0:
                    cpu.setflag('Z')
        cpu.increment_PC(1)

    def TAX(self,cpu,mem):
        cpu.cycles+=2
        if cpu.debug==1:
            print cpu.cycles, 'TAX'
        if cpu.reg_P[2]=='1':
            if cpu.reg_P[3]=='1':
                cpu.reg_X[2:]=cpu.reg_A[2:]
                if "{0:08b}".format(int(cpu.reg_A[2:],16))[0]=='1':
                    cpu.setflag('N')
                if dec(cpu.reg_A[2:])==0:
                    cpu.setflag('Z')
            elif cpu.reg_P[3]=='0':
                cpu.reg_X=cpu.reg_A
                if "{0:08b}".format(int(cpu.reg_A,16))[0]=='1':
                    cpu.setflag('N')
                if dec(cpu.reg_A)==0:
                    cpu.setflag('Z')
        elif cpu.reg_P[2]=='0':
            if cpu.reg_P[3]=='1':
                cpu.reg_X[2:]=cpu.reg_A[2:]
                if "{0:08b}".format(int(cpu.reg_A[2:],16))[0]=='1':
                    cpu.setflag('N')
                if dec(cpu.reg_A[2:])==0:
                    cpu.setflag('Z')
            elif cpu.reg_P[3]=='0':
                cpu.reg_X=cpu.reg_A
                if "{0:016b}".format(int(cpu.reg_A,16))[0]=='1':
                    cpu.setflag('N')
                if dec(cpu.reg_A)==0:
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

    def STA_addr(self,cpu,mem):
        cpu.cycles+=4
        temp_addr=reverse_endian(mem.read(cpu.reg_PB, str(hex(dec(cpu.reg_PC)+1))[2:],str(hex(dec(cpu.reg_PC)+2)[2:])))
        if cpu.emulationmode==1 or cpu.reg_P[2]=='1':
            mem.write(cpu.reg_PB, temp_addr, cpu.reg_A[2:])
        else:
            cpu.cycles+=1
            mem.write(cpu.reg_PB, temp_addr, reverse_endian(cpu.reg_A))
        if cpu.debug==1:
            print cpu.cycles, 'STA(abs) at', temp_addr    
        cpu.increment_PC(3)
        
    def LDX_const(self,cpu,mem):
        cpu.cycles+=2
        if cpu.debug==1:
            print cpu.cycles, 'LDX(immediate)'
        if cpu.emulationmode==1 or cpu.reg_P[2]=='1':
            temp=mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC)+1)[2:],hex(dec(cpu.reg_PC)+1)[2:])
            cpu.reg_X=cpu.reg_X[:2]+temp
            cpu.increment_PC(2)
            if "{0:08b}".format(int(temp,16))[0]=='1':
                cpu.setflag('N')
        elif cpu.reg_P[2]=='0':
            temp=reverse_endian(mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC)+1)[2:],hex(dec(cpu.reg_PC)+2)[2:]))
            cpu.reg_X=temp
            cpu.increment_PC(3)
            if "{0:016b}".format(int(temp,16))[0]=='1':
                cpu.setflag('N')
        if dec(temp)==0:
            cpu.setflag('Z')

    def LDY_const(self,cpu,mem):
        cpu.cycles+=2
        if cpu.debug==1:
            print cpu.cycles, 'LDY(immediate)'
        if cpu.emulationmode==1 or cpu.reg_P[2]=='1':
            temp=mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC)+1)[2:],hex(dec(cpu.reg_PC)+1)[2:])
            cpu.reg_Y=cpu.reg_Y[:2]+temp
            cpu.increment_PC(2)
            if "{0:08b}".format(int(temp,16))[0]=='1':
                cpu.setflag('N')
        elif cpu.reg_P[2]=='0':
            temp=reverse_endian(mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC)+1)[2:],hex(dec(cpu.reg_PC)+2)[2:]))
            cpu.reg_Y=temp
            cpu.increment_PC(3)
            if "{0:016b}".format(int(temp,16))[0]=='1':
                cpu.setflag('N')
        if dec(temp)==0:
            cpu.setflag('Z')

    def TCS(self,cpu,mem):
        cpu.cycles+=2
        if cpu.debug==1:
            print cpu.cycles, 'TCS'
        cpu.reg_S=cpu.reg_A
        cpu.increment_PC(1)

    def ORA_dp_X_indirect(self,cpu,mem):  # need to check X indexing
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
        temp=mem.read(cpu.reg_PB, str(hex(dec(cpu.reg_PC)+1)), str(hex(dec(cpu.reg_PC)+1)))
        temp="{0:08b}".format(int(temp,16))
        temp_regP=list(cpu.reg_P)
        for i in range(len(temp)):
            if temp[i]=='1':
                temp_regP[i]='0'
        cpu.reg_P=''.join(temp_regP)
        if cpu.debug==1:
            print cpu.cycles, 'REP', temp
        cpu.increment_PC(2)

    def SEP(self,cpu, mem):
        cpu.cycles+=3
        temp=mem.read(cpu.reg_PB, str(hex(dec(cpu.reg_PC)+1)), str(hex(dec(cpu.reg_PC)+1)))
        temp="{0:08b}".format(int(temp,16))
        temp_regP=list(cpu.reg_P)
        for i in range(len(temp)):
            if temp[i]=='1':
                temp_regP[i]='1'
        cpu.reg_P=''.join(temp_regP)
        if cpu.debug==1:
            print cpu.cycles, 'SEP', temp
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
        if cpu.reg_P[7]=='1':
            cpu.emulationmode=1
        elif cpu.reg_P[7]=='0':
            cpu.emulationmode=0
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
            self.stackpush(cpu, mem, cpu.reg_PC[:2])
            self.stackpush(cpu, mem, cpu.reg_PC[2:])
            self.stackpush(cpu, mem, hex(int(cpu.reg_P,2))[2:])
            cpu.setflag('I')
            cpu.setflag('D', clear=1)
            cpu.reg_PB='00'
            cpu.increment_PC(2)
            cpu.reg_PC=reverse_endian(mem.read(cpu.reg_PB, 'FFE6', 'FFE7'))
        elif cpu.emulationmode==1:
            cpu.reg_PC=str(hex(dec(cpu.reg_PC)+2)[2:])
            self.stackpush(cpu, mem, cpu.reg_PC[:2])
            self.stackpush(cpu, mem, cpu.reg_PC[2:])
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
        if cpu.emulationmode==1 or cpu.reg_P[2]=='1':
            temp=mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC)+1)[2:],hex(dec(cpu.reg_PC)+1)[2:])
            cpu.reg_A=cpu.reg_A[0:2]+temp
            cpu.increment_PC(2)
        elif cpu.reg_P[2]=='0':
            temp=reverse_endian(mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC)+1)[2:],hex(dec(cpu.reg_PC)+2)[2:]))
            cpu.reg_A=temp
            cpu.increment_PC(3)
        if cpu.debug==1:
            print cpu.cycles,'LDA(immediate)'
        if dec(temp)==0:
            cpu.setflag('Z')
        elif bin(dec(temp))[2]==1:
            cpu.setflag('N')
            
    def LDA_dp_Y_long(self,cpu,mem):  #have to recheck this addressing mode
        cpu.cycles+=6
        temp=mem.read(cpu.reg_PB,hex(dec(cpu.reg_PC)+1)[2:],hex(dec(cpu.reg_PC)+1)[2:])
        if cpu.reg_P[2]=='0':
            temp=temp+cpu.reg_D
            temp=hex(dec(temp)+dec(cpu.reg_Y))[2:].zfill(6)
            cpu.reg_A=reverse_endian(mem.read(temp[:2],temp[2:],hex(dec(temp[2:])+1)[2:]))
            cpu.increment_PC(2)
            cpu.cycles+=1
        if cpu.debug==1:
            print cpu.cycles, 'LDA(dp,long,Y) at', temp
        if dec(cpu.reg_A)==0:
            cpu.setflag('Z')
        elif "{0:016b}".format(int(cpu.reg_A,16))[0]=='1':
            cpu.setflag('N')


