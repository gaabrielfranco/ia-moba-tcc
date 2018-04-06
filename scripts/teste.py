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

data = read_data('df_data_pruned')

for experiment in data:
    data[experiment] = normalizes(data[experiment])[0]

for x in data:
    for y in data:
        if x != y:
            data.plot.hexbin(x=x, y=y, gridsize=25)
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
