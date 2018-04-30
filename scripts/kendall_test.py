from modules.data import read_data, normalizes
import argparse
from scipy.stats import kendalltau
import itertools
import pandas as pd

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


def metric_func(comb, data):
    metric_1, metric_2 = [0.0 for i in range(len(data))], [
        0.0 for i in range(len(data))]

    deaths_presence = False

    for attr in comb[0].split(','):
        if attr != 'deaths':
            metric_1 += data[attr]
        else:
            deaths_presence = True
    if deaths_presence:
        metric_1 /= data['deaths']
        deaths_presence = False

    for attr in comb[1].split(','):
        if attr != 'deaths':
            metric_2 += data[attr]
        else:
            deaths_presence = True
    if deaths_presence:
        metric_2 /= data['deaths']

    return metric_1, metric_2


def kendall_corr(data, metric_1, metric_2, comb_1, comb_2):
    tau, p_value = kendalltau(metric_1, metric_2)

    return tau, p_value


def main():
    parser = argparse.ArgumentParser(
        description='Kendall rank correlation coefficient script', prog="kendall_test.py")
    parser.add_argument('--wo', '-wo', action='store_true',
                        help='load data without outliers (defaut = False)')
    args = parser.parse_args()

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
        'kills,deaths,assists'
    ]

    if args.wo:
        data = read_data('df_data')
    else:
        data = read_data('df_data_pruned')

    for attr in data:
        data[attr] = (normalizes(data[attr]))[0]

    combinations = []

    combs = itertools.combinations(attributes, 2)
    for c in combs:
        combinations.append(list(c))

    kendall = []
    taus = []
    for comb in combinations:
        metric_1, metric_2 = metric_func(comb, data)

        tau, p_value = kendall_corr(data, metric_1, metric_2, comb[0], comb[1])

        kendall.append(
            {'comb_1': comb[0], 'comb_2': comb[1], 'tau': tau, 'p_value': p_value})
        taus.append(tau)

    taus.sort()
    ord_kendall = []
    for t in taus:
        for k in kendall:
            if k['tau'] == t:
                ord_kendall.append(k)

    df = pd.DataFrame(ord_kendall)
    file_name = 'kendall.csv' if args.wo else 'kendall_pruned.csv'
    df.to_csv(path + file_name)
    print('%s saved.' % (path + file_name))


if __name__ == "__main__":
    main()
