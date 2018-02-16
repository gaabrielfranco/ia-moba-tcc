'''
Implementado por Gabriel Franco
'''

import numpy as np
from sklearn.cluster import KMeans


def normalizes(x):
    x_norm = []
    minimum = np.min(x)
    maximum = np.max(x)
    for i in x:
        x_norm.append((i - minimum) / (maximum - minimum))

    return x_norm, minimum, maximum


def un_normalizes(m, minimum, maximum):
    x_un_norm = []
    for i in m:
        x_un_norm.append(i * (maximum - minimum) + minimum)

    return x_un_norm


def remove_outliers(method, data, c=2.0):
    new = []
    media = np.average(data)
    std = np.std(data)
    count = 0
    for d in data:
        if method == 'all':
            eff = d[0] - d[1] + d[2] + max(d[3], d[4])
        else:
            eff = d[0] - d[1] + d[2]
        if np.abs(media - eff) < c * std:
            new.append(d)
        else:
            count += 1
    return new, count


def summary(arq, eff, tabs=0):
    if tabs == 0:
        arq.write('Media: ' + str(np.average(eff)) + '\n')
        arq.write('Desvio: ' + str(np.std(eff)) + '\n')
        arq.write('Coef. Variacao: ' +
                  str(np.std(eff) / np.average(eff)) + '\n')
        arq.write('Minimo: ' + str(np.min(eff)) + '\n')
        arq.write('Maximo: ' + str(np.max(eff)) + '\n')
    else:
        for i in range(len(eff)):
            arq.write('\t\tCluster %d:\n' % (i + 1))
            arq.write('\t\t\tMedia: ' + str(np.average(eff[i])) + '\n')
            arq.write('\t\t\tDesvio: ' + str(np.std(eff[i])) + '\n')
            arq.write('\t\t\tCoef. Variacao: ' +
                      str(np.std(eff[i]) / np.average(eff[i])) + '\n')
            arq.write('\t\t\tMinimo: ' + str(np.min(eff[i])) + '\n')
            arq.write('\t\t\tMaximo: ' + str(np.max(eff[i])) + '\n')


def classification(k, data, method, without_outliers):
    if without_outliers:
        f = open('files/output_k-means/kmeans_' +
                 method + '_' + str(k) + '.txt', 'w')
    else:
        f = open('files/output_k-means/kmeans_' +
                 method + '_' + str(k) + '.txt', 'a')

    data_norm, min_norm, max_norm = normalizes(data)

    if method == 'all':
        print('Execucao para K = %d de todos os atributos' % k)
    else:
        print('Execucao para K = %d do KDA' % k)

    inertia = []
    cluster_centers_eff = []
    eff_f = []
    for i in range(k):
        eff_f.append([])

    if without_outliers:
        f.write(
            'Execucao sem podas de outliers com dados normalizados por n-partidas\n\n')
        print('\tExecucao sem poda de outliers')
    else:
        len_att = len(data_norm)

        data_norm, count_all = remove_outliers(method, data_norm)

        f.write(
            '\n==================================================================================\n')
        f.write(
            'Execucao com podas de outliers com dados normalizados por n-partidas\n\n')
        f.write('Foram podados ' + str(count_all) +
                ' de ' + str(len_att) + ' jogadores.\n\n')

        print('\tCom poda de outliers')

    for i in range(0, 10):
        print('\t\tExecucao %d' % i)
        f.write('Execucao com semente ' + str(i) + ':\n')
        km = KMeans(n_clusters=k, random_state=i, n_jobs=4)
        labels = km.fit_predict(data_norm)

        inertia.append(km.inertia_)
        f.write('\tInertia da execucao com semente ' + str(i) + ':\n')
        f.write('\t' + str(km.inertia_) + '\n\n')
        count = [0] * k
        for l in labels:
            count[l] += 1
        f.write('\tContagem da execucao com semente ' + str(i) + ':\n')
        f.write('\t' + str(count) + '\n\n')

        centroids = un_normalizes(
            km.cluster_centers_[:], min_norm, max_norm)
        f.write(
            '\tCentroides da execucao com semente ' + str(i) + ':\n')
        for j in centroids:
            f.write('\t' + str(j) + '\n')
        f.write('\n')

        if method == 'all':
            for j in centroids:
                cluster_centers_eff.append(
                    j[0] - j[1] + j[2] + max(j[3], j[4]))

            for j, d in enumerate(data_norm):
                eff = d[0] - d[1] + d[2] + max(d[3], d[4])

                eff_f[labels[j]].append(
                    abs(cluster_centers_eff[labels[j]] - eff))
        else:
            for j in centroids:
                cluster_centers_eff.append(
                    j[0] - j[1] + j[2])

            for j, d in enumerate(data_norm):
                eff = d[0] - d[1] + d[2]

                eff_f[labels[j]].append(
                    abs(cluster_centers_eff[labels[j]] - eff))

        f.write('\tDados da metrica F: \n')
        summary(f, eff_f, 1)
        f.write('\n')

        eff_f.clear()
        eff_f = []
        for i in range(k):
            eff_f.append([])
        cluster_centers_eff.clear()
        centroids.clear()

    f.write('Dados da metrica inertia: \n')
    summary(f, inertia)

    inertia.clear()

    f.close()


def main():
    data_all = []
    data_kda = []
    n_matches = []

    fp = open('files/attributes.txt', 'r')

    for l in fp:
        parts = l.strip().split()
        for i, p in enumerate(parts):
            parts[i] = int(p)
        if parts[4] >= 5:
            data_all.append(
                list(np.array(parts[1:4] + [parts[5]] + [parts[9]]) / parts[4]))
            data_kda.append(list(np.array(parts[1:4]) / parts[4]))

    fp.close()

    for i in ['all', 'kda']:
        for j in [3, 4, 5]:
            for k in [True, False]:
                if i == 'all':
                    classification(j, data_all, i, k)
                else:
                    classification(j, data_kda, i, k)


if __name__ == "__main__":
    main()
