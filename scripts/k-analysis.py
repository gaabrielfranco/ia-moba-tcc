#!/usr/bin/env python3

import argparse
from modules.clusters import clusterization_k_analysis
from modules.data import read_data
from modules.plots import plot_k_analysis


def main():
    verbose = False
    show_plots = False
    # Parse args
    parser = argparse.ArgumentParser(
        description='Run experiments using k-means', prog="k-means_experiments.py")
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='print the outputs on the terminal (defaut = False)')
    parser.add_argument('--show', '-s', action='store_true',
                        help='shows the graphics (defaut = False)')

    args = parser.parse_args()

    verbose = args.verbose
    show_plots = args.show

    # configuration parameters
    seed = 0
    json_file = 'files/output_k-analysis/output_k_analysis.json'
    cluster_list = list(range(3, 101))

    plots_path = 'files/output_k-analysis/'

    data = read_data('pruned')
    data_corr = read_data('corr')

    # Plot results
    attribute_names = {}
    attribute_names['kda'] = ["kills", "deaths", "assists"]
    attribute_names['all'] = ["kills", "deaths",
                              "assists", "denies", "gpm", "hd", "hh", "lh", "xpm"]
    attribute_names['kills'] = ["kills"]
    attribute_names['deaths'] = ["deaths"]
    attribute_names['assists'] = ["assists"]
    attribute_names['denies'] = ["denies"]
    attribute_names['gpm'] = ["gpm"]
    attribute_names['hd'] = ["hd"]
    attribute_names['hh'] = ["hh"]
    attribute_names['lh'] = ["lh"]
    attribute_names['xpm'] = ["xpm"]
    attribute_names_corr = {}
    attribute_names_corr['kills-corr'] = ["kills"]
    attribute_names_corr['deaths-corr'] = ["deaths"]
    attribute_names_corr['assists-corr'] = ["assists"]
    attribute_names_corr['denies-corr'] = ["denies"]
    attribute_names_corr['gpm-corr'] = ["gpm"]
    attribute_names_corr['hd-corr'] = ["hd"]
    attribute_names_corr['hh-corr'] = ["hh"]
    attribute_names_corr['lh-corr'] = ["lh"]
    attribute_names_corr['xpm-corr'] = ["xpm"]

    output_data = clusterization_k_analysis(
        data, cluster_list, seed, json_file, verbose)
    plot_k_analysis(output_data, attribute_names, plots_path, show_plots)

    output_data = clusterization_k_analysis(
        data_corr, cluster_list, seed, json_file, verbose)
    plot_k_analysis(output_data, attribute_names, plots_path, show_plots)


if __name__ == "__main__":
    main()
