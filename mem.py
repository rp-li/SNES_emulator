import numpy as np
import binascii
import sys

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
