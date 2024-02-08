#!/usr/bin/python3.10

'''
    Description: extracts QE output data for scf.
    Written by: Ignacio J. Chevallier-Boutell.
    Dated: October, 2021.
'''

import argparse
import re
from pandas import DataFrame

def main():

    File = args.input_file

    pEtot = '!    total energy'
    pWall = 'PWSCF        : '
    pAtoms = 'number of atoms/cell      ='
    pCell = 'celldm'
    
    Bohr2Angs = 0.529177210903
    ry2ev = 13.605693122994017

    Cell, Etot, Wall = [], [], []

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

    Etot = float(Etot[-1].split()[4])
    Wall = Wall[0].split()[-2]

    with open(f"{File.split('.out')[0]}.dat", 'w') as f:
        f.write('#At, Wall time, Etot [Ry], Etot/#At [Ry/at], Etot [eV], Etot/#At [eV/at]\n')
        f.write(f'{nAt}, {Wall}, {Etot:.6f}, {Etot/nAt:.6f}, {Etot*ry2ev:.6f}, {Etot*ry2ev/nAt:.6f}\n\n')
        f.write(f'Cell dimensions (Angstrom)\n')
        f.write(f'A = {Cell[0]:.2f}, B = {Cell[1]:.2f}, C = {Cell[2]:.2f}')
        

    # df = DataFrame({'Wall time':Wall, 'Etot [Ry]':Etot, 'Etot [eV]':float(Etot)*ry2ev})
    # df.to_csv(f"{File.split('.out')[0]}.dat", sep=',', index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('input_file', help = "Path to the output file.")

    args = parser.parse_args()

    main()
