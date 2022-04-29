#!/usr/bin/python3.9

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from cycler import cycler
import argparse

plt.rcParams["font.weight"] = "bold"
plt.rcParams["font.size"] = 35

plt.rcParams["axes.labelweight"] = "bold"
plt.rcParams["axes.linewidth"] = 3
plt.rcParams["axes.prop_cycle"] = cycler('color', ['tab:orange', 'mediumseagreen', 'm', 'y', 'k'])

plt.rcParams['xtick.major.size'] = 10
plt.rcParams['xtick.major.width'] = 3
plt.rcParams['ytick.major.size'] = 10
plt.rcParams['ytick.major.width'] = 3

plt.rcParams["legend.loc"] = 'best'
plt.rcParams["legend.frameon"] = True
plt.rcParams["legend.fancybox"] = True
plt.rcParams["legend.fontsize"] = 30
plt.rcParams["legend.edgecolor"] = 'black'

plt.rcParams["figure.figsize"] = 12.5, 10
plt.rcParams["figure.autolayout"] = True

plt.rcParams["lines.linewidth"] = 1
plt.rcParams["lines.markersize"] = 20
plt.rcParams["lines.linestyle"] = ':'

def main():
    file = args.input_file
    left = args.x_axis[0]
    right = args.x_axis[1]
    bottom = args.y_axis[0]
    top = args.y_axis[1]

    fig, ax = plt.subplots()

    ax.plot(pd.read_csv(file).iloc[:, 0], pd.read_csv(file).iloc[:, 1], ls='-')

    ax.set_xlabel('time [ps]')
    ax.set_ylabel('Temperature [K]')
    if (left != None) and (right != None):
        ax.set_xlim(float(left), float(right))

    plt.savefig('Temp-vs-time')

    fig, ax = plt.subplots()

    m = np.max(pd.read_csv(file).iloc[:, 2])
    ax.plot(pd.read_csv(file).iloc[:, 0], pd.read_csv(file).iloc[:, 2] - m, ls='-')

    ax.set_xlabel('time [ps]')
    ax.set_ylabel('Energy [Ry]')
    if (left != None) and (right != None):
        ax.set_xlim(float(left), float(right))
    if (bottom != None) and (top != None):
        ax.set_ylim(float(bottom), float(top))

    plt.savefig('Energy-vs-time')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('input_file', help = "Path to the csv file.")

    parser.add_argument('-x', '--x_axis', nargs = 2, default = [None, None],
                        help = "Choose range for X axis.")

    parser.add_argument('-y', '--y_axis', nargs = 2, default = [None, None],
                        help = "Choose range for Y axis.")

    args = parser.parse_args()

    main()
