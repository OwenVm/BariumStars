import pandas as pd
import numpy as np
import argparse
import textwrap
import numpy as np
from astropy.io import fits

parser = argparse.ArgumentParser(description="Conver 3 column text to 2 column ascii for bacchus",
                                epilog=textwrap.dedent(''' 
                                run as "python3 Merge.py  <name of input ascii file> <name of output txt file>"
                                ''')
                            )
parser.add_argument("input", type=str, help="text file")
parser.add_argument("output", type=str, help="Name of output file")
args = parser.parse_args()

input = args.input
output = args.output

data = np.loadtxt(f'{input}.txt', skiprows=1, usecols = (0, 1))

c1, c2 = data[:,0]*10, data[:,1]

newdata = np.array([c1, c2], dtype = object)

np.savetxt(f'{output}.asc', newdata.T,  delimiter="\t")

