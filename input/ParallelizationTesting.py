#!/usr/bin/python3.10

import argparse

def main():

    capa = args.CapaxAtomos
    itElec = args.itElec
    diag = args.diagonalParallelization

    batchingNames = []

    if diag == None:
        nodes = [2, 3, 4]
        OMP = [64, 32, 16, 8, 4, 2, 1]

        for n in nodes:
            MPI = [x for x in reversed(OMP)]

            for i in range(len(MPI)):
                fileName = f'Short-{capa}_n-{n}_MPI-{MPI[i]}_OMP-{OMP[i]}.sh'
                batchingNames.append(fileName)

                with open(fileName, 'w') as f:
                    f.write('#!/bin/bash \n\n')

                    f.write(f"#SBATCH --job-name={capa}-{n}-{MPI[i]}-{OMP[i]} \n\n")

                    f.write('#SBATCH --partition=short \n')
                    f.write('#SBATCH --time=00-01:00 \n\n')

                    f.write(f'#SBATCH --nodes={n} \n')
                    f.write(f'#SBATCH --ntasks-per-node={MPI[i]} \n')
                    f.write('#SBATCH --cpus-per-task=1 \n\n')

                    f.write('source /etc/profile \n')
                    f.write('module load quantum-espresso/6.7 \n')
                    f.write(f'export OMP_NUM_THREADS={OMP[i]} \n\n')

                    f.write(f'srun pw.x -inp TestDyn_{capa}_{itElec}.in >> TestDyn_{capa}_{itElec}_n-{n}_MPI-{MPI[i]}_OMP-{OMP[i]}.out \n')

        with open('multiBatch.sh', 'w') as f:
            for n in range(len(batchingNames)):
                f.write(f"sbatch {batchingNames[n]} && ")

    else:
        N = args.Nodes_MPI_OMP[0]
        M = args.Nodes_MPI_OMP[1]
        O = args.Nodes_MPI_OMP[2]
        Y = args.matrix

        for k in Y:
            fileName = f'Short-{capa}_n-{N}_MPI-{M}_OMP-{O}_nDiag-{k}.sh'
            batchingNames.append(fileName)

            with open(fileName, 'w') as f:
                f.write('#!/bin/bash \n\n')

                f.write(f"#SBATCH --job-name={capa}-diag-{k} \n\n")

                f.write('#SBATCH --partition=short \n')
                f.write('#SBATCH --time=00-01:00 \n\n')

                f.write(f'#SBATCH --nodes={N} \n')
                f.write(f'#SBATCH --ntasks-per-node={M} \n')
                f.write('#SBATCH --cpus-per-task=1 \n\n')

                f.write('source /etc/profile \n')
                f.write('module load quantum-espresso/6.7 \n')
                f.write(f'export OMP_NUM_THREADS={O} \n\n')

                f.write(f'srun pw.x -ndiag {k} -inp TestDyn_{capa}_{itElec}.in >> TestDyn_{capa}_{itElec}_n-{N}_MPI-{M}_OMP-{O}_nDiag-{k}.out \n')

        with open(f'multiBatch_n-{N}.sh', 'w') as f:
            for n in range(len(batchingNames)):
                f.write(f"sbatch {batchingNames[n]} && ")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('CapaxAtomos')

    parser.add_argument('itElec', type=int)

    parser.add_argument('-diag', "--diagonalParallelization", action='store_true')

    parser.add_argument('-NMO', "--Nodes_MPI_OMP", nargs=3, type=int)

    parser.add_argument('-Y', "--matrix", type = int, nargs = '+')

    args = parser.parse_args()

    main()
