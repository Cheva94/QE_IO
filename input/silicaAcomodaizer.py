#!/usr/bin/python3.10

import argparse
import re
from pandas import read_csv
import numpy as np

def main():

    Files = args.input_File

    for File in Files:
        pCoord = 'ATOMIC_POSITIONS'
        pCell_x = '  A  =  '
        pCell_y = '  B  =  '
        pCell_z = '  C  =  '
        pAtoms = '  nat  ='
        line_counter = 0
        all, idx = [], []
        Cell, xyz = [], []

        with open(File, 'r') as f:
            for line in f.readlines():
                line_counter += 1
                if re.search(pCell_x, line):
                    Cell.append(float(line.split()[-1]))
                elif re.search(pCell_y, line):
                    Cell.append(float(line.split()[-1]))
                elif re.search(pCell_z, line):
                    Cell.append(float(line.split()[-1]))
                elif re.search(pAtoms, line):
                    nAt = int(line.split()[-1])
                elif re.search(pCoord, line):
                    idx.append(line_counter)

        idx = idx[0]

        with open(File, 'r') as f:
            all = f.read().split('\n')
        
        with open(File, 'r') as f:
            for line in range(nAt):
                xyz.append(all[idx+line].split()[:4])

        xyz = np.array(xyz)
        at = np.array(xyz[:,0])
        rx = np.array(xyz[:,1]).astype(float)
        ry = np.array(xyz[:,2]).astype(float)
        rz = np.array(xyz[:,3]).astype(float)
        
        for i in range(nAt):
            if rx[i] < 0:
                rx[i] += Cell[0]
            elif rx[i] > Cell[0]:
                rx[i] -= Cell[0]

            if ry[i] < 0:
                ry[i] += Cell[1]
            elif ry[i] > Cell[1]:
                ry[i] -= Cell[1]

            if rz[i] < 0:
                rz[i] += Cell[2]
            elif rz[i] > Cell[2]:
                rz[i] -= Cell[2]

        if np.min(rx) < 0.00001:
            rx += 0.0001

        if np.min(ry) < 0.00001:
            ry += 0.0001

        if np.min(rz) < 0.00001:
            rz += 0.0001

        xyz = np.vstack((at, rx, ry, rz)).T

        with open(f'{File.split(".")[0]}.xyz', 'w') as f:
            f.write(f'{nAt} \n\n')
            for line in range(nAt):
                f.write(f'{xyz[line,0]}       {float(xyz[line,1]):.6f}       {float(xyz[line,2]):.6f}       {float(xyz[line,3]):.6f} \n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('input_File', nargs='+', help = "Path to the output File.")

    args = parser.parse_args()

    main()
