#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 15:41:12 2018

@author: marcos
"""
import argparse
from modules.data import read_data
import itertools
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import numpy as np
import sklearn.feature_selection as fs


def create_restrictions(data, corr_threshold):
    corr = data.corr()
    attributes = list(corr.columns)
    counts = np.zeros(len(attributes))
    restrictions = np.zeros((len(attributes), len(attributes)))
    for i in range(0, len(attributes)-1):
        for j in range(i+1, len(attributes)):
            if abs(corr[attributes[i]][attributes[j]]) >= corr_threshold:
                restrictions[i][j] += 1
                restrictions[j][i] += 1
                counts[i] += 1
                counts[j] += 1

    return restrictions


def check_violation(individual, restrictions):
    attributes_map = {"kills": 0, "deaths": 1,
                      "assists": 2, "denies": 3, "gpm": 4, "hd": 5, "hh": 6, "lh": 7, "xpm": 8}

    for i in individual:
        for j in individual:
            if restrictions[attributes_map[i]][attributes_map[j]]:
                return True

    return False


def fitness(data, metric='euclidean', k=10, seed=None):
    if metric == 'variance':
        sel = fs.VarianceThreshold()
        sel.fit(data)
        return np.average(np.array(sel.variances_))

    if seed < 0:
        random_seed = None
    else:
        random_seed = seed

    km = KMeans(n_clusters=k, random_state=random_seed, n_jobs=-1)
    labels = km.fit_predict(data)
    if metric == 'euclidean':
        return silhouette_score(data, labels)
    elif metric == 'cosine':
        return silhouette_score(data, labels, metric='cosine')
    else:
        return km.inertia_


def solution_str(candidate, save=False):
    return '{' + ','.join(candidate['solution']) + '}: %f' % candidate['evaluation'] if not save \
        else ','.join(candidate['solution']) + ',%f\n' % candidate['evaluation']


def save_solution(best, data, args):
    s = 'k;seed;metric;min_size;max_size;outliers;threshold\n'
    s += '%d;%d;%s;%d;%d;%d;%f\n' % (args.k, args.seed,
                                     args.metric, args.mins, args.maxs, args.wo, args.threshold)

    s += 'Top 10 solutions\n'

    for solution in best:
        s += solution_str(solution, True)

    if args.lang == 'pt':
        s.replace('.', ',')

    fp = open(args.csv_file, 'w')
    fp.write(s)
    fp.close()


def main():
    # Parsing command line arguments
    parser = argparse.ArgumentParser(
        description='Exact algorithm for solving feature selection for the silhouette problem')
    parser.add_argument('csv_file', help='CSV file to save solution')
    parser.add_argument('--k', type=int, default=10,
                        help='Number of clusters (default=10)')
    parser.add_argument('--seed', type=int, default=-1,
                        help='Random seed (default=-1). Use -1 for totally uncontrolled randomness')
    parser.add_argument('--lang', default='en',
                        help='Whether use . or , as floating point number decimal separator in output. If lang=en, uses dot if lang=pt, uses comma (default=en)')
    parser.add_argument('--wo', action='store_true',
                        help='Load data with outliers (default=False)')
    parser.add_argument('--mins', type=int, default=3,
                        help='Minimum size of solution (default=3)')
    parser.add_argument('--maxs', type=int, default=6,
                        help='Maximum size of solution (default=6)')
    parser.add_argument('--metric', choices=['euclidean', 'cosine', 'variance', 'inertia'], default='euclidean',
                        help='Distance metric: euclidean | cosine | variance | inertia (default=euclidean)')
    parser.add_argument('--threshold', type=float, default=0.75,
                        help='Threshold value (defaut=0.75)')
    args = parser.parse_args()

    # Loading data
    if args.wo:
        data = read_data('df_data')
    else:
        data = read_data('df_data_pruned')

    # Normalizing data
    for col in data.columns:
        data[col] = (data[col] - data[col].min()) / \
            (data[col].max() - data[col].min())

    # Create restrictions
    restrictions = create_restrictions(data, args.threshold)

    # Generate all possible combinations
    cols = list(data.columns)
    combinations = []
    for r in range(args.mins, args.maxs+1):
        combs = itertools.combinations(cols, r)
        for c in combs:
            if not check_violation(c, restrictions):
                combinations.append(list(c))

    # Find best solution
    count = 1
    if args.metric == 'inertia':
        best = [{'evaluation': float('inf'), 'solution': []}
                for i in range(10)]
    else:
        best = [{'evaluation': 0.0, 'solution': []} for i in range(10)]
    for it, c in enumerate(combinations):
        candidate = {'evaluation': fitness(
            data[c], args.metric, args.k, args.seed), 'solution': c}
        print('\tTesting set =', solution_str(candidate), end=' ')
        if it < 10:
            best[it] = candidate
            print('new best!')
        elif args.metric == 'inertia':
            print_best = True
            position_out = -1
            diff = -1
            for index in range(len(best)):
                if candidate['evaluation'] < best[index]['evaluation']:
                    if diff == -1:
                        position_out = index
                        diff = best[index]['evaluation'] - \
                            candidate['evaluation']
                        print_best = False
                    elif best[index]['evaluation'] - candidate['evaluation'] > diff:
                        position_out = index
                        diff = best[index]['evaluation'] - \
                            candidate['evaluation']
                        print_best = False
            if print_best:
                print()
            else:
                best[position_out] = candidate
                print('new best!')
        else:
            print_best = True
            position_out = -1
            diff = -1
            for index in range(len(best)):
                if candidate['evaluation'] > best[index]['evaluation']:
                    if diff == -1:
                        position_out = index
                        diff = candidate['evaluation'] - \
                            best[index]['evaluation']
                        print_best = False
                    elif candidate['evaluation'] - best[index]['evaluation'] > diff:
                        position_out = index
                        diff = candidate['evaluation'] - \
                            best[index]['evaluation']
                        print_best = False
            if print_best:
                print()
            else:
                best[position_out] = candidate
                print('new best!')
        count += 1

    print('\nTop 10 best solution found of %d tested:' % count)

    for solution in best:
        print(solution)

    save_solution(best, data, args)


if __name__ == '__main__':
    main()
