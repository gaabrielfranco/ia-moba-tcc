#!/usr/bin/env python3

from modules.data import read_data
import argparse

import numpy as np
import pandas as pd
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt

def main():
    show_plots = False

    parser = argparse.ArgumentParser(
        description='Plot the attributes distribution', prog="plot_distribution.py")
    parser.add_argument('--show', '-s', action='store_true',
                        help='shows the plots (defaut = False)')
    parser.add_argument('--with_outliers', '-wo', action='store_true',
                        help='plot with outliers (defaut = False)')

    args = parser.parse_args()
    show_plots = args.show
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

    df = pd.DataFrame(data=np.array(data['all']), columns=['kills', 'deaths', 'assists', 'denies', 'gpm', 'hd', 'hh', 'lh', 'xpm'])
    
    print('\n\nProcessing scatter matrix...', end=' ')
    scatter_matrix(df, alpha=0.2, figsize=(6,6), diagonal='kde')
    print('done.')
    
    plt.savefig(plots_path + 'scatter_matrix.png', dpi='figure')
    
    if show_plots:
        plt.show()

if __name__ == "__main__":
    main()