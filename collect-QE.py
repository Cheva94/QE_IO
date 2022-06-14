#!/usr/bin/python3.10

'''
    Description: extracts QE output data for scf, relax or dynamics calculations.
                It also extracts coordinates from the dynamics.
    Written by: Ignacio J. Chevallier-Boutell.
    Dated: October, 2021.
'''

import argparse
import re
from pandas import DataFrame

def main():

    F = args.input_file

    if args.dynamics:
        dt = 0.0004837761 # ps
        # dt = 0.0005 # ps
        pTemp = 'temperature           ='
        pEnergy = 'const'

        for file in F:
            Temp, Energy = [], []

            with open(file, 'r') as f:
                for line in f.readlines():
                    if re.search(pTemp, line):
                        Temp.append(line)
                    if re.search(pEnergy, line):
                        Energy.append(line)

            Temp = [line.split()[2] for line in Temp]
            Energy = [line.split()[5] for line in Energy]
            Time = [(x+1)*dt for x in range(len(Temp))]

            df = DataFrame({'Time [ps]':Time, 'Temperature [K]':Temp, 'Ekin + Etot [Ry]':Energy})
            df.to_csv(f"{file.split('.out')[0]}.csv", sep=',', index=False)

    elif args.pwo2xsf:
        pAtoms = 'number of atoms/cell      ='
        pCoord = 'ATOMIC_POSITIONS'
        pCell = 'celldm'
        nAt, line_counter = 0, 0
        all, Index, Coords = [], [], []
        Cell = []
        Bohr2Angs = 0.529177210903


        for file in F:
            with open(file, 'r') as f:
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

            with open(file, 'r') as f:
                for line in f.readlines():
                    line_counter += 1
                    if re.search(pCoord, line):
                        Index.append(line_counter)

            with open(file, 'r') as f:
                all = f.read().split('\n')

            with open(f'{file.split(".out")[0]}.xsf', 'w') as f:
                f.write(f'ANIMSTEPS {len(Index)} \n')
                f.write(f'CRYSTAL \n')
                f.write(f'PRIMVEC \n')
                f.write(f'    {Cell[0]}    0.0     0.0 \n')
                f.write(f'    0.0    {Cell[1]}     0.0 \n')
                f.write(f'    0.0    0.0     {Cell[2]} \n')
                for block in range(len(Index)):
                    f.write(f' PRIMCOORD {block+1} \n')
                    f.write(f'{nAt} 1 \n')
                    for line in range(nAt):
                        f.write(f'{all[Index[block]+line]} \n')

    else:
        pEtot = '!    total energy'
        pST = 'smearing contrib'
        pSmearing = 'smearing,'

        for file in F:
            if args.solvent:
                Etot = []
                with open(file, 'r') as f:
                    for line in f.readlines():
                        if re.search(pEtot, line):
                            Etot.append(line)

                Etot = [Etot[-1].split()[4]]

                df = DataFrame({'Etot [Ry]':Etot})
                df.to_csv(f"{file.split('.out')[0]}.csv", sep=',', index=False)

            else:
                Etot, ST, Smearing = [], [], []
                with open(file, 'r') as f:
                    for line in f.readlines():
                        if re.search(pEtot, line):
                            Etot.append(line)
                        if re.search(pST, line):
                            ST.append(line)
                        if re.search(pSmearing, line):
                            Smearing.append(line)

                Etot = [Etot[-1].split()[4]]
                ST = [ST[-1].split()[4]]
                SmearType = [Smearing[-1].split()[5]]
                Degauss = [Smearing[-1].split()[-1]]

                df = DataFrame({'Smearing':SmearType, 'Degauss [Ry]':Degauss, 'Etot [Ry]':Etot, 'ST [Ry]':ST})
                df['TS/Etot [%]'] = df.apply(lambda row: 100 * float(row['ST [Ry]']) / float(row['Etot [Ry]']), axis=1)
                df.to_csv(f"{file.split('.out')[0]}.csv", sep=',', index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('input_file', nargs = '+', help = "Path to the output file.")

    parser.add_argument('-dyn', '--dynamics', action = 'store_true', help = "Extracts time, temperature and energy from dynamics.")

    parser.add_argument('-o2a', '--pwo2xsf', action = 'store_true', help = "Extracts coordinates from dynamics.")

    parser.add_argument('-ste', '--solvent', action = 'store_true', help = "Just solvent. No smearing.")

    args = parser.parse_args()

    main()
