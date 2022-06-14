#!/usr/bin/python3.10

import numpy as np
import pandas as pd
import argparse
import matplotlib.pyplot as plt
from cycler import cycler

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
plt.rcParams["legend.fontsize"] = 20
plt.rcParams["legend.edgecolor"] = 'black'

plt.rcParams["figure.figsize"] = 12.5, 10
plt.rcParams["figure.autolayout"] = True

plt.rcParams["lines.linewidth"] = 4
plt.rcParams["lines.markersize"] = 8
# plt.rcParams["lines.linestyle"] = ':'

def main():

    bohr2angs = 0.529177210903
    ry2ev = 13.605693122994017

    file = args.input_file
    data =  pd.read_csv(f"{file}", delim_whitespace = True).to_numpy()

    fig, axf = plt.subplots()

    axf.axhline(0, c = 'black', lw = 3, ls = ':')
    axf.plot(data[:, 0] * bohr2angs, data[:, 1] * ry2ev)# / bohr2angs)
    axf.set_xlabel('Z [A]')
    axf.set_ylabel('E [eV]')

    plt.savefig(f'{file.split(".dat")[0]}.png')

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('input_file', help = "Path to the csv file.")

    args = parser.parse_args()

    main()
