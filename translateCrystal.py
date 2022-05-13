#!/usr/bin/python3.10

import argparse
from pandas import read_csv
import numpy as np

def main():
    F = args.input_file
    X = args.moveAlongX
    Y = args.moveAlongY
    Z = args.moveAlongZ
    output_file = f"{F.split('.xsf', 1)[0]}-X_{X}-Y_{Y}-Z_{Z}"

    with open(f'{F}','r') as orig, open(f'{output_file}.xsf','w') as dest:
        for line in orig.readlines()[:6]:
                dest.write(line)

    xsf = read_csv(F, header = None, delim_whitespace = True,
                    names=['idAt', 'rx', 'ry', 'rz', 'fx', 'fy', 'fz'])
    nAtTot = int(xsf.iloc[7,0])
    rows = nAtTot + 2
    xyz = xsf.iloc[8:,0:4].reset_index(drop=True).to_numpy()
    at = np.array(xyz[:,0])
    rx = np.array(xyz[:,1]).astype(float)
    ry = np.array(xyz[:,2]).astype(float)
    rz = np.array(xyz[:,3]).astype(float)

    if X != None:
        rx += X

    if Y != None:
        ry += Y

    if Z != None:
        rz += Z

    xyz = np.vstack((at, rx, ry, rz)).T

    with open(f'{output_file}.xsf','a') as f:
        f.write(' PRIMCOORD 1 \n')
        f.write(f'{nAtTot} 1 \n')
        for line in range(nAtTot):
            f.write(f'{xyz[line,0]} \t {float(xyz[line,1]):.6f} \t {float(xyz[line,2]):.6f} \t {float(xyz[line,3]):.6f} \n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('input_file', help = "Path to the xsf input file.")

    parser.add_argument('-X', '--moveAlongX', type = float)
    parser.add_argument('-Y', '--moveAlongY', type = float)
    parser.add_argument('-Z', '--moveAlongZ', type = float)

    args = parser.parse_args()

    main()
