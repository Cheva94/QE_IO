#!/usr/bin/python3.10

import numpy as np
import pandas as pd

xyz_base = pd.read_csv('silicaSym.xyz', header=None, delim_whitespace=True).to_numpy()
cellx = float(xyz_base[0, 1])
celly = float(xyz_base[0, 3])
cellz = float(xyz_base[0, 5])
xyz_base= xyz_base[1:, :4]

rz = np.array(xyz_base[:,3]).astype(float)
base = len(rz[rz<7.0])
drag = np.mean(rz[(7.0<rz) & (rz<8.0)])
xyz_base = xyz_base[:base, :]

xyz_alc = pd.read_csv('template.xyz', header=None, delim_whitespace=True).to_numpy()
cellx = float(xyz_alc[0, 1])
celly = float(xyz_alc[0, 3])
cellz = float(xyz_alc[0, 5])
xyz_alc = xyz_alc[1:, :4]

rz = np.array(xyz_alc[:,3]).astype(float)
top = len(rz[rz>4.0])
xyz_alc = xyz_alc[-top:, :]

at = np.array(xyz_alc[:,0])
rx = np.array(xyz_alc[:,1]).astype(float)
ry = np.array(xyz_alc[:,2]).astype(float)
rz = np.array(xyz_alc[:,3]).astype(float)

for i in range(top):
    if rx[i] < 0:
        rx[i] += cellx
    elif rx[i] > cellx:
        rx[i] -= cellx

    if ry[i] < 0:
        ry[i] += celly
    elif ry[i] > celly:
        ry[i] -= celly

if np.min(rx) < 0.00001:
    rx += 0.0001

if np.min(ry) < 0.00001:
    ry += 0.0001

rz += drag - np.min(rz)

xyz_alc = np.vstack((at, rx, ry, rz)).T

with open('movil.xyz', 'w') as f:
    f.write(f'{base+top} \n\n')
    for line in range(top):
        f.write(f'{xyz_alc[line,0]}          {float(xyz_alc[line,1]):.6f}          {float(xyz_alc[line,2]):.6f}          {float(xyz_alc[line,3]):.6f} \n')