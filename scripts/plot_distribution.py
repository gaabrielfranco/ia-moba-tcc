#!/usr/bin/env python3

import modules.plots as plt
from modules.data import read_data
import argparse


def main():
    show_plots = False

    parser = argparse.ArgumentParser(
        description='Plot the attributes distribution', prog="plot_distribution.py")
    parser.add_argument('--show', '-s', action='store_true',
                        help='shows the plots (defaut = False)')
    parser.add_argument('--norm', '-n', action='store_true',
                        help='normalize plots (defaut = False)')
    parser.add_argument('--with_outliers', '-wo', action='store_true',
                        help='plot with outliers (defaut = False)')

    args = parser.parse_args()
    show_plots = args.show
    norm = args.norm
    with_outliers = args.with_outliers

    plots_path = ('files/output_plot_distribution/without_outliers/' if not(with_outliers)
                  else 'files/output_plot_distribution/with_outliers/')

    if with_outliers:
        data = read_data()
    else:
        data = read_data('pruned')

    attribute_names = {}
    attribute_names['kills'] = ["kills"]
    attribute_names['deaths'] = ["deaths"]
    attribute_names['assists'] = ["assists"]
    attribute_names['denies'] = ["denies"]
    attribute_names['gpm'] = ["gpm"]
    attribute_names['hd'] = ["hd"]
    attribute_names['hh'] = ["hh"]
    attribute_names['lh'] = ["lh"]
    attribute_names['xpm'] = ["xpm"]

    plt.plot_distributions(data, attribute_names, plots_path, show_plots, norm)
    plt.plot_all_distributions(
        data, attribute_names, plots_path, show_plots, norm)
    plt.plot_all_sep_distributions(
        data, attribute_names, plots_path, show_plots, norm)


if __name__ == "__main__":
    main()
