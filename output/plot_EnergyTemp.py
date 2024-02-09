#!/usr/bin/python3.10

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from cycler import cycler
import argparse
from matplotlib.ticker import MultipleLocator
from scipy.ndimage import gaussian_filter1d

plt.rcParams["font.weight"] = "bold"
plt.rcParams["font.size"] = 25

plt.rcParams["axes.labelweight"] = "bold"
plt.rcParams["axes.linewidth"] = 3
plt.rcParams["axes.prop_cycle"] = cycler('color', ['tab:orange', 'mediumseagreen', 'm', 'y', 'k'])

plt.rcParams['xtick.major.size'] = 10
plt.rcParams['xtick.major.width'] = 3
plt.rcParams['ytick.major.size'] = 10
plt.rcParams['ytick.major.width'] = 3

plt.rcParams['xtick.minor.size'] = 5
plt.rcParams['xtick.minor.width'] = 1.5
plt.rcParams['ytick.minor.size'] = 5
plt.rcParams['ytick.minor.width'] = 1.5

plt.rcParams["legend.loc"] = 'best'
plt.rcParams["legend.frameon"] = True
plt.rcParams["legend.fancybox"] = True
plt.rcParams["legend.fontsize"] = 30
plt.rcParams["legend.edgecolor"] = 'black'

plt.rcParams["figure.figsize"] = 25, 10
plt.rcParams["figure.autolayout"] = True

plt.rcParams["lines.linewidth"] = 1
plt.rcParams["lines.markersize"] = 20
plt.rcParams["lines.linestyle"] = ':'

def main():
    file = args.input_file
    left = args.x_axis[0]
    right = args.x_axis[1]
    bottomE = args.y_axisE[0]
    topE = args.y_axisE[1]
    bottomT = args.y_axisT[0]
    topT = args.y_axisT[1]

    ry2ev = 13.605693122994017

    x = pd.read_csv(file).iloc[:, 0].to_numpy()
    yT = pd.read_csv(file).iloc[:, 1]
    yTs = gaussian_filter1d(yT, sigma=30)

    yE = pd.read_csv(file).iloc[:, 2]
    yE *= ry2ev
    maxE = np.max(yE)
    print(f'Máxima energía: {maxE} eV')
    print(f'Tiempo simulado: {x[-1]} ps')
    yE -= maxE
    yEs = gaussian_filter1d(yE, sigma=30)

    
    _, ax = plt.subplots(1, 2)

    ### TEMPERATURE
    ax[0].plot(x, yT, ls='-')
    ax[0].plot(x, yTs, c='black', lw=3, ls='-')
    ax[0].set_xlabel('time [ps]')
    ax[0].set_ylabel('Temperature [K]')
    if (left != None) and (right != None):
        ax[0].set_xlim(float(left), float(right))
    if (bottomT != None) and (topT != None):
        ax[0].set_ylim(float(bottomT), float(topT))

    ### ENERGY
    ax[1].plot(x, yE, ls='-')
    ax[1].plot(x, yEs, c='black', lw=3, ls='-')
    ax[1].set_xlabel('time [ps]')
    ax[1].set_ylabel('Ekin + Etot [eV]')
    if (left != None) and (right != None):
        ax[1].set_xlim(float(left), float(right))
    if (bottomE != None) and (topE != None):
        ax[1].set_ylim(float(bottomE), float(topE))

    plt.savefig(f'{file.split(".csv")[0]}.png')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('input_file', help = "Path to the csv file.")

    parser.add_argument('-x', '--x_axis', nargs = 2, default = [None, None],
                        help = "Choose range for X axis for both temperature and energy.")

    parser.add_argument('-yE', '--y_axisE', nargs = 2, default = [None, None],
                        help = "Choose range for Y axis on energy plot.")

    parser.add_argument('-yT', '--y_axisT', nargs = 2, default = [None, None],
                        help = "Choose range for Y axis on temperature plot.")

    args = parser.parse_args()

    main()
