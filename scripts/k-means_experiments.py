#!/usr/bin/env python3
import argparse
from modules.clusters import clusterization
from modules.data import read_data, normalizes, de_normalize
from modules.plots import plot_inertia, plot_counts, plot_clusters, plot_silhouette_score


def main():

    verbose = False
    show_plots = False
    pruned = False
    corr = False
    exp_all = False

    # Parse args
    parser = argparse.ArgumentParser(
        description='Run experiments using k-means', prog="k-means_experiments.py")
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='print the outputs on the terminal (defaut = False)')
    parser.add_argument('--show', '-s', action='store_true',
                        help='shows the plots (defaut = False)')
    parser.add_argument('--not-all', '-na', action='store_true',
                        help='execute the experiments without all data (defaut = False)')
    parser.add_argument('--pruned', '-p', action='store_true',
                        help='execute the experiments with pruned data (defaut = False)')
    parser.add_argument('--corr', '-c', action='store_true',
                        help='execute the experiments with correlation analysis (defaut = False)')
    parser.add_argument('--k-int', '-k', nargs='*', type=int,
                        default=[3, 4, 5], help='Define the parameter k with a integer list. Example: --k-int 3 4 5 10. (defaut = 3 4 5)')
    parser.add_argument('--k-str', '-ks', nargs='*', type=str,
                        default='', help='Define the parameter k with a string. Example: --k-str \'list(range(1, 5))\'')

    args = parser.parse_args()
    verbose = args.verbose
    show_plots = args.show
    pruned = args.pruned
    corr = args.corr
    exp_all = args.not_all

    if args.k_str == '':
        cluster_list = args.k_int
    else:
        cluster_list = eval(args.k_str[0])

    # configuration parameters
    seed = 0
    input_file = 'files/attributes.txt'
    json_file = 'files/output_k-means_experiments/data/output_kmeans.json'
    json_file_corr = 'files/output_k-means_experiments/data_corr/output_kmeans_corr.json'
    json_file_pruned = 'files/output_k-means_experiments/data_pruned/output_kmeans_pruned.json'

    plots_path = 'files/output_k-means_experiments/data/'
    plots_path_corr = 'files/output_k-means_experiments/data_corr/'
    plots_path_pruned = 'files/output_k-means_experiments/data_pruned/'

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

    if not(exp_all):
        # Run experiments with outliers
        data = read_data()
        output_data = clusterization(
            data, cluster_list, seed, json_file, verbose)
        plot_inertia(output_data, plots_path +
                     'inertia.png', cluster_list, show_plots)
        plot_silhouette_score(output_data, plots_path +
                              'silhouette_score.png', cluster_list, show_plots)
        plot_clusters(output_data, attribute_names, plots_path, show_plots)
        plot_counts(output_data, cluster_list, plots_path, show_plots)

    del attribute_names['kda']
    del attribute_names['all']

    if corr:
        # Run same experiments with corr data
        data_corr = read_data('corr')

        output_corr_data = clusterization(
            data_corr, cluster_list, seed, json_file_corr, verbose)

        keys = list(attribute_names.keys())
        for i in keys:
            attribute_names[i + '-corr'] = [i]
            del attribute_names[i]

        plot_clusters(output_corr_data, attribute_names,
                      plots_path_corr, show_plots)
        plot_inertia(output_corr_data, plots_path_corr +
                     'inertia-corr.png', cluster_list, show_plots)
        plot_silhouette_score(output_corr_data, plots_path_corr +
                              'silhouette_score-corr.png', cluster_list, show_plots)
        plot_counts(output_corr_data, cluster_list,
                    plots_path_corr, show_plots)

    if pruned:
        # Run same experiments without outliers
        pruned_data = read_data('pruned')

        output_pruned_data = clusterization(
            pruned_data, cluster_list, seed, json_file_pruned, verbose)

        # Plot results
        attribute_names = {}
        attribute_names['kda-wo'] = ["kills", "deaths", "assists"]
        attribute_names['all-wo'] = ["kills", "deaths",
                                     "assists", "denies", "gpm", "hd", "hh", "lh", "xpm"]
        attribute_names['kills-wo'] = ["kills"]
        attribute_names['deaths-wo'] = ["deaths"]
        attribute_names['assists-wo'] = ["assists"]
        attribute_names['denies-wo'] = ["denies"]
        attribute_names['gpm-wo'] = ["gpm"]
        attribute_names['hd-wo'] = ["hd"]
        attribute_names['hh-wo'] = ["hh"]
        attribute_names['lh-wo'] = ["lh"]
        attribute_names['xpm-wo'] = ["xpm"]
        plot_clusters(output_pruned_data, attribute_names,
                      plots_path_pruned, show_plots, True)
        plot_inertia(output_pruned_data, plots_path_pruned +
                     'inertia-wo.png', cluster_list, show_plots)
        plot_silhouette_score(output_pruned_data, plots_path_pruned +
                              'silhouette_score-wo.png', cluster_list, show_plots)
        plot_counts(output_pruned_data, cluster_list,
                    plots_path_pruned, show_plots)


if __name__ == "__main__":
    main()
