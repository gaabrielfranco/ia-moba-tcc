#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 15:41:12 2018

@author: marcos
"""
import argparse
from modules.data import read_data
import itertools
import numpy as np
import sklearn.feature_selection as fs

def get_avg_variance(data):
    sel = fs.VarianceThreshold()
    sel.fit(data)
    return np.average(np.array(sel.variances_))
    
def solution_str(candidate):
    return '{' + ','.join(candidate['solution']) + '}: %f' % candidate['evaluation']

def main():
    ### Parsing command line arguments
    parser = argparse.ArgumentParser(description='Exact algorithm for solving feature selection for the variance problem')
    parser.add_argument('--with_outilers', '-wo', action='store_true', help='Load data with outliers (default=False)')
    parser.add_argument('--mins', type=int, default=3, help='Minimum size of solution (default=3)')
    parser.add_argument('--maxs', type=int, default=6, help='Maximum size of solution (default=6)')
    args = parser.parse_args()
    
    ### Loading data
    if args.with_outilers:
        data = read_data('df_data')
    else:
        data = read_data('df_data_pruned')
        
    ### Normalizing data
    for col in data.columns:
        data[col] = (data[col] - data[col].min()) / (data[col].max() - data[col].min())
        
    ### Generate all possible combinations
    cols = list(data.columns)
    combinations = []
    for r in range(args.mins, args.maxs+1):
        combs = itertools.combinations(cols, r)
        for c in combs:
            combinations.append(list(c))
            
    ### Find best solution
    count = 0
    best = {'evaluation': 0.0, 'solution': []}
    for c in combinations:
        candidate ={'evaluation': get_avg_variance(data[c]), 'solution': c}
        print('\tTesting set =', solution_str(candidate), end=' ')
        if candidate['evaluation'] > best['evaluation']:
            best = candidate
            print('new best!')
        else:
            print()
        count += 1
            
    print('\nBest solution found of %d tested:' % count)
    print('\tBest =', solution_str(best))

if __name__=='__main__':
    main()
