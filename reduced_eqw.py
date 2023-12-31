import pandas as pd
import numpy as np
import argparse
import os 
import textwrap

parser = argparse.ArgumentParser(description="Select lines based on the equivalent widths.",
                                epilog=textwrap.dedent(''' 
                                run as "python3 reduced_eqw.py Fe_<star>.list Selected_Fe_lines_eqw_txt"
                                ''')
                            )
parser.add_argument("input", type=str, help="Path to the .eqw file")
parser.add_argument("output", type=str, help="Name of output file")

args = parser.parse_args()

file = args.input
out = args.output

lines = np.loadtxt(file, dtype = str, skiprows=2)

Excitation = lines[:,1].astype(str)

wavelength = lines[:,2].astype(float)
eqw_c = lines[:,5].astype(float)
eqw_o = lines[:,6].astype(float)

wavelength = lines[:,2].astype(float)
eqw_c = lines[:,5].astype(float)
eqw_o = lines[:,6].astype(float)
red_eqw_c = eqw_c/wavelength
red_eqw_o = eqw_o/wavelength

indexes = np.intersect1d(np.where(red_eqw_c < 0.025)[0], np.where(red_eqw_o < 0.025)[0])

newData = np.array([i for i in wavelength[indexes]])

count_I = 0
count_II = 0

for i in indexes:
    if Excitation[i] == '1':
        count_I += 1
    if Excitation[i] == '2':
        count_II += 1

print(f"Number of Fe I lines: {count_I}, number of Fe II lines: {count_II}")

np.savetxt(out, newData.T.flatten(), newline = " ", fmt='%4.3f')



