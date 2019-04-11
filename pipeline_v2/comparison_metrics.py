import pandas as pd
from copy import deepcopy
from modules.plots import radarplot
import seaborn as sns
from statsmodels.distributions.empirical_distribution import ECDF
import matplotlib.pyplot as plt
from scipy.spatial.distance import cosine
import seaborn as sns
from copy import deepcopy
import numpy as np


def main():
    df = pd.read_csv(
        "create_database/df_database_w_metrics_all.csv", index_col=0)
    df_norm = pd.read_csv(
        "create_database/df_database_norm_w_metrics_all.csv", index_col=0)
    df_cluster = pd.read_csv(
        "create_database/df_database_clusters_all.csv", index_col=0)
    data = pd.read_csv(
        "create_database/df_database_all.csv", index_col=0)
    metrics = ["Metric_" + str(i) for i in range(1, 11)]
    metrics.append("KDA")
    '''
    # Radarplots are a bad choice 'cause we've many attributes
    # Radarplots of top10 for each metric
    folder = "all/starplots_top10"

    for metric in metrics:
        df_ord = df_norm.sort_values(by=[metric], ascending=False)
        df_top10 = df_ord.loc[:, data.columns].iloc[:10]
        df_top10.index = list(range(10))
        label = ["Top " + str(i) for i in range(1, 11)]
        file_name = "img/" + folder + "/" + metric + "_starplot"

        radarplot(df_top10, file_name, label=label, figsize=(12, 9))

    # CDF for each metric per cluster
    folder = "all/ecdf_per_cluster"

    df_norm.insert(len(df_norm.columns), column="cluster",
                   value=df_cluster["cluster"])

    for metric in metrics:
        fig = plt.figure(figsize=(5.55, 4.7))
        plt.rc('font', size=7)
        for i in range(10):
            ecdf = ECDF(df_norm[df_norm.cluster == i][metric].values)
            plt.plot(ecdf.x, ecdf.y, label="Cluster " + str(i+1))
        plt.legend()
        plt.tight_layout()
        file_name = "img/" + folder + "/" + metric
        plt.savefig(file_name, bbox_inches='tight', pad_inches=0.01)
        plt.clf()
        print('Graph %s saved.' % file_name)

    '''
    # Comparison between metrics using cosine distance
    folder = "all/cosine_comparison"
    sns.set()

    for i in range(len(metrics)):
        # Top 10 in Metric i
        df_ord = df_norm.sort_values(by=[metrics[i]], ascending=False)
        df_top10 = df_ord.loc[:, data.columns].iloc[:10]

        index = df_top10.index
        cont = 0
        data_matrix = []
        arr = []
        for idx in range(len(index)):
            for j in range(len(index)):
                dist = cosine(df_top10.loc[index[idx]],
                              df_top10.loc[index[j]])
                arr.append(dist)
            data_matrix.append(deepcopy(arr))
            arr.clear()
        data_matrix = np.array(data_matrix)
        mask = np.zeros_like(data_matrix)
        mask[np.triu_indices_from(mask)] = True
        with sns.axes_style("white"):
            fig = plt.figure(figsize=(10, 8))
            plt.rc('font', size=7)
            ax = sns.heatmap(data_matrix, vmin=0, vmax=1,
                             annot=True, fmt=".4f", square=True, mask=mask)
            ax.set_xticklabels(["Top " + str(x + 1) for x in range(10)])
            ax.set_yticklabels(["Top " + str(x + 1) for x in range(10)])
            plt.tight_layout()
            file_name = "img/" + folder + "/" + metrics[i]
            plt.savefig(file_name, bbox_inches='tight', pad_inches=0.01)
            plt.clf()
            print('Graph %s saved.' % file_name)


if __name__ == "__main__":
    main()
