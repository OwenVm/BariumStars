import pandas as pd
import numpy as np
import argparse
import os 

parser = argparse.ArgumentParser(description="Select lines from line file")
parser.add_argument("input", type=str, help="Path to the .list file")
parser.add_argument("output", type=str, help="Name of outpur file")


args = parser.parse_args()

file = args.input
out = args.output

lines = np.loadtxt(file, dtype = str, skiprows=2)

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

np.savetxt(out, newData.T.flatten(), newline = " ", fmt='%4.3f')



