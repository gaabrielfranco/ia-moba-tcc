#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from modules.data import read_data
import argparse
from scipy.stats import kendalltau
import itertools
import pandas as pd
import numpy as np

########################################
#          About attributes            #
# K: higher => better                  #
# D: lower => better                   #
# A: higher => better                  #
# denies: higher => better             #
# gpm: higher => better                #
# hd: higher => better                 #
# hh: higher => better                 #
# lh: higher => better                 #
# xpm: higher => better                #
########################################

# Feature selection result: (assists, deaths, denies, gpm, hh)

# TODO:
#   - Kendall rank correlation entre o TOP 10 + KDA (todas as possibilidades)
#   - Deixar a métrica como um parâmetro genérico
#   - Na normalização, se joga o deaths para 0, mas ele divide na fórmula, e ai?!

'''
TOP 10:

    deaths,gpm,hh
    deaths,hh,xpm
    deaths,denies,hh,xpm
    assists,deaths,gpm,hh
    deaths,denies,gpm,hh
    assists,deaths,denies,gpm,hh
    assists,deaths,hh,lh
    deaths,denies,hh,kills
    assists,deaths,hh,xpm
    assists,deaths,denies,hh

'''


def sum_by_deaths(comb, data):
    metric_1 = np.zeros(len(data))
    metric_2 = np.zeros(len(data))

    deaths_presence = False

    for attr in comb[0].split(','):
        if attr != 'deaths':
            metric_1 += data[attr].as_matrix()
        else:
            deaths_presence = True
    if deaths_presence:
        metric_1 /= (1 + data['deaths'].as_matrix())
        deaths_presence = False

    for attr in comb[1].split(','):
        if attr != 'deaths':
            metric_2 += data[attr].as_matrix()
        else:
            deaths_presence = True
    if deaths_presence:
        metric_2 /= (1 + data['deaths'].as_matrix())

    return metric_1, metric_2


def harmonic(comb, data):
    metric_1 = np.zeros(len(data))
    metric_2 = np.zeros(len(data))

    for attr in comb[0].split(','):
        if attr != 'deaths':
            metric_1 += 1 / (1 + data[attr].as_matrix())
        else:
            metric_1 += 1 + data[attr].as_matrix()

    for attr in comb[1].split(','):
        if attr != 'deaths':
            metric_2 += 1 / (1 + data[attr].as_matrix())
        else:
            metric_2 += 1 + data[attr].as_matrix()

    return len(metric_1)/metric_1, len(metric_2)/metric_2


def main():
    parser = argparse.ArgumentParser(
        description='Kendall rank correlation coefficient script', prog="kendall_test.py")
    parser.add_argument('--wo', '-wo', action='store_true',
                        help='load data without outliers (defaut = False)')
    parser.add_argument('--metric', '-m', default='sum_by_deaths', choices=['sum_by_deaths', 'harmonic'],
                        help='Type of metric calculation: sum all and divide by deaths or harmonic mean (sum_by_deaths|harmonic) (default=sum_by_deaths)')
    parser.add_argument('--sample', '-s', default=0, type=int,
                        help='Number of samples for p-value test (defaut = Without sample test)')
    args = parser.parse_args()

    # Dynamic metric funcion
    if args.metric == 'sum_by_deaths':
        metric_func = sum_by_deaths
    else:
        metric_func = harmonic

    path = 'files/output_kendall_test/'

    attributes = [
        'deaths,gpm,hh',
        'deaths,hh,xpm',
        'deaths,denies,hh,xpm',
        'assists,deaths,gpm,hh',
        'deaths,denies,gpm,hh',
        'assists,deaths,denies,gpm,hh',
        'assists,deaths,hh,lh',
        'deaths,denies,hh,kills',
        'assists,deaths,hh,xpm',
        'assists,deaths,denies,hh',
        'assists,deaths,kills'
    ]
    attributes.sort()

    if args.wo:
        data = read_data('df_data')
    else:
        data = read_data('df_data_pruned')

    for col in data.columns:
        data[col] = (data[col] - data[col].min()) / \
            (data[col].max() - data[col].min())

    combinations = []
    combs = itertools.combinations(attributes, 2)
    for c in combs:
        combinations.append(list(c))

    kendall = []
    taus = []
    kendall_sample = []
    taus_sample = []
    for comb in combinations:
        metric_1, metric_2 = metric_func(comb, data)

        tau, p_value = kendalltau(metric_1, metric_2)

        kendall.append(
            {'comb_1': comb[0], 'comb_2': comb[1], 'tau': tau, 'p_value': p_value})
        taus.append(tau)

        if args.sample > 0:
            sample = np.random.randint(0, len(data), args.sample)

            data_sample = data.iloc[sample, :]

            metric_1, metric_2 = metric_func(comb, data_sample)

            tau, p_value = kendalltau(metric_1, metric_2)

            kendall_sample.append(
                {'comb_1': comb[0], 'comb_2': comb[1], 'tau': tau, 'p_value': p_value})
            taus_sample.append(tau)

    taus.sort()

    ord_kendall = []
    for t in taus:
        for k in kendall:
            if k['tau'] == t:
                ord_kendall.append(k)

    df = pd.DataFrame(ord_kendall)
    file_name = 'kendall_' + args.metric + \
        '.csv' if args.wo else 'kendall_pruned_' + args.metric + '.csv'
    df.to_csv(path + file_name, sep=';', decimal=',')
    print('%s saved.' % (path + file_name))

    if args.sample > 0:
        file_name_samples = 'kendall_sample_' + str(args.sample) + '_' + args.metric + \
            '.csv' if args.wo else 'kendall_pruned_sample_' + \
            str(args.sample) + '_' + args.metric + '.csv'
        df_sample = pd.DataFrame(kendall_sample)
        df_sample.to_csv(path + file_name_samples, sep=';', decimal=',')
        print('%s saved.' % (path + file_name_samples))


if __name__ == "__main__":
    main()
