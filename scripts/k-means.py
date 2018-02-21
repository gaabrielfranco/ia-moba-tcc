'''
Implementado por Gabriel Franco
'''

import numpy as np
from sklearn.cluster import KMeans
import pandas as pd
import copy


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


def create_obj(i, inertia, count, centroids, eff, data=None, labels=None, method=None, k=None):
    if data is not None:
        new_obj = {}
        if method == 'all':
            for j in ["kills", "deaths", "assists", "denies", "lh"]:
                new_obj[j] = [[] for x in range(k)]

            for j, k in enumerate(data):
                new_obj["kills"][labels[j]].append(k[0])
                new_obj["deaths"][labels[j]].append(k[1])
                new_obj["assists"][labels[j]].append(k[2])
                new_obj["denies"][labels[j]].append(k[3])
                new_obj["lh"][labels[j]].append(k[4])
        else:
            for j in ["kills", "deaths", "assists"]:
                new_obj[j] = [[] for x in range(k)]

            for j, k in enumerate(data):
                new_obj["kills"][labels[j]].append(k[0])
                new_obj["deaths"][labels[j]].append(k[1])
                new_obj["assists"][labels[j]].append(k[2])

        return new_obj
    else:
        new_obj = {}
        new_obj["semente"] = i
        new_obj["inertia"] = inertia
        new_obj["contagem"] = count
        new_obj["centroids"] = centroids
        new_obj["f"] = []

        for j in range(len(eff)):
            new_obj["f"].append({})
            new_obj["f"][j]["media"] = np.average(eff[j])
            new_obj["f"][j]["desvio"] = np.std(eff[j])
            new_obj["f"][j]["coef_var"] = np.std(eff[j]) / np.average(eff[j])
            new_obj["f"][j]["min"] = np.min(eff[j])
            new_obj["f"][j]["max"] = np.max(eff[j])

        return new_obj


def classification(k, data, method, without_outliers, out_json, eff_json):
    if without_outliers:
        outliers = "sem_poda_de_outlier"
        f = open('files/output_k-means/kmeans_' +
                 method + '_' + str(k) + '.txt', 'w')
    else:
        outliers = "com_poda_de_outlier"
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
    min_inertia = 1000000

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

        print('\tExecucao com poda de outliers')

    for i in range(0, 10):
        print('\t\tExecucao %d' % i)
        f.write('Execucao com semente ' + str(i) + ':\n')
        km = KMeans(n_clusters=k, random_state=i, n_jobs=-1)
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

        if km.inertia_ < min_inertia:
            min_i = i
            min_inertia = km.inertia_
            min_count = count
            min_centroids = centroids[:]
            min_eff_f = eff_f[:]
            min_labels = labels[:]

        eff_f.clear()
        eff_f = []
        for j in range(k):
            eff_f.append([])
        cluster_centers_eff.clear()
        centroids.clear()

    out_json[outliers] = create_obj(
        min_i, min_inertia, min_count, min_centroids, min_eff_f)

    eff_json = create_obj(
        min_i, min_inertia, min_count, min_centroids, min_eff_f, data_norm, min_labels, method, k)

    f.write('Dados da metrica inertia: \n')
    summary(f, inertia)

    inertia.clear()

    f.close()

    return out_json, eff_json


def main():
    data_all = []
    data_kda = []

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

    out_json = {}
    eff_json = {}
    out_final = {"all": {}, "kda": {}}
    eff_final = {"kills": {}, "deaths": {},
                 "assists": {}, "denies": {}, "lh": {}}

    all_att = ["kills", "deaths", "assists", "denies", "lh"]
    kda_att = ["kills", "deaths", "assists"]

    for i in ['all', 'kda']:
        for j in [3, 4, 5]:
            for k in [True, False]:
                if i == 'all':
                    out_json, eff_json = classification(
                        j, data_all, i, k, out_json, eff_json)
                else:
                    out_json, eff_json = classification(
                        j, data_kda, i, k, out_json, eff_json)

                out = ('so' if k else 'co')

                if i == 'all':
                    for att in all_att:
                        for cluster in range(j):
                            eff_final[att][i + '_' + str(j) + '_' + out] = []
                            eff_final[att][i + '_' +
                                           str(j) + '_' + out].append(copy.deepcopy(eff_json[att][cluster]))
                else:
                    for att in kda_att:
                        for cluster in range(j):
                            eff_final[att][i + '_' + str(j) + '_' + out] = []
                            eff_final[att][i + '_' +
                                           str(j) + '_' + out].append(copy.deepcopy(eff_json[att][cluster]))

                eff_json.clear()

            out_final[i][j] = copy.deepcopy(out_json)
            out_json.clear()

    out = pd.DataFrame(out_final)
    out.to_json('files/output_k-means/output_kmeans.json')

    out_2 = pd.DataFrame(eff_final)
    out_2.to_json('files/output_k-means/clusters_kmeans.json')


if __name__ == "__main__":
    main()
