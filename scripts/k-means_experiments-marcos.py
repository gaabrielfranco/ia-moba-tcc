#!/usr/bin/env python3

import numpy as np
from sklearn.cluster import KMeans
import pandas as pd
from pprint import PrettyPrinter
import matplotlib.pyplot as plt
import sys
import argparse

'''
    TODO: análise de correlação
'''


def normalizes(x):
    x_norm = []
    minimum = np.min(x, axis=0)
    maximum = np.max(x, axis=0)
    for i in x:
        x_norm.append((i - minimum) / (maximum - minimum))

    return x_norm, minimum, maximum


def de_normalize(m, minimum, maximum):
    x_de_norm = []

    for i in m:
        x_de_norm.append(i * (maximum - minimum) + minimum)

    return x_de_norm


def prune(data, c):
    arrData = np.array(data)

    shp = arrData.shape

    remove = [False] * len(data)

    for i in range(shp[1]):
        dt = arrData[:, i]
        avg = np.average(dt)
        std = np.std(dt)
        pos = 0
        for d in dt:
            if np.abs(avg - d) > c * std:
                remove[pos] = True
            pos += 1

    output = []
    for i, r in enumerate(remove):
        if not r:
            output.append(data[i])

    return output


def outlier_removal(data, c=2.0):
    pruned_data = {}
    print()
    for experiment in data.keys():
        print('Pruning outliers from %s...' % experiment)
        pruned_data[experiment + '-wo'] = prune(data[experiment], c)

    return pruned_data


def read_data(input_file, corr):
    print('\nReading input data from file %s...' % input_file, end=' ')

    data = {}
    data_corr = {}
    data['all'] = []
    data['kda'] = []
    data['kdlh'] = []
    data['everyone'] = []
    data['5best'] = []
    data['2best'] = []
    data['best'] = []
    data['wtf'] = []
    data['wohd'] = []
    data['kills'] = []
    data['deaths'] = []
    data['assists'] = []
    data['denies'] = []
    data['gpm'] = []
    data['hd'] = []
    data['hh'] = []
    data['lh'] = []
    data['xpm'] = []
    if corr:
        data_corr['kills-corr'] = []
        data_corr['deaths-corr'] = []
        data_corr['assists-corr'] = []
        data_corr['denies-corr'] = []
        data_corr['gpm-corr'] = []
        data_corr['hd-corr'] = []
        data_corr['hh-corr'] = []
        data_corr['lh-corr'] = []
        data_corr['xpm-corr'] = []

    fp = open(input_file, 'r')

    for l in fp:
        parts = l.strip().split()
        for i, p in enumerate(parts):
            parts[i] = int(p)
        if parts[4] >= 5:
            data['all'].append(
                list(np.array(parts[1:4] + [parts[5]] + [parts[9]]) / parts[4]))
            data['kda'].append(list(np.array(parts[1:4]) / parts[4]))
            data['kdlh'].append(
                list(np.array([parts[1]] + [parts[5]] + [parts[9]]) / parts[4]))
            data['everyone'].append(
                list(np.array(parts[1:4] + parts[5:]) / parts[4]))
            data['5best'].append(
                list(np.array([parts[1]] + parts[6:8] + parts[9:]) / parts[4]))
            data['2best'].append(
                list(np.array([parts[1]] + [parts[7]]) / parts[4]))
            data['best'].append(
                list(np.array([parts[7]]) / parts[4]))
            data['wtf'].append(
                list(np.array([parts[1]] + [parts[6]] + parts[9:]) / parts[4]))
            data['wohd'].append(
                list(np.array(parts[1:4] + parts[5:7] + parts[8:]) / parts[4]))
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
            if corr:
                data_corr['kills-corr'].append(list(np.array([parts[1]] +
                                                             [parts[3]] + [parts[2]] + [parts[8]] + [parts[6]]) / parts[4]))
                data_corr['deaths-corr'].append(
                    list(np.array([parts[2]] + [parts[8]] + [parts[7]] + [parts[6]] + [parts[3]]) / parts[4]))
                data_corr['assists-corr'].append(
                    list(np.array([parts[3]] + [parts[1]] + [parts[6]] + [parts[9]] + [parts[10]]) / parts[4]))
                data_corr['denies-corr'].append(
                    list(np.array([parts[5]] + [parts[3]] + [parts[6]] + [parts[8]] + [parts[2]]) / parts[4]))
                data_corr['gpm-corr'].append(list(np.array([parts[6]] + [parts[3]] + [
                    parts[8]] + [parts[2]] + [parts[5]]) / parts[4]))
                data_corr['hd-corr'].append(list(np.array([parts[7]] + [parts[2]] +
                                                          [parts[8]] + [parts[3]] + [parts[6]]) / parts[4]))
                data_corr['hh-corr'].append(list(np.array([parts[8]] + [parts[2]] +
                                                          [parts[6]] + [parts[7]] + [parts[10]]) / parts[4]))
                data_corr['lh-corr'].append(list(np.array([parts[9]] + [parts[3]] + [
                    parts[2]] + [parts[8]] + [parts[6]]) / parts[4]))
                data_corr['xpm-corr'].append(list(np.array([parts[10]] + [parts[3]] + [
                    parts[8]] + [parts[2]] + [parts[6]]) / parts[4]))

    fp.close()

    print('done.\n')

    return data, data_corr


def clusterization(data, cluster_list, seed, json_file, verbose):
    output_data = {}

    for attr_set in data.keys():
        for k in cluster_list:
            print('Executing experiment with %s attributes and %d clusters...' % (
                attr_set, k))
            data_norm, min_norm, max_norm = normalizes(data[attr_set])
            km = KMeans(n_clusters=k, random_state=seed, n_jobs=-1)
            labels = km.fit_predict(data_norm)

            experiment = attr_set + '_' + str(k)
            output_data[experiment] = {}

            # Init data matrix with k lists
            output_data[experiment]['clusters'] = []
            for i in range(k):
                output_data[experiment]['clusters'].append([])

            # Assign each individual from the database to its corresponding cluster
            for i, instance in enumerate(data[attr_set]):
                output_data[experiment]['clusters'][labels[i]].append(instance)

            output_data[experiment]['inertia'] = km.inertia_
            output_data[experiment]['centroids'] = de_normalize(
                km.cluster_centers_, min_norm, max_norm)
            output_data[experiment]['seed'] = seed

    if verbose:
        print('\n\nOutput data summary:')
        pp = PrettyPrinter(depth=3)
        pp.pprint(output_data)

    data_out = pd.DataFrame(output_data)
    data_out.to_json(json_file)

    print('\nOutput data successfully exported to file %s\n' % json_file)

    return output_data


def plot_clusters(data, attribute_names, plots_path, show_plots):
    # config output images
    plt.rcParams["figure.figsize"] = (25, 16)
    plt.rcParams['font.size'] = 18.0

    fig, ax = plt.subplots()

    for experiment in data.keys():
        experiment_type = experiment.split('_')[0]
        for i, attr in enumerate(attribute_names[experiment_type]):
            plt.title('Experiment: %s - attribute: %s' % (experiment, attr))

            plot_data = []
            labels = []
            n = 0
            for cluster in data[experiment]['clusters']:
                cluster = np.array(cluster)
                plot_data.append(cluster[:, i])
                labels.append('Cluster %d' % (n + 1))
                n += 1

            plt.boxplot(plot_data, False, '', labels=labels)
            plot_file = plots_path + experiment + '_' + attr + '.png'
            plt.savefig(plot_file)
            print('Graph %s saved.' % plot_file)
            if show_plots:
                plt.show()
            plt.clf()


def plot_inertia(data, file_name, show_plots):
    # config output images
    plt.rcParams["figure.figsize"] = (25, 16)
    plt.rcParams['font.size'] = 18.0

    fig, ax = plt.subplots()

    plot_data = []
    labels = []
    colors = []

    data_sorted = sorted(data.items(), key=lambda x: str(x[0]))

    for iteration, (experiment, value) in enumerate(data_sorted):
        labels.append(experiment)
        plot_data.append(value['inertia'])
        if iteration % 3 == 0:
            colors.append('blue')
        elif iteration % 3 == 1:
            colors.append('red')
        else:
            colors.append('black')

    groups = np.arange(len(data.keys()))
    width = 0.35

    plt.bar(groups, plot_data, width, tick_label=labels, color=colors)
    plt.xticks(groups, labels, rotation=90)
    plt.title("Inertia for each experiment")
    plt.savefig(file_name)
    print('Graph %s saved.' % file_name)
    if show_plots:
        plt.show()
    plt.clf()


def plot_counts(data, cluster_list, plots_path, show_plots):
    # config output images
    plt.rcParams["figure.figsize"] = (25, 16)
    plt.rcParams['font.size'] = 18.0

    titles = {}

    for experiment in data.keys():
        titles[experiment.split('_')[0]] = "Clusters with the experiment \"" + experiment.split('_')[0] + \
            "\" running the k-means for k = " + str(cluster_list)

    data_sorted = sorted(data.items(), key=lambda x: x[0])

    for iteration, (experiment, value) in enumerate(data_sorted):
        plot_data = []
        labels = []
        i = 1
        for c in value['clusters']:
            plot_data.append(len(c))
            labels.append('Cluster ' + str(i))
            i += 1
        if iteration % 3 == 0:
            fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
            ax1.pie(plot_data, autopct='%1.1f%%')
            ax1.axis('equal')
        elif iteration % 3 == 1:
            ax2.pie(plot_data, autopct='%1.1f%%')
            ax2.axis('equal')
        else:
            ax3.pie(plot_data, autopct='%1.1f%%')
            ax3.axis('equal')
            ax3.legend(labels, loc="lower right")
            file_name = plots_path + experiment.split('_')[0] + '_pie.png'
            plt.suptitle(titles[experiment.split('_')[0]], fontsize=20)
            plt.legend(loc="lower right")
            plt.savefig(file_name)
            print('Graph %s saved.' % file_name)
            if show_plots:
                plt.show()
            plt.clf()


def correlation_analysis(data, attributes):
    output_data = {}
    for i, attr in enumerate(attributes):
        output_data[attr] = []
        for d in data:
            output_data[attr].append(float(d[i]))

    df = pd.DataFrame(output_data)
    df = df.corr()

    experiments = {}
    for i in df.axes[0]:
        experiments[i] = []

    for column in df:
        df_sorted = df.applymap(lambda x: abs(x))
        df_sorted = df_sorted.sort_values(by=column, ascending=True)
        for index, value in enumerate(df_sorted[column][:4]):
            experiments[column].append(df_sorted.axes[0][index])

    return experiments


def main():
    verbose = False
    show_plots = False
    pruned = False
    corr = True

    # Parse args
    parser = argparse.ArgumentParser(
        description='Run experiments using k-means', prog="k-means_experiments.py")
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='print the outputs on the terminal (defaut = False)')
    parser.add_argument('--show', '-s', action='store_true',
                        help='shows the graphics (defaut = False)')
    parser.add_argument('--pruned', '-p', action='store_true',
                        help='execute the experiments with pruned data (defaut = False)')
    parser.add_argument('--corr', '-c', action='store_true',
                        help='execute the experiments with correlation analysis (defaut = False)')

    args = parser.parse_args()

    verbose = args.verbose
    show_plots = args.show
    pruned = args.pruned
    corr = args.corr

    # configuration parameters
    seed = 0
    input_file = 'files/attributes.txt'
    json_file = 'files/output_k-means_experiments/output_kmeans.json'
    json_file_corr = 'files/output_k-means_experiments/output_kmeans_corr.json'
    json_file_pruned = 'files/output_k-means_experiments/output_kmeans_pruned.json'
    cluster_list = [3, 4, 5]

    plots_path = 'files/output_k-means_experiments/'

    # Run experiments with outliers
    data, data_corr = read_data(input_file, corr)

    #output_data = clusterization(data, cluster_list, seed, json_file, verbose)

    # Plot results
    attribute_names = {}
    attribute_names['kda'] = ["kills", "deaths", "assists"]
    attribute_names['all'] = ["kills", "deaths", "assists", "denies", "lh"]
    attribute_names['kdlh'] = ["kills", "denies", "lh"]
    attribute_names['everyone'] = ["kills", "deaths",
                                   "assists", "denies", "gpm", "hd", "hh", "lh", "xpm"]
    attribute_names['5best'] = ["kills", "gpm", "hd", "lh", "xpm"]
    attribute_names['2best'] = ["kills", "hd"]
    attribute_names['best'] = ["hd"]
    attribute_names['wtf'] = ["kills", "gpm", "lh", "xpm"]
    attribute_names['wohd'] = ["kills", "deaths",
                               "assists", "denies", "gpm", "hh", "lh", "xpm"]
    attribute_names['kills'] = ["kills"]
    attribute_names['deaths'] = ["deaths"]
    attribute_names['assists'] = ["assists"]
    attribute_names['denies'] = ["denies"]
    attribute_names['gpm'] = ["gpm"]
    attribute_names['hd'] = ["hd"]
    attribute_names['hh'] = ["hh"]
    attribute_names['lh'] = ["lh"]
    attribute_names['xpm'] = ["xpm"]

    #plot_clusters(output_data, attribute_names, plots_path, show_plots)
    #plot_inertia(output_data, plots_path + 'inertia.png', show_plots)
    #plot_counts(output_data, cluster_list, plots_path, show_plots)

    if corr:
        experiments = correlation_analysis(
            data['everyone'], attribute_names['everyone'])

        output_data = clusterization(
            data_corr, cluster_list, seed, json_file_corr, verbose)

        attribute_names = {}

        for i in experiments.keys():
            attribute_names[i + '-corr'] = experiments[i]
            attribute_names[i + '-corr'].insert(0, i)

        plot_clusters(output_data, attribute_names, plots_path, show_plots)
        plot_inertia(output_data, plots_path + 'inertia-corr.png', show_plots)
        plot_counts(output_data, cluster_list, plots_path, show_plots)

    if pruned:
        # Run same experiments without outliers
        pruned_data = outlier_removal(data)

        output_pruned_data = clusterization(
            pruned_data, cluster_list, seed, json_file_pruned, verbose)

        # Plot results
        attribute_names = {}
        attribute_names['kda-wo'] = ["kills", "deaths", "assists"]
        attribute_names['all-wo'] = ["kills",
                                     "deaths", "assists", "denies", "lh"]
        attribute_names['kdlh-wo'] = ["kills", "denies", "lh"]
        attribute_names['everyone-wo'] = ["kills", "deaths",
                                          "assists", "denies", "gpm", "hd", "hh", "lh", "xpm"]
        attribute_names['5best-wo'] = ["kills", "gpm", "hd", "lh", "xpm"]
        attribute_names['2best-wo'] = ["kills", "hd"]
        attribute_names['best-wo'] = ["hd"]
        attribute_names['wtf-wo'] = ["kills", "gpm", "lh", "xpm"]
        attribute_names['wohd-wo'] = ["kills", "deaths",
                                      "assists", "denies", "gpm", "hh", "lh", "xpm"]
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
                      plots_path, show_plots)

        plot_inertia(output_pruned_data, plots_path +
                     'inertia-wo.png', show_plots)
        plot_counts(output_pruned_data, cluster_list, plots_path, show_plots)


if __name__ == "__main__":
    main()
