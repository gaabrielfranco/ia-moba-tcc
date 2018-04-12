#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from modules.data import read_data
import sklearn.feature_selection as fs

def main():
    parser = argparse.ArgumentParser(
        description='Rank/Select features using variance threshold', prog="feature_selection.py")
    parser.add_argument('--threshold', '-th', type=float, help='variance threshold t (0 <= t < 1) (default = 0)')
    parser.add_argument('--pruned', '-p', action='store_true',
                        help='load pruned data (defaut = False)')
    args = parser.parse_args()
    
    if not args.threshold:
        threshold = 0.0
    else:
        threshold = args.threshold
    
    if threshold < 0 or threshold > 1:
        parser.print_help()
        parser.exit(1)
    
    if args.pruned:
        data = read_data('df_data_pruned')
    else:
        data = read_data('df_data')
    
    for col in data.columns:
        data[col] = (data[col] - data[col].min()) / (data[col].max() - data[col].min())
        
    sel = fs.VarianceThreshold(threshold)
    new_data = sel.fit_transform(data)
    mask = sel.get_support()
    
    values = []
    texts = []
    for i,c in enumerate(data.columns):
        if mask[i]:
            status = 'selected.'
        else:
            status = 'not selected.'
            
        pos = 0
        while pos < len(values) and values[pos] >= sel.variances_[i]:
            pos += 1
        texts.insert(pos, '%s(%8.6f): %s' % (c.ljust(10), sel.variances_[i], status))
        values.insert(pos, sel.variances_[i])

    print('\n\nThreshold: %8.6f, %d attributes selected.\n' % (threshold, new_data.shape[1]))
    print('\n'.join(texts))
    print('\n')
    
if __name__ == "__main__":
    main()
