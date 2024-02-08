#!/usr/bin/python3.10

import argparse
import re
from pandas import read_csv
import numpy as np

def main():

    File = args.input_File

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
    rz = np.array(xyz[:,3]).astype(float)
    top2 = len(rz[rz>8.5])
    xyz = xyz[-top2:, :]

    topAtoms_z = len(rz[rz>10.0])
    topAtoms = xyz[-topAtoms_z:, :]
    
    O_avgH = np.mean(rz[(8.5<rz) & (rz<9.5)]) - 1.49
    
    rzT = np.array(topAtoms[:,3]).astype(float)
    rzT *= -1
    sup = np.max(rzT)
    rzT += O_avgH - sup
    
    inf = np.min(rzT)
    rzT += 0.0001 - inf

    rzB = np.array(xyz[:,3]).astype(float)
    rzB += 0.0001 - inf

    with open(f'{File.split(".")[0]}.xsf', 'w') as f:
        f.write(f'ANIMSTEPS 1 \n')
        f.write(f'CRYSTAL \n')
        f.write(f'PRIMVEC \n')
        f.write(f'    {Cell[0]}    0.0     0.0 \n')
        f.write(f'    0.0    {Cell[1]}     0.0 \n')
        f.write(f'    0.0    0.0     {Cell[2]} \n')
        f.write(f' PRIMCOORD 1 \n')
        f.write(f'{top2+topAtoms_z} 1 \n')

        for line in range(topAtoms_z):
            f.write(f'{topAtoms[line,0]} \t {float(topAtoms[line,1]):.6f} \t {float(topAtoms[line,2]):.6f} \t {rzT[line]:.6f} \n')

        for line in range(top2):
            f.write(f'{xyz[line,0]} \t {float(xyz[line,1]):.6f} \t {float(xyz[line,2]):.6f} \t {rzB[line]:.6f} \n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('input_File', help = "Path to the output File.")

    args = parser.parse_args()

    main()
