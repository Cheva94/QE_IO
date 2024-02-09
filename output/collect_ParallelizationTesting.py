#!/usr/bin/python3.10

import argparse
import re
from linecache import getline

def main():

    F = args.input_file

    pDiag = "per band group will be used"
    pSticks = "Parallelization info"
    pKS = "number of Kohn-Sham states"
    pFFT = "Dense  grid:"
    pmaxIt = "iteration #"
    pWALL = "PWSCF        :"

    output = f'{F[0].split("_n-")[0]}-RESULTS.csv'

    with open(output, 'w') as O:
        O.write(f"Nodes, MPI, OMP, Subgroups/Band, Subgroup Size, Sticks Tot, Sticks Min, Sticks Max, Sticks Ratio, KS States, FFT dense (z), FFT smooth (z), Max It, WALL [s] \n")

        for file in F:
            fileName = file.split("_n-")[1].split(".out")[0]
            nodes = int(fileName.split("_MPI-")[0])
            MPI = int(fileName.split("_MPI-")[1].split("_OMP-")[0])
            OMP = int(fileName.split("_OMP-")[1].split("_nDiag-")[0])
            maxIt = []

            with open(file, 'r') as f:
                for ind, line in enumerate(f,1):
                    if re.search(pDiag, line):
                        diag = getline(f.name, ind).split("sub-group")[0].strip()
                        diagSize = getline(f.name, ind+1).split("size of sub-group:")[1].split("procs")[0].strip()

                    if re.search(pSticks, line):
                        sticksMin = getline(f.name, ind+3).split()[3]
                        sticksMax = getline(f.name, ind+4).split()[3]
                        sticksTot = int(getline(f.name, ind+5).split()[3])

                        sticksRatio = int(sticksTot / (nodes * MPI))

                    if re.search(pKS, line):
                        KS = getline(f.name, ind).split()[-1]

                    if re.search(pFFT, line):
                        FFTd = getline(f.name, ind).split()[-1].split(")")[0]
                        FFTs = getline(f.name, ind+2).split()[-1].split(")")[0]

                    if re.search(pWALL, line):
                        WALL = getline(f.name, ind).split("CPU")[1].split("WALL")[0].strip()
                        M = int(WALL.split('m')[0])
                        S = float(WALL.split('m')[1].split("s")[0])
                        WALL = 60 * M + S

                    if re.search(pmaxIt, line):
                        maxIt.append(getline(f.name, ind))

            maxIt = int(maxIt[-1].split("ecut=")[0].split("iteration #")[1].strip())
            O.write(f"{nodes}, {MPI}, {OMP}, {diag}, {diagSize}, {sticksTot}, {sticksMin}, {sticksMax}, {sticksRatio}, {KS}, {FFTd}, {FFTs}, {maxIt}, {WALL:.6f} \n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('input_file', nargs = '+', help = "Path to the input file.")

    args = parser.parse_args()

    main()
