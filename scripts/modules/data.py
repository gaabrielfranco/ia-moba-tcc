import numpy as np
from pprint import PrettyPrinter
import pandas as pd


def normalizes(x):
    x_norm = []
    minimum = np.min(x, axis=0)
    maximum = np.max(x, axis=0)
    for i in x:
        x_norm.append((i - minimum) / (maximum - minimum))

    return x_norm, minimum, maximum


def de_normalize(x, minimum, maximum):
    x_de_norm = []

    for i in x:
        x_de_norm.append(i * (maximum - minimum) + minimum)

    return x_de_norm

# Refatoraresse método para ler de um json, criando o método que gera o json apenas 1x. Tem que ter poda e análise de correlação


def remove_outliers(data, c=2.0):
    new_data = []
    outliers = []
    outliers_attr = []
    attributes = ["kills", "deaths",
                  "assists", "denies", "gpm", "hd", "hh", "lh", "xpm"]
    avg = np.average(list(data), axis=0)
    std = np.std(list(data), axis=0)

    for d in data:
        att_v = np.abs(avg - d) <= c * std
        if att_v.all():
            new_data.append(d)
        else:
            outliers.append(d)
            attr = []
            for i, j in enumerate(att_v):
                if j:
                    attr.append(attributes[i])
            outliers_attr.append(attr)
    '''
    print("tamanho de data c/ outliers = ", len(data))
    print("tamanho de data s/ outliers = ", len(new_data))
    print()
    print("min c/ outlier = ", list(np.min(list(data), axis=0)))
    print("max c/ outlier = ", list(np.max(list(data), axis=0)))
    print()
    print("min s/ outlier = ", list(np.min(list(new_data), axis=0)))
    print("max s/ outlier = ", list(np.max(list(new_data), axis=0)))
    print()
    print("dif do max c/ menos s/ outlier")
    print(list(np.max(list(data), axis=0) - np.max(list(new_data), axis=0)))
    '''
    print(len(outliers_attr))
    count = 0
    teste = [0 for i in range(10)]
    for i in outliers_attr:
        teste[len(i)] += 1

    print(teste)
    # return new_data


def read_data(method='all'):
    if method == 'all':
        df_all = pd.read_json('files/data/data_all.json')
        df_corr = pd.read_json('files/data/data_corr.json')
        return df_all
        # print(df_all)


def create_data(input_file, corr=True, verbose=False):
    print('\nReading input data from file %s...' % input_file, end=' ')

    data = {}
    data_corr = {}
    data['all'] = []
    data['kda'] = []
    data['kills'] = []
    data['deaths'] = []
    data['assists'] = []
    data['denies'] = []
    data['gpm'] = []
    data['hd'] = []
    data['hh'] = []
    data['lh'] = []
    data['xpm'] = []
    if corr:
        data_corr['kills-corr'] = []
        data_corr['deaths-corr'] = []
        data_corr['assists-corr'] = []
        data_corr['denies-corr'] = []
        data_corr['gpm-corr'] = []
        data_corr['hd-corr'] = []
        data_corr['hh-corr'] = []
        data_corr['lh-corr'] = []
        data_corr['xpm-corr'] = []

    fp = open(input_file, 'r')

    for l in fp:
        parts = l.strip().split()
        for i, p in enumerate(parts):
            parts[i] = int(p)
        if parts[4] >= 5:
            data['kda'].append(list(np.array(parts[1:4]) / parts[4]))
            data['all'].append(
                list(np.array(parts[1:4] + parts[5:]) / parts[4]))
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
    data_pd = pd.DataFrame(data)
    data_pd.to_json('files/data/data_all.json')
    print('done.\n')

    # Dynamically maps n least correlated attributes to each attribute
    correlation_map = []
    correlation_map_names = {}

    if corr:
        # Mapping the database
        attr_positions = np.array([1, 2, 3, 5, 6, 7, 8, 9, 10])
        matches_position = 4
        attr_names = np.array(['kills', 'deaths', 'assists',
                               'denies', 'gpm', 'hd', 'hh', 'lh', 'xpm'], dtype=str)

        # n least correlated atrributes and minimum matches per player
        n = 4
        min_matches = 5

        # normalizes database and discard maximum and minimum information (underline redirects to "nothing")
        dt, _, _ = normalizes(data['all'])

        # Computes correlation matrix (absolute values)
        corr_matrix = pd.DataFrame(dt).corr().abs().as_matrix()

        # Line count
        i = 0
        for attr_line in corr_matrix:
            # Sort indexes of matrix line by its values and get the indexes related to the n smallest values
            sorted_indexes = attr_line.argsort()[:n]

            correlation_map.append(attr_positions[sorted_indexes])
            correlation_map_names[attr_names[i]] = list(
                attr_names[sorted_indexes])

            i += 1

        fp = open(input_file, 'r')

        for l in fp:
            parts = l.strip().split()
            for i, p in enumerate(parts):
                parts[i] = int(p)
            if parts[matches_position] >= min_matches:
                for i, position in enumerate(attr_positions):
                    line = [parts[position]]
                    # print('Data for %s:' % (attr_names[i] + '-corr'), end=' ')
                    for other in correlation_map[i]:
                        line.append(parts[other])
                        l = list(attr_positions)
                        # print('%s (%d)' % (attr_names[l.index(other)], other), end=' ')
                    # print()
                    data_corr[attr_names[i] + '-corr'].append(
                        list(np.array(line) / parts[matches_position]))

                # print()

        fp.close()

        data_pd = pd.DataFrame(data_corr)
        data_pd.to_json('files/data/data_corr.json')

        if verbose:
            pp = PrettyPrinter()
            pp.pprint(correlation_map_names)
            print()

    return data, data_corr, correlation_map, correlation_map_names
