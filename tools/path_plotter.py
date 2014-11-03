#!/usr/bin/env python


import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tk
from math import atan2, asin
from numpy import rad2deg



def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")



if __name__ == "__main__":
    ##########################################################################
    # args
    parser = argparse.ArgumentParser(description='PLots paths from CSV files with pose information')
    parser.register('type', 'bool', str2bool)
    parser.add_argument('-i', metavar='INPUT_FILES', type=str, required=True, help='CSV input files')
    parser.add_argument('-o', metavar='OUTPUT_FILE_NAME', type=str, required=False, default='results', help='Output file name (exports in svg, eps and png)')
    parser.add_argument('-p', metavar='FILE_POSITION_START_COLUNM', type=int, required=False, default=1, help='CSV data column where the arrows position starts')
    parser.add_argument('-v', metavar='FILE_VECTOR_START_COLUNM', type=int, required=False, default=8, help='CSV data column where the arrows vector starts')
    parser.add_argument('-a', metavar='ARROW_SCALE', type=float, required=False, default=0.0025, help='Arrow scale')
    parser.add_argument('-c', metavar='ARROWS_COLORS', type=str, required=False, default='g+b', help='Arrows colors for each file')
    parser.add_argument('-t', metavar='GRAPH_TITLE', type=str, required=False, default='Paths', help='Graph title')
    parser.add_argument('-s', metavar='SAVE_GRAPH', type='bool', required=False, default=True, help='Save graphs to files using the name prefix specified with -o')
    parser.add_argument('-d', metavar='DISPLAY_GRAPH', type='bool', required=False, default=False, help='Show graph')
    args = parser.parse_args()



    ##########################################################################
    # graph setup
    fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=100)

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(args.t)

    plt.minorticks_on()
#     plt.grid(b=True, which='major', color='k', linestyle='--', linewidth=0.3, alpha=0.7)
#     plt.grid(b=True, which='minor', color='k', linestyle='--', linewidth=0.1, alpha=0.7)
    majorLocator = tk.MultipleLocator(1.0)
    minorLocator = tk.MultipleLocator(0.25)
    ax.xaxis.set_major_locator(majorLocator)
    ax.xaxis.set_minor_locator(minorLocator)

    x_min = 0
    x_max = 0
    y_min = 0
    y_max = 0

    ##########################################################################
    # path plotting
    file_names = args.i.split('+')
    arrow_colors = args.c.split('+')
    
    for idx, file in enumerate(file_names):
        arrow_positions_x = np.loadtxt(file, dtype=float, delimiter=' ', skiprows=2, usecols=(args.p,))
        arrow_positions_y = np.loadtxt(file, dtype=float, delimiter=' ', skiprows=2, usecols=(args.p + 1,))
        arrow_directions_x = np.loadtxt(file, dtype=float, delimiter=' ', skiprows=2, usecols=(args.v,))
        arrow_directions_y = np.loadtxt(file, dtype=float, delimiter=' ', skiprows=2, usecols=(args.v + 1,))
        number_arrows = min(len(arrow_positions_x), len(arrow_positions_y), len(arrow_directions_x), len(arrow_directions_y))

        x_min = np.min([np.min(arrow_positions_x), x_min])
        x_max = np.max([np.max(arrow_positions_x), x_max])
        y_min = np.min([np.min(arrow_positions_y), y_min])
        y_max = np.max([np.max(arrow_positions_y), y_max])

        print file, number_arrows

        for i in range(0, number_arrows):
#             print arrow_positions_x[i], arrow_positions_y[i], arrow_directions_x[i], arrow_directions_y[i]

            ax.arrow(arrow_positions_x[i], arrow_positions_y[i], arrow_directions_x[i] * args.a, arrow_directions_y[i] * args.a,
                     shape='full', width=0.0002, linewidth=0.0002, length_includes_head=True, head_width=0.0006, head_length=0.001, color=arrow_colors[idx])

#             ax.annotate(str(i), fontsize=0.1,
#                         xy=(arrow_positions_x[i] + arrow_directions_x[i] * args.a, arrow_positions_y[i] + arrow_directions_y[i] * args.a),
#                         xytext=(arrow_positions_x[i], arrow_positions_y[i]),
# #                         arrowprops=dict(arrowstyle="->", linewidth=0.05, color=arrow_colors[idx])
#                         arrowprops=dict(width=0.05, headwidth=0.15, frac=0.3, linewidth=0.05, color=arrow_colors[idx])
#                         )

#             ax.text(arrow_positions_x[i], arrow_positions_y[i], str(i),
#                     ha="left", va="center", rotation=rad2deg(asin(arrow_directions_y[i])), size=0.1,
#                     bbox=dict(boxstyle="rarrow,pad=0.05", color=arrow_colors[idx], lw=0.05, alpha=0.2, width=0.1, mutation_scale=0.1, mutation_aspect=1.0))

    plt.axis('tight')
    axlim = list(plt.axis())
    axlim[0] = x_min - abs(x_min * 0.1)
    axlim[1] = x_max + abs(x_max * 0.1)
    axlim[2] = y_min - abs(y_min * 0.1)
    axlim[3] = y_max + abs(y_max * 0.1)
    plt.axis(axlim)
    plt.draw()



    ##########################################################################
    # output
    if args.s:
        plt.savefig('%s.svg' % args.o)
        plt.savefig('%s.eps' % args.o)
        plt.savefig('%s.pdf' % args.o)
        plt.savefig('%s.png' % args.o, dpi=1000, bbox_inches='tight')

    if args.d:
        plt.show()

    exit(0)
