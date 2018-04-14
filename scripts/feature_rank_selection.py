#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import numpy as np
from modules.data import read_data
import sklearn.feature_selection as fs

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

### Get the order of magnitude of a number
def getOrder(x):
    if x == 0.0:
        return 0.0
    return 10**np.floor(np.log10(np.abs(x)))

### Main function
def main():
    # Parsing command line arguments
    parser = argparse.ArgumentParser(
        description='Rank/Select features using variance threshold', prog="feature_selection.py")
    parser.add_argument(
        'perc', type=float, help='percentage of the relevance space covered by feature selection (0.0 <= perc <= 1.0)')
    parser.add_argument('--pruned', '-p', action='store_true',
                        help='load pruned data (defaut = False)')
    args = parser.parse_args()

    if args.perc < 0 or args.perc > 1:
        parser.print_help()
        parser.exit(1)

    # Loading data
    if args.pruned:
        data = read_data('df_data_pruned')
    else:
        data = read_data('df_data')

    # Normalizing data
    for col in data.columns:
        data[col] = (data[col] - data[col].min()) / \
            (data[col].max() - data[col].min())

    # Threshold determination
    sel = fs.VarianceThreshold()
    sel.fit(data)
    vls = np.array(sel.variances_)
    vls = (vls - np.min(vls)) / (np.max(vls) - np.min(vls))

    perc = 1 - args.perc
    maxVal = 0
    for v in vls:
        if v < perc:
            originalVal = v * (np.max(sel.variances_) -
                               np.min(sel.variances_)) + np.min(sel.variances_)
            if originalVal > maxVal:
                maxVal = originalVal
    delta = getOrder(maxVal) * 1E-2
    threshold = maxVal + delta

    # Applying feature selection using the obtained threshold
    sel = fs.VarianceThreshold(threshold)
    new_data = sel.fit_transform(data)
    mask = sel.get_support()

    # Sorting data by their variance
    values = []
    names = []
    texts = []
    for i, c in enumerate(data.columns):
        if mask[i]:
            status = 'selected.'
        else:
            status = 'not selected.'

        pos = 0
        while pos < len(values) and values[pos] >= sel.variances_[i]:
            pos += 1
        texts.insert(pos, '%s(%8.6f): %s' %
                     (c.ljust(10), sel.variances_[i], status))
        values.insert(pos, sel.variances_[i])
        names.insert(pos, c)

    # Printing a short report
    print('\n\nSelecting features above %.2f%% of relevance space.' %
          (args.perc * 100))
    print('Dinamically obtained threshold: %8.6f, %d attributes selected.\n' %
          (threshold, new_data.shape[1]))
    print('====== Ranking =========')
    print('\n'.join(texts))
    print('\n')
    
    values = {'attribute': names, 'variance': values}
    df = pd.DataFrame(values)
    
    with plt.style.context('seaborn-whitegrid'):
        plt.bar(names, df['variance'])
        plt.title('Selecting Features above %d%% of relevance space' % (args.perc * 100))
        ### Legenda para a linha do limiar
        plt.axhline(threshold, color='k', linestyle='--', label='threshold')
        plt.legend()
        plt.ylabel('Variance')
        plt.xlabel('Attributes')
        plt.show()
    
if __name__ == "__main__":
    main()
