#!/usr/bin/env python3

# https://seaborn.pydata.org/tutorial/distributions.html

import numpy as np
import seaborn as sns
import argparse
import matplotlib.pyplot as plt

def remove_outliers(data, c=2.0):
    new_data = []
    
    avg = np.average(data)
    std = np.std(data)
    
    for d in data:
        if type(d) is list:
            d = d[0]
        if np.abs(avg - d) <= c * std:
            new_data.append(d)
            
    return new_data

def read_data(input_file, no_outliers):
    print('\nReading input data from file %s...' % input_file, end=' ')

    data = {}
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
    
    if no_outliers:
        for attr in data.keys():
            print('Outlier removal for attribute %s' % attr)
            print('\tBefore: min=%.4f max=%.4f' % (np.min(data[attr]), np.max(data[attr])))
            data[attr] = remove_outliers(data[attr])
            print('\tAfter: min=%.4f max=%.4f' % (np.min(data[attr]), np.max(data[attr])))

    return data


def plot_distributions(data, attribute_names, plots_path, show_plots, norm):
    # config output images
    plt.rcParams["figure.figsize"] = (25, 16)
    plt.rcParams['font.size'] = 18.0

    for attr in attribute_names:
        if norm:
            ax = sns.distplot(data[attr])
        else:
            ax = sns.distplot(data[attr], kde=False)
        title = attr + ' distribution'
        if norm:
            title += ' - normalized'
        plt.suptitle(title, fontsize=20)
        file_name = plots_path + attr + '_dist'
        if norm:
            file_name += '_norm'
        file_name += '.png'
        plt.savefig(file_name)
        print('Graph %s saved.' % file_name)
        if show_plots:
            plt.show()
        plt.clf()

def plot_all_sep_distributions(data, attribute_names, plots_path, show_plots, norm):
    # config output images
    plt.rcParams["figure.figsize"] = (25, 16)
    plt.rcParams['font.size'] = 18

    f, axarr = plt.subplots(3, 3, sharey=True)

    i = 0
    j = 0

    for attr in attribute_names:
        if norm:
            sns.distplot(data[attr], ax=axarr[i, j])
        else:
            sns.distplot(data[attr], ax=axarr[i, j], kde=False)
        title = attr + ' distribution'
        if norm:
            title += ' - normalized'
        axarr[i, j].set_title(title)
        j += 1
        if j == 3:
            j = 0
            i += 1
    if show_plots:
        plt.show()
    file_name = plots_path + 'all_sep_dist'
    if norm:
        file_name += '_norm'
    file_name += '.png'
    plt.savefig(file_name)
    print('Graph %s saved.' % file_name)
    plt.clf()


def plot_all_distributions(data, attribute_names, plots_path, show_plots, norm):
    # config output images
    plt.rcParams["figure.figsize"] = (25, 16)
    plt.rcParams['font.size'] = 18

    for attr in attribute_names:
        if norm:
            sns.distplot(data[attr], label=attr)
        else:
            sns.distplot(data[attr], label=attr, kde=False)

    title = 'All distributions'
    if norm:
        title += ' - normalized'
    plt.suptitle(title, fontsize=20)
    plt.legend()
    if show_plots:
        plt.show()
    file_name = plots_path + 'all_dist'
    if norm:
        file_name += '_norm'
    file_name += '.png'
    plt.savefig(file_name)
    print('Graph %s saved.' % file_name)
    plt.clf()


def main():
    show_plots = False

    parser = argparse.ArgumentParser(
        description='Plot the attributes distribution', prog="plot_distribution.py")
    parser.add_argument('--show', '-s', action='store_true',
                        help='shows the plots (defaut = False)')
    parser.add_argument('--norm', '-n', action='store_true',
                        help='normalize plots (defaut = False)')
    parser.add_argument('--remove_outliers', '-r', action='store_true',
                        help='remove outliers (defaut = False)')

    args = parser.parse_args()
    show_plots = args.show
    norm = args.norm
    no_outliers = args.remove_outliers

    input_file = 'files/attributes.txt'
    plots_path = 'files/output_plot_distribution/'

    data = read_data(input_file, no_outliers)

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

    plot_distributions(data, attribute_names, plots_path, show_plots, norm)
    plot_all_distributions(data, attribute_names, plots_path, show_plots, norm)
    plot_all_sep_distributions(data, attribute_names, plots_path, show_plots, norm)

if __name__ == "__main__":
    main()
