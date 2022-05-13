#!/usr/local/bin/python3.10

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from cycler import cycler
# from matplotlib.ticker import FormatStrFormatter # para determinar decimales en los ejes
# Ejemplo con 2 decimales: ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
# import matplotlib.ticker as mtick # permite hacer ejes con porcentajes
# from mpl_toolkits.mplot3d import Axes3D # gráficos 3D

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

plt.rcParams["lines.linewidth"] = 4
plt.rcParams["lines.markersize"] = 20
plt.rcParams["lines.linestyle"] = ':'

def main():

    fig, ax = plt.subplots()

    ax.plot([1,2,3], [5,6,7], marker='^', label='s')
    # ax.bar(x, height, width, label=, yerr = , capsize=8, error_kw = {'elinewidth':5 , 'capthick':2})
    # ax.errorbar(x, y, yerr = , capsize = 15, marker = '^', ls = 'None', ms = 20, label = )
    # ax.axhline(y, c = , lw = 4, ls = '-')
    # ax.hlines(y=0.6, xmin=0.0, xmax=1.0, color='b')
    # ax.axvline(x, c = , lw = 4, ls = '-')
    # ax.vlines(y=0.6, xmin=0.0, xmax=1.0, color='b')

    ax.set_xlabel('x')
    ax.set_ylabel('y')

    # plt.annotate(TEXT, (X_POSITION, Y_POSITION), ...
    # plt.axhspan(Y_START, Y_END, ...)  #horizontal shading
    # plt.axvspan(X_START, X_END, ...)  #vertical shading
    # ax.fill_between([0, 10.56], 2.4, 7.1, color='black', alpha=0.1, zorder=1)

    # plt.gca().spines['top'].set_visible(False)
    # plt.gca().spines['right'].set_visible(False)

    # ax.set_xlim(left=, right=)
    # ax.set_ylim(bottom=, top=)

    # ax.set_xticks(x)
    # ax.set_xticklabels(x, rotation=25, ha='center')

    # ax.text(0.98,0.98, 'n-alkanes', ha='right', va='top', transform=ax.transAxes)
    # ax.legend()#ncol=, bbox_to_anchor=(, ))
    # ax.set_title()

    # plt.savefig()

    plt.show()

if __name__ == "__main__":
    main()
