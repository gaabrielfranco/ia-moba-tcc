#!/usr/bin/env python3

import numpy as np
from sklearn.cluster import SpectralClustering
import pandas as pd
from pprint import PrettyPrinter
import matplotlib.pyplot as plt
import sys
import os


def normalizes(x):
    x_norm = []
    minimum = np.min(x)
    maximum = np.max(x)
    for i in x:
        x_norm.append(list((i - minimum) / (maximum - minimum)))

    print("min e max = ", np.min(x_norm), np.max(x_norm), "\n")
    return x_norm, minimum, maximum


def un_normalizes(m, minimum, maximum):
    x_un_norm = []
    for i in m:
        x_un_norm.append(list(np.array(i) * (maximum - minimum) + minimum))

    return x_un_norm


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


def read_data(input_file):
    print('\nReading input data from file %s...' % input_file, end=' ')

    data = {}
    data['all'] = []
    data['kda'] = []
    data['kdlh'] = []
    data['everyone'] = []
    data['5best'] = []
    data['2best'] = []
    data['best'] = []
    data['wtf'] = []
    data['wohd'] = []

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

    fp.close()

    print('done.\n')

    return data

def get_centroids(labels, data, k):
    data_centroids = [[] for x in range(k)]

    for i, content in enumerate(labels):
        data_centroids[content].append(data[i])

    centroids = [[] for x in range(k)]

    for i, content in enumerate(data_centroids):
        centroids[i] = np.average(content, axis=0)

    return centroids
    
def get_inertia(labels, centroids, data):
    inertia = 0.0

    #inertia: Sum of squared distances of samples to their closest cluster center.
    for i, content in enumerate(labels):
        for j in range(len(data[i])):
            inertia += (data[i][j] - centroids[content][j]) ** 2

    return inertia
        

def clusterization(data, cluster_list, seed, json_file, verbose):
    output_data = {}

    for attr_set in data.keys():
        for k in cluster_list:
            print('Executing experiment with %s attributes and %d clusters...' % (
                attr_set, k))

            data_norm, min_norm, max_norm = normalizes(data[attr_set])

            km = SpectralClustering(n_clusters=k, random_state=seed, n_jobs=-1)
            try:
                labels = km.fit_predict(data_norm)
            except ValueError as e:
                print("erro bizarro...")
                print(e)

            experiment = attr_set + '_' + str(k)
            output_data[experiment] = {}

            # Init data matrix with k lists
            output_data[experiment]['clusters'] = []
            for i in range(k):
                output_data[experiment]['clusters'].append([])

            # Assign each individual from the database to its corresponding cluster
            for i, instance in enumerate(data[attr_set]):
                output_data[experiment]['clusters'][labels[i]].append(instance)

            data_unnorm = un_normalizes(data_norm, min_norm, max_norm)

            output_data[experiment]['centroids'] = get_centroids(labels, data_unnorm, k)
            output_data[experiment]['inertia'] = get_inertia(labels, get_centroids(labels, data_norm, k), data_norm)
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

    for iteration, experiment in enumerate(data.keys()):
        labels.append(experiment)
        plot_data.append(data[experiment]['inertia'])
        if iteration % 3 == 0:
            colors.append('blue')
        elif iteration % 3 == 1:
            colors.append('red')
        else:
            colors.append('black')

    groups = np.arange(len(data.keys()))
    width = 0.35

    plt.bar(groups, plot_data, width, tick_label=labels, color=colors)
    plt.xticks(groups, labels, rotation=45)
    plt.title("Inertia for each experiment")
    plt.savefig(file_name)
    print('Graph %s saved.' % file_name)
    if show_plots:
        plt.show()
    plt.clf()


def plot_counts(data, plots_path, show_plots):
    # config output images
    plt.rcParams["figure.figsize"] = (25, 16)
    plt.rcParams['font.size'] = 18.0

    titles = {
        "all": "Clusters with the experiment \"all\" running the spectral clustering for k = [3, 4, 5]",
        "kda": "Clusters with the experiment \"kda\" running the spectral clustering for k = [3, 4, 5]",
        "kdlh": "Clusters with the experiment \"kdlh\" running the spectral clustering for k = [3, 4, 5]",
        "everyone": "Clusters with the experiment \"everyone\" running the spectral clustering for k = [3, 4, 5]",
        "5best": "Clusters with the experiment \"5best\" running the spectral clustering for k = [3, 4, 5]",
        "2best": "Clusters with the experiment \"2best\" running the spectral clustering for k = [3, 4, 5]",
        "best": "Clusters with the experiment \"best\" running the spectral clustering for k = [3, 4, 5]",
        "wtf": "Clusters with the experiment \"wtf\" running the spectral clustering for k = [3, 4, 5]",
        "wohd": "Clusters with the experiment \"wohd\" running the spectral clustering for k = [3, 4, 5]"
    }

    for iteration, experiment in enumerate(data.keys()):
        plot_data = []
        labels = []
        i = 1
        for c in data[experiment]['clusters']:
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

def main():
    verbose = False
    show_plots = False
    pruned = False

    for i in range(1, len(sys.argv)):
        if sys.argv[1] == "--help":
            print('Opções:\n')
            print("--verbose: printa os arquivos em tela (defaut = False)")
            print("--show: mostra o graficos em tela em tela (defaut = False)")
            print(
                "--pruned: executa o experimento para os dados podados também (defaut = False)")
            print("--help: mostra o menu de ajuda")
            return
        if sys.argv[i] == "--verbose":
            verbose = True
        if sys.argv[i] == "--show":
            show_plots = True
        if sys.argv[1] == "--pruned":
            pruned = True

    # configuration parameters, to be changed to command line parameters later...
    seed = 0
    input_file = 'files/attributes.txt'
    json_file = 'files/output_spectral-clustering_experiments/output_spectral-clustering.json'
    json_file_pruned = 'files/output_spectral-clustering_experiments/output_spectral-clustering_pruned.json'
    cluster_list = [3, 4, 5]

    plots_path = 'files/output_spectral-clustering_experiments/'

    # Run experiments with outliers
    data = read_data(input_file)

    output_data = clusterization(data, cluster_list, seed, json_file, verbose)

    # Plot results
    attribute_names = {}
    attribute_names['all'] = ["kills", "deaths", "assists", "denies", "lh"]
    attribute_names['kda'] = ["kills", "deaths", "assists"]
    attribute_names['kdlh'] = ["kills", "denies", "lh"]
    attribute_names['everyone'] = ["kills", "deaths",
                                   "assists", "denies", "gpm", "hd", "hh", "lh", "xpm"]
    attribute_names['5best'] = ["kills", "gpm", "hd", "lh", "xpm"]
    attribute_names['2best'] = ["kills", "hd"]
    attribute_names['best'] = ["hd"]
    attribute_names['wtf'] = ["kills", "gpm", "lh", "xpm"]
    attribute_names['wohd'] = ["kills", "deaths",
                               "assists", "denies", "gpm", "hh", "lh", "xpm"]
    
    plot_clusters(output_data, attribute_names, plots_path, show_plots)

    plot_inertia(output_data, plots_path + 'inertia.png', show_plots)
    plot_counts(output_data, plots_path, show_plots)

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
        plot_clusters(output_pruned_data, attribute_names,
                      plots_path, show_plots)

        plot_inertia(output_pruned_data, plots_path +
                     'inertia-wo.png', show_plots)


if __name__ == "__main__":
    main()
