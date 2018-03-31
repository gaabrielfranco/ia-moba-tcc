from modules.data import read_data, create_data, remove_outliers
from modules.clusters import clusterization
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
#create_data('files/attributes.txt', True, False)
#a = read_data('corr_pruned')
kmeans, kmeans_corr, kmeans_pruned = read_data('k-means_experiments')

cont = 0
f = {}
for experiment in kmeans_pruned:
    if experiment.split('_')[0] == 'all' or experiment.split('_')[0] == 'kda':
        f[experiment] = {}
        for k, cluster in enumerate(kmeans_pruned[experiment]['clusters']):
            f[experiment][k] = 0
            for player in cluster:
                f[experiment][k] += (player[0] + player[2]) / player[1]
            f[experiment][k] /= len(cluster)

plt.rcParams["figure.figsize"] = (25, 16)
plt.rcParams['font.size'] = 12.0
data = []
labels = []
for experiment in f:
    for k, cluster in enumerate(f[experiment]):
        data.append(f[experiment][k])
        labels.append(experiment + ' - C' + str(k + 1))

pallete = sns.color_palette("Blues", len(data))

groups = np.arange(len(data))

plt.bar(groups, data, 0.35, tick_label=labels, color=pallete)
plt.xticks(groups, labels, rotation=90)
plt.title("F for each cluster")
plt.savefig('teste.png')

'''
    TODO:
    - Refatorar read data pra TAMBÉM retornar obj pandas e salvar os attrs de correlação
    - Arrumar plots_distribution (feito)
    - Persistir data (feito)
    - Arrumar k-analysis
    - Arrumar k-means_experiments
    - Refatorar os outros códigos (todo nos códigos)
'''
