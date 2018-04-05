from modules.data import read_data, create_data, remove_outliers, normalizes, de_normalize
from modules.clusters import clusterization
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples
import pandas as pd
import matplotlib.cm as cm

# Params
cluster_list = [3, 4, 5, 10]
seed = 0
json_file = 'teste.json'
verbose = False
data = read_data('pruned')

# Start here
output_data = {}
k = 10
attr_set = 'all'

# class
data_norm, min_norm, max_norm = normalizes(data[attr_set])

km = KMeans(n_clusters=k, random_state=seed)
cluster_labels = km.fit_predict(data_norm)

silhouette_avg = silhouette_score(
    data_norm, cluster_labels, metric="euclidean")
sample_silhouette_values = silhouette_samples(
    data_norm, cluster_labels, metric="euclidean")

fig, ax1 = plt.subplots(1, 1)
fig.set_size_inches(18, 7)

y_lower = 10
for i in range(k):
    # Aggregate the silhouette scores for samples belonging to
    # cluster i, and sort them
    ith_cluster_silhouette_values = sample_silhouette_values[cluster_labels == i]

    ith_cluster_silhouette_values.sort()

    size_cluster_i = ith_cluster_silhouette_values.shape[0]
    y_upper = y_lower + size_cluster_i

    color = (sns.color_palette("husl", k))

    ax1.fill_betweenx(np.arange(y_lower, y_upper),
                      0, ith_cluster_silhouette_values,
                      facecolor=color[i], edgecolor=color[i], alpha=0.7)

    # Label the silhouette plots with their cluster numbers at the middle
    ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i + 1))

    # Compute the new y_lower for next plot
    y_lower = y_upper + 10  # 10 for the 0 samples

ax1.set_title("The silhouette plot for the experiment " +
              attr_set + "_" + str(k))
ax1.set_xlabel("The silhouette coefficient values")
ax1.set_ylabel("Cluster label")

# The vertical line for average silhouette score of all the values
ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

ax1.set_yticks([])  # Clear the yaxis labels / ticks
ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

plt.show()
'''
    TODO:
    - Refatorar read data pra TAMBÉM retornar obj pandas e salvar os attrs de correlação
    - Arrumar plots_distribution (feito)
    - Persistir data (feito)
    - Arrumar k-analysis
    - Arrumar k-means_experiments
    - Refatorar os outros códigos (todo nos códigos)
'''
