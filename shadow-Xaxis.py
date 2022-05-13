#!/usr/bin/python3.10

'''
    Description: Representación gráfica de el conjunto solución para una inecuación.
		 Mejoras y debug en https://github.com/Cheva94/misc/blob/master/shadow-Xaxis.py
    Written by: Ignacio J. Chevallier-Boutell.
    Dated: November, 2021.
'''

import argparse
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import AutoMinorLocator
from cycler import cycler
from matplotlib.patches import Rectangle, Circle

plt.rcParams["font.weight"] = "bold"
plt.rcParams["font.size"] = 35

plt.rcParams["axes.labelweight"] = "bold"
plt.rcParams["axes.linewidth"] = 5
plt.rcParams["axes.spines.left"] = False
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False

plt.rcParams['xtick.major.size'] = 10
plt.rcParams['xtick.major.width'] = 5

plt.rcParams["figure.figsize"] = 12, 12
plt.rcParams["figure.autolayout"] = True

def main():

    xlim = args.xlim
    xsol = args.xsol
    include = args.include

    fig, ax = plt.subplots()

    shadow=Rectangle((xsol[0],-3), np.abs(xsol[1]-xsol[0]), 6, fc='tab:orange', alpha=0.5, clip_on=False, zorder=1)
    ax.add_patch(shadow)

    if include == 'left':
        circleL = Circle((xsol[0], 0), radius=1, ec='tab:orange', fc='tab:orange', clip_on=True, zorder=5)
        circleR = Circle((xsol[1], 0), radius=1, ec='tab:orange', fc='white', lw=5, clip_on=True, zorder=5)

        ax.add_patch(circleL)
        ax.add_patch(circleR)

        ax.annotate(xsol[0], (xsol[0], 0), xytext=(xsol[0]-2, 4), zorder=10)
        ax.annotate(xsol[1], (xsol[1], 0), xytext=(xsol[1], 4), zorder=10)

    elif include == 'right':
        circleL = Circle((xsol[0], 0), radius=1, ec='tab:orange', fc='white', lw=5, clip_on=True, zorder=5)
        circleR = Circle((xsol[1], 0), radius=1, ec='tab:orange', fc='tab:orange', clip_on=True, zorder=5)

        ax.add_patch(circleL)
        ax.add_patch(circleR)

        ax.annotate(xsol[0], (xsol[0], 0), xytext=(xsol[0], 4), zorder=10)
        ax.annotate(xsol[1], (xsol[1], 0), xytext=(xsol[1]-2, 4), zorder=10)

    elif include == 'both':
        circleL = Circle((xsol[0], 0), radius=1, ec='tab:orange', fc='tab:orange', clip_on=True, zorder=5)
        circleR = Circle((xsol[1], 0), radius=1, ec='tab:orange', fc='tab:orange', clip_on=True, zorder=5)

        ax.add_patch(circleL)
        ax.add_patch(circleR)

        ax.annotate(xsol[0], (xsol[0], 0), xytext=(xsol[0]-2, 4), zorder=10)
        ax.annotate(xsol[1], (xsol[1], 0), xytext=(xsol[1]-2, 4), zorder=10)

    elif include == 'none':
        circleL = Circle((xsol[0], 0), radius=1, ec='tab:orange', fc='white', lw=5, clip_on=True, zorder=5)
        circleR = Circle((xsol[1], 0), radius=1, ec='tab:orange', fc='white', lw=5, clip_on=True, zorder=5)

        ax.add_patch(circleL)
        ax.add_patch(circleR)

        ax.annotate(xsol[0], (xsol[0], 0), xytext=(xsol[0], 4), zorder=10)
        ax.annotate(xsol[1], (xsol[1], 0), xytext=(xsol[1], 4), zorder=10)

    else:
        print('Elegir alguna de las opciones: left, right, both o none para indicar el relleno de los círculos para inclusión.')

    ax.yaxis.set_visible(False)
    ax.spines['bottom'].set_position('center')
    ax.set_xlim(xlim[0], xlim[1])
    ax.set_xlabel('x', loc='right')
    ax.set_aspect('equal')
    ax.arrow(xlim[1], -0.001, 1, 0, width=0.18, color="k", head_width=1, head_length=1, clip_on=False)

    plt.savefig('shadow-Xaxis')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser = argparse.ArgumentParser(description='Representación gráfica de el conjunto solución para una inecuación.')

    parser.add_argument('xlim', help = "Valores mínimo y máximo para plotear el eje x.", nargs = 2, type=int)

    parser.add_argument('xsol', help = "Valores mínimo y máximo de la solución. Si es -inf, escribir un valor menor al mínimo de xlim. Si es +inf, escribir un valor mayor al máximo de xlim.", nargs = 2, type=float)

    parser.add_argument('include', help = 'Indicar si debe rellenar el círculo de la izquierda (left), de la derecha (right), ambos (both) o ninguno (none).')

    parser.add_argument('-o', '--output', help = "Path for the output file.")

    args = parser.parse_args()

    main()
