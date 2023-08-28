import pandas as pd
import numpy as np
import argparse
import getch
import os 

parser = argparse.ArgumentParser(description="Select lines from line file")
parser.add_argument("input", type=str, help="Name of line file")
parser.add_argument("output", type=str, help="Name of output file")
parser.add_argument('-d', '--detailed', action = 'store_true', help = "Shows Excitation if using Fe_allines.list")
#parser.add_argument("pdf", type=str, help="Path to pdf file")

#run as "python3 Selection.py <file with all Fe lines>.list Fe_selected_lines.txt" for not detailed
#or as "python3 Selection.py AllFe.txt.list Fe_selected_lines.txt -d" for detailed

args = parser.parse_args()

file = args.input
out = args.output
#pdf = args.pdf

if args.detailed:

    lines = np.loadtxt(file, dtype = str)

    data = lines[:,0].astype(float)
    Excitation = lines[:,-2].astype(str)

    count_I = 0
    count_II = 0

    SelectedLines = []
    print(f"If you want to accept a line, type 'y', if you want to reject just press any other key. To quit press 'q'")

    for i in range(len(data)):
        print(f"Accept line at {float(data[i])}? (page {i+1}/{len(data)}) (Fe {Excitation[i]}) (y/n)")

        #os.system(f"evince -i {i+1} {pdf}")
        accept = getch.getch()
        
        if accept == 'y':
            SelectedLines.append(data[i])
            
            if Excitation[i] == 'I':
                count_I += 1
            if Excitation[i] == 'II':
                count_II += 1
            print(f"Accepted, number of I lines = {count_I}, number of II lines = {count_II}")
        if accept == 'q':
            print("Quitting...")
            break

    newData = np.array([i for i in SelectedLines])
    np.savetxt(out, newData.T.flatten(), newline = " ", fmt='%4.3f')

else:
    data = np.loadtxt(file, dtype = float)

    SelectedLines = []

    print(f"If you want to accept a line, type 'y', if you want to reject just press any other key. To quit press 'q'")

    for i in range(len(data)):
        print(f"Accept line at {float(data[i])}? (page {i+1}/{len(data)}) (y/n)")
        accept = getch.getch()
        if accept == 'y':
            SelectedLines.append(data[i])
        if accept == 'q':
            print("Quitting..")
            break

    newData = np.array([i for i in SelectedLines])
    np.savetxt(out, newData.T.flatten(), newline = " ", fmt='%4.3f')