#!/usr/bin/python3.10

'''
    Description: extracts QE output data for relax.
    Written by: Ignacio J. Chevallier-Boutell.
    Dated: October, 2021.
'''

import argparse
import re
from pandas import DataFrame
import numpy as np

def main():

    File = args.input_file

    pCell = 'celldm'
    pEtot = 'Final energy    '
    pWall = 'PWSCF        : '
    pCoord = 'ATOMIC_POSITIONS'
    pAtoms = 'number of atoms/cell      ='
    pBFGS = 'number of bfgs steps'

    line_counter = 0
    Bohr2Angs = 0.529177210903
    ry2ev = 13.605693122994017

    Cell, Etot, Wall = [], [], []
    Index, BFGS = [], []
    xyz_init, xyz_end = [], []
        
    with open(File, 'r') as f:
        for line in f.readlines():
            if re.search(pAtoms, line):
                nAt = int(line.split()[-1])
            elif re.search(pCell, line):
                line = line.split()
                alat = float(line[1])
                Cell.append(alat*Bohr2Angs)
                Cell.append(float(line[3])*alat*Bohr2Angs)
                Cell.append(float(line[5])*alat*Bohr2Angs)
            elif re.search(pEtot, line):
                Etot.append(line)
            elif re.search(pWall, line):
                Wall.append(line)
            elif re.search(pBFGS, line):
                BFGS.append(line)

    Etot = float(Etot[-1].split()[3])
    Wall = Wall[0].split()[-2]
    BFGS = len(BFGS) + 1
    
    with open(File, 'r') as f:
        for line in f.readlines():
            line_counter += 1
            if re.search(pCoord, line):
                Index.append(line_counter)

    if BFGS != len(Index):
        print('BFGS no coincide con cantidad de "ATOMIC_POSITIONS"')
        exit()

    with open(File, 'r') as f:
        all = f.read().split('\n')

    with open(f'{File.split(".out")[0]}.xsf', 'w') as f:
        f.write(f'ANIMSTEPS {BFGS}\n')
        f.write(f'CRYSTAL\n')
        f.write(f'PRIMVEC\n')
        f.write(f'\t{Cell[0]:.2f}\t0.00\t0.00\n')
        f.write(f'\t0.00\t{Cell[1]:.2f}\t0.00\n')
        f.write(f'\t0.00\t0.00\t{Cell[2]:.2f}\n')
        for block in range(BFGS):
            f.write(f' PRIMCOORD {block+1}\n')
            f.write(f'{nAt} 1\n')
            for line in range(nAt):
                f.write(f'{all[Index[block]+line]}\n')
    
    idx = Index[-1]
    with open(File, 'r') as f:
        for line in range(nAt):
            xyz_end.append(all[idx+line].split()[:4])

    xyz_end = np.array(xyz_end)
    rzf = xyz_end[:,3].astype(float)

    init = File.split('.out')[0]+'.in'
    line_counter = 0

    with open(init, 'r') as f:
        for line in f.readlines():
            line_counter += 1
            if re.search(pCoord, line):
                idx = line_counter

    with open(init, 'r') as f:
        all = f.read().split('\n')

    with open(init, 'r') as f:
        for line in range(nAt):
            xyz_init.append(all[idx+line].split()[:4])

    xyz_init = np.array(xyz_init)
    rzi = xyz_init[:,3].astype(float)

    with open(f"{File.split('.out')[0]}.dat", 'w') as f:
        f.write('#At, Wall time, Iterations, Etot [Ry], Etot [eV]\n')
        f.write(f'{nAt}, {Wall}, {BFGS}, {Etot:.6f}, {Etot*ry2ev:.6f}\n\n')
        f.write('Dimensiones de celda (Angstrom)\n')
        f.write(f'A = {Cell[0]:.2f}, B = {Cell[1]:.2f}, C = {Cell[2]:.2f}\n\n')
        f.write('Vacío\n')
        f.write('\tCondición inicial\n')
        f.write('\t\tMenor Z [A], Mayor Z [A], Void [A]\n')
        f.write(f'\t\t{np.min(rzi):.2f}, {np.max(rzi):.2f}, {Cell[2]-(np.max(rzi)-np.min(rzi)):.2f}\n')
        f.write('\tCondición final\n')
        f.write('\t\tMenor Z [A], Mayor Z [A], Void [A]\n')
        f.write(f'\t\t{np.min(rzf):.2f}, {np.max(rzf):.2f}, {Cell[2]-(np.max(rzf)-np.min(rzf)):.2f}\n\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('input_file', help = "Path to the output file.")

    args = parser.parse_args()

    main()
