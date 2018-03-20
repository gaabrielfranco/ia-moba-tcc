#!/usr/bin/env python3

import argparse
import numpy as np
from pprint import PrettyPrinter
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


def normalizes(x):
    x_norm = []
    minimum = np.min(x, axis=0)
    maximum = np.max(x, axis=0)
    for i in x:
        x_norm.append((i - minimum) / (maximum - minimum))

    return x_norm, minimum, maximum


def clusterization(data, cluster_list, seed, json_file, verbose):
    output_data = {}

    for attr_set in data.keys():
        output_data[attr_set] = {}
        output_data[attr_set]['n_clusters'] = []
        output_data[attr_set]['inertia'] = []
        for k in cluster_list:
            print('Executing experiment %s with %d clusters...' % (attr_set, k))
            data_norm, min_norm, max_norm = normalizes(data[attr_set])
            km = KMeans(n_clusters=k, random_state=seed, n_jobs=-1)
            km.fit_predict(data_norm)

            # Init data matrix with k lists
            output_data[attr_set]['n_clusters'].append(k)
            output_data[attr_set]['inertia'].append(km.inertia_)

    if verbose:
        print('\n\nOutput data summary:')
        pp = PrettyPrinter(depth=3)
        pp.pprint(output_data)

    data_out = pd.DataFrame(output_data)
    data_out.to_json(json_file)

    print('\nOutput data successfully exported to file %s\n' % json_file)

    return output_data


def read_data(input_file, verbose):
    print('\nReading input data from file %s...' % input_file, end=' ')

    data = {}
    data['all'] = []
    data['kda'] = []
    data['kills'] = []
    data['deaths'] = []
    data['assists'] = []
    data['denies'] = []
    data['gpm'] = []
    data['hd'] = []
    data['hh'] = []
    data['lh'] = []
    data['xpm'] = []
    data['kills-corr'] = []
    data['deaths-corr'] = []
    data['assists-corr'] = []
    data['denies-corr'] = []
    data['gpm-corr'] = []
    data['hd-corr'] = []
    data['hh-corr'] = []
    data['lh-corr'] = []
    data['xpm-corr'] = []

    fp = open(input_file, 'r')

    for l in fp:
        parts = l.strip().split()
        for i, p in enumerate(parts):
            parts[i] = int(p)
        if parts[4] >= 5:
            data['kda'].append(list(np.array(parts[1:4]) / parts[4]))
            data['all'].append(
                list(np.array(parts[1:4] + parts[5:]) / parts[4]))
            data['kills'].append(
                list(np.array([parts[1]]) / parts[4]))
            data['deaths'].append(list(np.array([parts[2]]) / parts[4]))
            data['assists'].append(list(np.array([parts[3]]) / parts[4]))
            data['denies'].append(list(np.array([parts[5]]) / parts[4]))
            data['gpm'].append(list(np.array([parts[6]]) / parts[4]))
            data['hd'].append(list(np.array([parts[7]]) / parts[4]))
            data['hh'].append(list(np.array([parts[8]]) / parts[4]))
            data['lh'].append(list(np.array([parts[9]]) / parts[4]))
            data['xpm'].append(list(np.array([parts[10]]) / parts[4]))
            #K, D, A, Npartidas, denies, gpm, hero_damage, hero_healing, LH, xp_p_min

    fp.close()

    print('done.\n')

    # Mapping the database
    attr_positions = np.array([1, 2, 3, 5, 6, 7, 8, 9, 10])
    matches_position = 4
    attr_names = np.array(['kills', 'deaths', 'assists',
                           'denies', 'gpm', 'hd', 'hh', 'lh', 'xpm'], dtype=str)

    # n least correlated atrributes and minimum matches per player
    n = 4
    min_matches = 5

    # normalizes database and discard maximum and minimum information (underline redirects to "nothing")
    dt, _, _ = normalizes(data['all'])

    # Computes correlation matrix (absolute values)
    corr_matrix = pd.DataFrame(dt).corr().abs().as_matrix()

    # Dynamically maps n least correlated attributes to each attribute
    correlation_map = []
    correlation_map_names = {}

    # Line count
    i = 0
    for attr_line in corr_matrix:
        # Sort indexes of matrix line by its values and get the indexes related to the n smallest values
        sorted_indexes = attr_line.argsort()[:n]

        correlation_map.append(attr_positions[sorted_indexes])
        correlation_map_names[attr_names[i]] = list(attr_names[sorted_indexes])

        i += 1

    fp = open(input_file, 'r')

    for l in fp:
        parts = l.strip().split()
        for i, p in enumerate(parts):
            parts[i] = int(p)
        if parts[matches_position] >= min_matches:
            for i, position in enumerate(attr_positions):
                line = [parts[position]]
                for other in correlation_map[i]:
                    line.append(parts[other])
                    l = list(attr_positions)
                data[attr_names[i] +
                     '-corr'].append(list(np.array(line) / parts[matches_position]))

    fp.close()

    pp = PrettyPrinter()
    if verbose:
        print('Correlation map: ')
        pp.pprint(correlation_map_names)
        print()

    return data, correlation_map, correlation_map_names


def plot_inertia(data, attribute_names, plots_path, show_plots):
     # config output images
    plt.rcParams["figure.figsize"] = (25, 16)
    plt.rcParams['font.size'] = 18.0

    for experiment in data:
        fig, ax = plt.subplots()
        plt.title("Inertia x K - %s" % experiment)
        plt.plot(data[experiment]['n_clusters'], data[experiment]['inertia'])
        file_name = plots_path + experiment + '_k_analysis.png'
        plt.savefig(file_name)
        print('Graph %s saved.' % file_name)
        if show_plots:
            plt.show()
        plt.clf()


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
    input_file = 'files/attributes.txt'
    json_file = 'files/output_k-analysis/output_k_analysis.json'
    cluster_list = list(range(3, 101))

    plots_path = 'files/output_k-analysis/'

    # Run experiments with outliers
    data, correlation_map, correlation_map_names = read_data(
        input_file, verbose)

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
    attribute_names['kills-corr'] = ["kills"]
    attribute_names['deaths-corr'] = ["deaths"]
    attribute_names['assists-corr'] = ["assists"]
    attribute_names['denies-corr'] = ["denies"]
    attribute_names['gpm-corr'] = ["gpm"]
    attribute_names['hd-corr'] = ["hd"]
    attribute_names['hh-corr'] = ["hh"]
    attribute_names['lh-corr'] = ["lh"]
    attribute_names['xpm-corr'] = ["xpm"]

    output_data = clusterization(data, cluster_list, seed, json_file, verbose)
    plot_inertia(output_data, attribute_names, plots_path, show_plots)


if __name__ == "__main__":
    main()
