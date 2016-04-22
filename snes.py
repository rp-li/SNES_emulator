import numpy as np
import binascii
import sys

ROMPATH="../SMW_rom.sfc"
#ROMPATH="../test.txt"

with open(ROMPATH, 'rb') as rom:
    content=rom.read()

rombuffer=binascii.hexlify(content)
print type(rombuffer)
