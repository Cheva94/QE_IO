#!/usr/bin/python3.10

import argparse
import re
from pandas import read_csv
import numpy as np

def main():

    File = args.input_File

    pAtoms = 'number of atoms/cell      ='
    pCoord = 'ATOMIC_POSITIONS'
    pCell = 'celldm'
    nAt, line_counter = 0, 0
    all, idx = [], []
    Cell, xyz = [], []
    Bohr2Angs = 0.529177210903

    with open(File, 'r') as f:
        for line in f.readlines():
            if re.search(pAtoms, line):
                nAt = int(line.split()[-1])
            if re.search(pCell, line):
                line = line.split()
                alat = float(line[1])
                Cell.append(alat*Bohr2Angs)
                Cell.append(float(line[3])*alat*Bohr2Angs)
                Cell.append(float(line[5])*alat*Bohr2Angs)
                break
    Cell = np.round(Cell,2)

    with open(File, 'r') as f:
        for line in f.readlines():
            line_counter += 1
            if re.search(pCoord, line):
                idx.append(line_counter)
    idx = idx[-1]

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

    topAtoms_z = len(rz[rz>7.9])
    topAtoms = xyz[-topAtoms_z:, :]
    bottomO_z = len(rz[rz<1.0])
    O_avgH = np.mean(rz[rz<1.0])
    bottomO = xyz[bottomO_z:, :]

    rzT = np.array(topAtoms[:,3]).astype(float)
    rzT *= -1
    sup = np.max(rzT)
    rzT += O_avgH - sup
    inf = np.min(rzT)
    rzT += 0.0001 - inf
    
    rzB = np.array(bottomO[:,3]).astype(float)
    rzB += O_avgH + 0.0001 - inf

    with open(f'{File.split(".")[0]}.xsf', 'w') as f:
        f.write(f'ANIMSTEPS 1 \n')
        f.write(f'CRYSTAL \n')
        f.write(f'PRIMVEC \n')
        f.write(f'    {Cell[0]}    0.0     0.0 \n')
        f.write(f'    0.0    {Cell[1]}     0.0 \n')
        f.write(f'    0.0    0.0     {Cell[2]} \n')
        f.write(f' PRIMCOORD 1 \n')
        f.write(f'{nAt+topAtoms_z-bottomO_z} 1 \n')

        for line in range(topAtoms_z):
            f.write(f'{topAtoms[line,0]} \t {float(topAtoms[line,1]):.6f} \t {float(topAtoms[line,2]):.6f} \t {rzT[line]:.6f} \n')

        for line in range(nAt-bottomO_z):
            f.write(f'{bottomO[line,0]} \t {float(bottomO[line,1]):.6f} \t {float(bottomO[line,2]):.6f} \t {rzB[line]:.6f} \n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('input_File', help = "Path to the output File.")

    args = parser.parse_args()

    main()
