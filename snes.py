import numpy as np
import binascii
import sys
from cpu import *
from mem import *

ROMPATH="../SMW_rom.sfc"
#ROMPATH="../test.txt"

rom=rom(ROMPATH)
cpu=cpu(3580000)
mem=mem()
