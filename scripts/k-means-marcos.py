#!/usr/bin/env python3

import numpy as np
from sklearn.cluster import KMeans
import pandas as pd
from pprint import PrettyPrinter
import matplotlib.pyplot as plt

def normalizes(x):
    x_norm = []
    minimum = np.min(x)
    maximum = np.max(x)
    for i in x:
        x_norm.append((i - minimum) / (maximum - minimum))

    return x_norm, minimum, maximum


def un_normalizes(m, minimum, maximum):
    x_un_norm = []
    for i in m:
        x_un_norm.append(i * (maximum - minimum) + minimum)

    return x_un_norm

def prune(data, c):
    arrData = np.array(data)
    
    shp = arrData.shape
    
    remove = [False] * len(data)
    
    for i in range(shp[1]):
        dt = arrData[:,i]
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
            data['kdlh'].append(list(np.array([parts[1]] + [parts[5]] + [parts[9]]) / parts[4]))
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

def clusterization(data, cluster_list, seed, json_file, verbose):
    output_data = {}

    for attr_set in data.keys():
        for k in cluster_list:
            print('Executing experiment with %s attributes and %d clusters...' % (attr_set, k))
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
            output_data[experiment]['centroids'] = un_normalizes(km.cluster_centers_, min_norm, max_norm)
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
                plot_data.append(cluster[:,i])
                labels.append('Cluster %d' % (n+1))
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
    
    fig, ax = plt.subplots()
    
    plot_data = []
    labels = []
    
    for experiment in data.keys():
        labels.append(experiment)
        plot_data.append(data[experiment]['inertia'])
        
    groups = np.arange(len(data.keys()))
    width = 0.35
        
    plt.bar(groups, plot_data, width, tick_label=labels)
    plt.savefig(file_name)
    print('\nGraph %s saved.' % file_name)
    if show_plots:
        plt.show()
    plt.clf()
    
def plot_counts(data, plots_path, show_plots):
    # config output images
    plt.rcParams["figure.figsize"] = (25, 16)
    
    for experiment in data.keys():
        fig, ax = plt.subplots()
        plot_data = []
        labels = []
        i = 1
        for c in data[experiment]['clusters']:
            plot_data.append(len(c))
            labels.append(i)
            i += 1
        plt.pie(plot_data, labels=labels)
        file_name = plots_path + experiment + '_pie.png'
        plt.savefig(file_name)
        print('\nGraph %s saved.' % file_name)
        if show_plots:
            plt.show()
        plt.clf()

def main():
    # configuration parameters, to be changed to command line parameters later...
    seed = 0
    input_file = 'files/attributes.txt'
    json_file = 'files/output_k-means/output_kmeans_marcos.json'
    #json_file_pruned = 'files/output_k-means/output_kmeans_pruned_marcos.json'
    cluster_list = [3, 4, 5]
    verbose = True
    show_plots = False
    plots_path = 'files/output_plots/'
 
    # Run experiments with outliers
    data = read_data(input_file)
    
    output_data = clusterization(data, cluster_list, seed, json_file, verbose)
    
    # Plot results
    attribute_names = {}
    attribute_names['kda'] = ["kills", "deaths", "assists"]
    attribute_names['all'] = ["kills", "deaths", "assists", "denies", "lh"]
    attribute_names['kdlh'] = ["kills", "denies", "lh"]
    attribute_names['everyone'] = ["kills", "deaths", "assists", "denies", "gpm", "hd", "hh", "lh", "xpm"]
    attribute_names['5best'] = ["kills", "gpm", "hd", "lh", "xpm"]
    attribute_names['2best'] = ["kills", "hd"]
    attribute_names['best'] = ["hd"]
    attribute_names['wtf'] = ["kills", "gpm", "lh", "xpm"]
    attribute_names['wohd'] = ["kills", "deaths", "assists", "denies", "gpm", "hh", "lh", "xpm"]
    plot_clusters(output_data, attribute_names, plots_path, show_plots)
    
    plot_inertia(output_data, plots_path + 'inertia.png', show_plots)
    plot_counts(output_data, plots_path, show_plots)
    
    """
    # Run same experiments without outliers
    pruned_data = outlier_removal(data)
    
    output_pruned_data = clusterization(pruned_data, cluster_list, seed, json_file_pruned, verbose)
    
    # Plot results
    attribute_names = {}
    attribute_names['kda-wo'] = ["kills", "deaths", "assists"]
    attribute_names['all-wo'] = ["kills", "deaths", "assists", "denies", "lh"]
    attribute_names['kdlh-wo'] = ["kills", "denies", "lh"]
    plot_clusters(output_pruned_data, attribute_names, plots_path, show_plots)
    
    plot_inertia(output_pruned_data, plots_path + 'inertia-wo.png', show_plots)
    """

if __name__ == "__main__":
    main()
