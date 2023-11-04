import pandas as pd
import numpy as np
import argparse
import textwrap
import numpy as np
from astropy.io import fits

parser = argparse.ArgumentParser(description="Conver 2 column ascii to 3 column text for iSpec",
                                epilog=textwrap.dedent(''' 
                                run as "python3 Merge.py  <name of input ascii file> <name of output txt file>"
                                ''')
                            )
parser.add_argument("input", type=str, help="Ascii file")
parser.add_argument("output", type=str, help="Name of output file")
parser.add_argument("-e", "--error", type=int, help="Computes error", required=False)
args = parser.parse_args()

input = args.input
output = args.output
error = args.error

data = np.loadtxt(f'{input}.asc')

columns = ['waveobs', 'flux', 'err']

c1 = data[:,0]/10
c2 = data[:,1]
c3 = np.zeros(len(c1))

if error == 1:
    c3 = np.sqrt(np.abs(c2))

newdata = np.array([c1, c2, c3], dtype = object)

np.savetxt(f'{output}.txt', newdata.T,  delimiter="\t")

#add header
copy = open(f'{output}.txt', 'r')
original = copy.read()
copy.close

copy = open(f'{output}.txt', 'w')
copy.write(f'waveobs\tflux\terrr\n')
copy.write(original)
copy.close()

