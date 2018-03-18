#!/usr/bin/env python3

# https://seaborn.pydata.org/tutorial/distributions.html

import numpy as np
import seaborn as sns
import argparse
import matplotlib.pyplot as plt
import pandas as pd


def normalizes(x):
    x_norm = []
    minimum = np.min(x, axis=0)
    maximum = np.max(x, axis=0)
    for i in x:
        x_norm.append((i - minimum) / (maximum - minimum))

    return x_norm


def read_data(input_file):
    print('\nReading input data from file %s...' % input_file, end=' ')

    data = {}
    data_corr = {}
    data['kills'] = []
    data['deaths'] = []
    data['assists'] = []
    data['denies'] = []
    data['gpm'] = []
    data['hd'] = []
    data['hh'] = []
    data['lh'] = []
    data['xpm'] = []

    fp = open(input_file, 'r')

    for l in fp:
        parts = l.strip().split()
        for i, p in enumerate(parts):
            parts[i] = int(p)
        if parts[4] >= 5:
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
            # K, D, A, Npartidas, denies, gpm, hero_damage, hero_healing, LH, xp_p_min

    fp.close()

    print('done.\n')

    return data


def plot_distributions(data, attribute_names, plots_path, show_plots):
    # config output images
    plt.rcParams["figure.figsize"] = (25, 16)
    plt.rcParams['font.size'] = 18.0

    for attr in attribute_names:
        ax = sns.distplot(normalizes(data[attr]))
        plt.suptitle(
            attr + ' norm distribution', fontsize=20)
        file_name = plots_path + attr + '_dist_norm.png'
        plt.savefig(file_name)
        print('Graph %s saved.' % file_name)
        if show_plots:
            plt.show()
        plt.clf()

        ax = sns.distplot(normalizes(data[attr]))
        plt.suptitle(attr + ' distribution', fontsize=20)
        file_name = plots_path + attr + '_dist.png'
        plt.savefig(file_name)
        print('Graph %s saved.' % file_name)
        if show_plots:
            plt.show()
        plt.clf()


def plot_all_sep_distributions(data, attribute_names, plots_path, show_plots):
    # config output images
    plt.rcParams["figure.figsize"] = (25, 16)
    plt.rcParams['font.size'] = 18

    f, axarr = plt.subplots(3, 3)

    i = 0
    j = 0

    for attr in attribute_names:
        sns.distplot(normalizes(data[attr]), ax=axarr[i, j])
        axarr[i, j].set_title(attr + ' distribution')
        j += 1
        if j == 3:
            j = 0
            i += 1
    if show_plots:
        plt.show()
    file_name = plots_path + 'all_sep_dist.png'
    plt.savefig(file_name)


def plot_all_distributions(data, attribute_names, plots_path, show_plots):
    # config output images
    plt.rcParams["figure.figsize"] = (25, 16)
    plt.rcParams['font.size'] = 18

    for attr in attribute_names:
        sns.distplot(normalizes(data[attr]), label=attr)

    plt.suptitle('All distributions', fontsize=20)
    plt.legend()
    if show_plots:
        plt.show()
    file_name = plots_path + 'all_dist.png'
    plt.savefig(file_name)


def main():
    show_plots = False

    parser = argparse.ArgumentParser(
        description='Plot the attributes distribution', prog="plot_distribution.py")
    parser.add_argument('--show', '-s', action='store_true',
                        help='shows the plots (defaut = False)')

    args = parser.parse_args()
    show_plots = args.show

    input_file = 'files/attributes.txt'
    plots_path = 'files/output_plot_distribution/'

    data = read_data(input_file)

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

    plot_distributions(data, attribute_names, plots_path, show_plots)
    plot_all_distributions(data, attribute_names, plots_path, show_plots)
    plot_all_sep_distributions(data, attribute_names, plots_path, show_plots)


if __name__ == "__main__":
    main()
