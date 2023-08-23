import pandas as pd
import numpy as np
import argparse

parser = argparse.ArgumentParser(description="Convert fits to ASCII file")
parser.add_argument("input", type=str, help="line file")
parser.add_argument("output", type=str, help="naam file")
args = parser.parse_args()

file = args.input
out = args.output

data = np.loadtxt(file)

newData = np.array([i for i in data])

np.savetxt(out, newData.T.flatten() ,fmt='%4.3f', newline = " ")
