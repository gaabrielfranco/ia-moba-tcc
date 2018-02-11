#=================================================================================
# Versão 1: (K + A - D) / Npartidas
# Versão 2: (K + A - D + max(LH, denies)) / Npartidas
#
# - 10 execuções com random_state distintas, para K = 3, 4 e 5
#   - Para cada 10 execuções do passo acima, computar média e desvio para inércia
# - Manter normalização
# - Deixar outliers
# - No arquivo output_n_partidas.txt, incluir min e max absoluto (antes de normalizar)
#=================================================================================

import numpy as np
from sklearn.cluster import KMeans


def normalizes(x):
    xNorm = []
    minimum = np.min(x)
    maximum = np.max(x)
    for i in x:
        xNorm.append((i - minimum) / (maximum - minimum))

    return xNorm


def remove_outliers(method, data, c=2.0):
    new = []
    media = np.average(data)
    std = np.std(data)
    count = 0
    for d in data:
        if method == 'all':
            # (K - D + A + max(denies, LH)) / n_partidas
            eff = d[0] - d[1] + d[2] + max(d[3], d[4])
        else:
            # (K - D + A) / n_partidas
            eff = d[0] - d[1] + d[2]
        if np.abs(media - eff) < c * std:
            new.append(d)
        else:
            count += 1
    return new, count


def summary(arq, eff):
    arq.write('Media: ' + str(np.average(eff)) + '\n')
    arq.write('Desvio: ' + str(np.std(eff)) + '\n')
    arq.write('Coef. Variacao: ' + str(np.std(eff) / np.average(eff)) + '\n')
    arq.write('Minimo: ' + str(np.min(eff)) + '\n')
    arq.write('Maximo: ' + str(np.max(eff)) + '\n')


def classification(k, data_all, data_kda):
    file_all = open('files/kmeans_all_' + str(k) + '.txt', 'w')
    file_kda = open('files/kmeans_kda_' + str(k) + '.txt', 'w')

    data_all_normalized = normalizes(data_all)
    data_kda_normalized = normalizes(data_kda)

    print('Execucao para K = %d' % k)
    inertia = []
    file_all.write(
        'Execucao sem podas de outliers com dados normalizados por n-partidas...\n\n')
    print('\tSem poda de outliers para todos os atributos')
    # All attributes with normalized min-max data
    for i in range(0, 10):
        print('\t\tExecucao %d' % i)
        file_all.write('Execucao com semente ' + str(i) + ':\n')
        km = KMeans(n_clusters=k, random_state=i, n_jobs=4)
        labels = km.fit_predict(data_all_normalized)

        inertia.append(km.inertia_)
        file_all.write('\tInertia da execucao com semente ' + str(i) + ':\n')
        file_all.write('\t' + str(km.inertia_) + '\n\n')
        count = [0] * k
        for l in labels:
            count[l] += 1
        file_all.write('\tContagem da execucao com semente ' + str(i) + ':\n')
        file_all.write('\t' + str(count) + '\n\n')

        # Normalized n-matches data (just for cluster centers)
        km = KMeans(n_clusters=k, random_state=i, n_jobs=4)
        labels = km.fit_predict(data_all)
        file_all.write(
            '\tCentroides da execucao com semente ' + str(i) + ':\n')
        file_all.write('\t' + str(km.cluster_centers_) + '\n\n')

    file_all.write('Dados da metrica inertia: \n')
    summary(file_all, inertia)

    inertia.clear()

    file_kda.write(
        'Execucao sem podas de outliers com dados normalizados por n-partidas...\n\n')
    print('\tSem poda de outliers para KDA')
    # KDA attributes
    for i in range(0, 10):
        print('\t\tExecucao %d' % i)
        file_kda.write('Execucao com semente ' + str(i) + ':\n\n')
        km = KMeans(n_clusters=k, random_state=i, n_jobs=4)
        labels = km.fit_predict(data_kda_normalized)

        inertia.append(km.inertia_)
        file_kda.write('\tInertia da execucao com semente ' + str(i) + ':\n')
        file_kda.write('\t' + str(km.inertia_) + '\n\n')
        count = [0] * k
        for l in labels:
            count[l] += 1
        file_kda.write('\tContagem da execucao com semente ' + str(i) + ':\n')
        file_kda.write('\t' + str(count) + '\n\n')

        # Normalized n-matches data (just for cluster centers)
        km = KMeans(n_clusters=k, random_state=i, n_jobs=4)
        labels = km.fit_predict(data_kda)
        file_kda.write(
            '\tCentroides da execucao com semente ' + str(i) + ':\n')
        file_kda.write('\t' + str(km.cluster_centers_) + '\n\n')

    file_kda.write('Dados da metrica inertia: \n')
    summary(file_kda, inertia)

    len_all = len(data_all_normalized)
    len_kda = len(data_kda_normalized)

    data_all_normalized, count_all = remove_outliers(
        'all', data_all_normalized)
    data_kda_normalized, count_kda = remove_outliers(
        'kda', data_kda_normalized)

    inertia.clear()

    file_all.write(
        '\n==================================================================================\n')
    file_all.write(
        'Execucao com podas de outliers com dados normalizados por n-partidas...\n\n')
    file_all.write('Foram podados ' + str(count_all) +
                   ' de ' + str(len_all) + ' jogadores.\n\n')
    print('\tCom poda de outliers para todos os atributos')
    # All attributes with normalized min-max data
    for i in range(0, 10):
        print('\t\tExecucao %d' % i)
        file_all.write('Execucao com semente ' + str(i) + ':\n')
        km = KMeans(n_clusters=k, random_state=i, n_jobs=4)
        labels = km.fit_predict(data_all_normalized)

        inertia.append(km.inertia_)
        file_all.write('\tInertia da execucao com semente ' + str(i) + ':\n')
        file_all.write('\t' + str(km.inertia_) + '\n\n')
        count = [0] * k
        for l in labels:
            count[l] += 1
        file_all.write('\tContagem da execucao com semente ' + str(i) + ':\n')
        file_all.write('\t' + str(count) + '\n\n')

        # Normalized n-matches data (just for cluster centers)
        km = KMeans(n_clusters=k, random_state=i, n_jobs=4)
        labels = km.fit_predict(data_all)
        file_all.write(
            '\tCentroides da execucao com semente ' + str(i) + ':\n')
        file_all.write('\t' + str(km.cluster_centers_) + '\n\n')

    file_all.write('Dados da metrica inertia: \n')
    summary(file_all, inertia)

    inertia.clear()

    file_kda.write(
        '\n==================================================================================\n')
    file_kda.write(
        'Execucao com podas de outliers com dados normalizados por n-partidas...\n\n')
    file_kda.write('Foram podados ' + str(count_kda) +
                   ' de ' + str(len_kda) + ' jogadores.\n\n')
    print('\tCom poda de outliers para KDA')
    # KDA attributes
    for i in range(0, 10):
        print('\t\tExecucao %d' % i)
        file_kda.write('Execucao com semente ' + str(i) + ':\n\n')
        km = KMeans(n_clusters=k, random_state=i, n_jobs=4)
        labels = km.fit_predict(data_kda_normalized)

        inertia.append(km.inertia_)
        file_kda.write('\tInertia da execucao com semente ' + str(i) + ':\n')
        file_kda.write('\t' + str(km.inertia_) + '\n\n')
        count = [0] * k
        for l in labels:
            count[l] += 1
        file_kda.write('\tContagem da execucao com semente ' + str(i) + ':\n')
        file_kda.write('\t' + str(count) + '\n\n')

        # Normalized n-matches data (just for cluster centers)
        km = KMeans(n_clusters=k, random_state=i, n_jobs=4)
        labels = km.fit_predict(data_kda)
        file_kda.write(
            '\tCentroides da execucao com semente ' + str(i) + ':\n')
        file_kda.write('\t' + str(km.cluster_centers_) + '\n\n')

    file_kda.write('Dados da metrica inertia: \n')
    summary(file_kda, inertia)

    print('\n')

    file_all.close()
    file_kda.close()


def main():
    data_all = []
    data_kda = []
    n_matches = []

    fp = open('files/atributes.txt', 'rU')

    for l in fp:
        parts = l.strip().split()
        for i, p in enumerate(parts):
            parts[i] = int(p)
        if parts[4] >= 5:
            data_all.append(
                list(np.array(parts[1:4] + [parts[5]] + [parts[9]]) / parts[4]))
            data_kda.append(list(np.array(parts[1:4]) / parts[4]))

    fp.close()

    for k in [3, 4, 5]:
        classification(k, data_all, data_kda)


if __name__ == "__main__":
    main()
