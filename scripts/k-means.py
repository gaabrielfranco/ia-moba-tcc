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
            arq.write('\tGrupo %d:\n' % (i + 1))
            arq.write('\t\tMedias: ' + str(np.average(eff[i])) + '\n')
            arq.write('\t\tDesvios: ' + str(np.std(eff[i])) + '\n')
            arq.write('\t\tCoefs. Variacao: ' +
                      str(np.std(eff[i]) / np.average(eff[i])) + '\n')
            arq.write('\t\tMinimos: ' + str(np.min(eff[i])) + '\n')
            arq.write('\t\tMaximos: ' + str(np.max(eff[i])) + '\n')


def classification(k, data_all, data_kda):
    file_all = open('files/kmeans_all_' + str(k) + '.txt', 'w')
    file_kda = open('files/kmeans_kda_' + str(k) + '.txt', 'w')

    data_all_normalized, min_norm_all, max_norm_all = normalizes(data_all)
    data_kda_normalized, min_norm, max_norm = normalizes(data_kda)

    print('Execucao para K = %d' % k)

    inertia = []
    cluster_centers_eff = []
    eff_f = []
    for i in range(k):
        eff_f.append([])

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

        centroids = un_normalizes(
            km.cluster_centers_[:], min_norm_all, max_norm_all)
        file_all.write(
            '\tCentroides da execucao com semente ' + str(i) + ':\n')
        for i in centroids:
            file_all.write('\t' + str(i) + '\n')
        file_all.write('\n')

        # Inertia with F(K - D + A + max(LH, denies))
        for i in centroids:
            cluster_centers_eff.append(i[0] - i[1] + i[2] + max(i[3], i[4]))

        for i, d in enumerate(data_all):
            eff = d[0] - d[1] + d[2] + max(d[3], d[4])

            eff_f[labels[i]].append(abs(cluster_centers_eff[labels[i]] - eff))

        file_all.write('\tDados da metrica F: \n')
        summary(file_all, eff_f, 1)
        file_all.write('\n')

        eff_f.clear()
        eff_f = []
        for i in range(k):
            eff_f.append([])
        cluster_centers_eff.clear()
        centroids.clear()

    file_all.write('Dados da metrica inertia: \n')
    summary(file_all, inertia)

    inertia.clear()

    return

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
        for i in km.cluster_centers_:
            file_kda.write('\t' + str(i) + '\n')
        file_kda.write('\n')

        # Inertia with F(K - D + A)
        for i in km.cluster_centers_:
            cluster_centers_eff.append(i[0] - i[1] + i[2])

        for i, d in enumerate(data_kda):
            eff = d[0] - d[1] + d[2]

            eff_f.append(abs(cluster_centers_eff[labels[i]] - eff))

        file_kda.write('\tDados da metrica F: \n')
        summary(file_kda, eff_f, 1)
        file_kda.write('\n')

        eff_f.clear()
        cluster_centers_eff.clear()

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
        for i in km.cluster_centers_:
            file_all.write('\t' + str(i) + '\n')
        file_all.write('\n')

        # Inertia with F(K - D + A)
        for i in km.cluster_centers_:
            cluster_centers_eff.append(i[0] - i[1] + i[2] + max(i[3], i[4]))

        for i, d in enumerate(data_all):
            eff = d[0] - d[1] + d[2] + max(d[3], d[4])

            eff_f.append(abs(cluster_centers_eff[labels[i]] - eff))

        file_all.write('\tDados da metrica F: \n')
        summary(file_all, eff_f, 1)
        file_all.write('\n')

        eff_f.clear()
        cluster_centers_eff.clear()

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
        for i in km.cluster_centers_:
            file_kda.write('\t' + str(i) + '\n')
        file_kda.write('\n')

        # Inertia with F(K - D + A)
        for i in km.cluster_centers_:
            cluster_centers_eff.append(i[0] - i[1] + i[2])

        for i, d in enumerate(data_kda):
            eff = d[0] - d[1] + d[2]

            eff_f.append(abs(cluster_centers_eff[labels[i]] - eff))

        file_kda.write('\tDados da metrica F: \n')
        summary(file_kda, eff_f, 1)
        file_kda.write('\n')

        eff_f.clear()
        cluster_centers_eff.clear()

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