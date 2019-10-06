import pandas as pd
from copy import deepcopy
from modules.plots import radarplot, radarplot_multi, radarplot_comp
import seaborn as sns
from statsmodels.distributions.empirical_distribution import ECDF
from scipy.spatial.distance import cosine
import seaborn as sns
from copy import deepcopy
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from joblib import load


def main():
    df_norm = pd.read_csv(
        "create_database/df_database_norm_w_metrics_all.csv", index_col=0)
    df_cluster = pd.read_csv(
        "create_database/df_database_clusters_all.csv", index_col=0)
    data = pd.read_csv(
        "create_database/df_database_all.csv", index_col=0)
    data_out = pd.read_csv(
        "create_database/df_database_all_w_outliers.csv", index_col=0)

    #metrics = ["GDM", "KDA"]
    metrics = ["GDM"]

    # Plot params
    matplotlib.rcParams['pdf.fonttype'] = 42
    matplotlib.rcParams['ps.fonttype'] = 42
    matplotlib.style.use('ggplot')

    '''
    # Radar plot of VP.Solo
    data_out = (data_out - data_out.min()) / (data_out.max() - data_out.min())
    player_solo = data_out.loc[[134556694]]
    file_name = "VP_solo.pdf"
    columns = list(player_solo.columns)
    for i in range(len(columns)):
        if columns[i] == "firstblood_claimed":
            columns[i] = "firstbloods"

    player_solo.columns = columns
    player_solo.index = [0]
    radarplot(player_solo, file_name, label=None, figsize=(3.8, 2.8))
    '''

    # Multi radarplot for top 10
    file_name = "img/all/starplot_top10.pdf"
    df_ord = df_norm.sort_values(by=["GDM"], ascending=False)
    df_top10_m1 = df_ord.loc[:, data.columns].iloc[:10]
    df_top10_m1.index = [x for x in range(0, 10)]

    df_ord = df_norm.sort_values(by=["KDA"], ascending=False)
    df_top10_kda = df_ord.loc[:, data.columns].iloc[:10]
    df_top10_kda.index = [x for x in range(0, 10)]

    radarplot_comp(df_top10_m1, df_top10_kda, file_name)

    '''
    # Multi radarplot for centroids
    file_name = "img/all/starplot_centroids.pdf"
    km = load("kmeans.joblib")
    centroids = pd.DataFrame(km.cluster_centers_, columns=data.columns)
    label = ["Centroid " + str(i) for i in range(1, 11)]
    radarplot_multi(centroids, file_name, figsize=(3.5, 2.3))
    '''
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
    '''
    '''
    # CDF for each metric per cluster
    folder = "all/ecdf_per_cluster"

    df_norm.insert(len(df_norm.columns), column="cluster",
                   value=df_cluster["cluster"])

    colors_vec = ["#e6194b", "#3cb44b", "#ffe119", "#0082c8",
                  "#f58231", "#911eb4", "#46f0f0", "#f032e6", "#fabebe", "#008080"]

    pallete = sns.color_palette(colors_vec)

    for metric in metrics:
        fig = plt.figure(figsize=(3.8, 2.8))
        plt.rc('font', size=7)
        plt.tight_layout()
        for i in range(10):
            ecdf = ECDF(df_norm[df_norm.cluster == i][metric].values)
            plt.plot(ecdf.x, ecdf.y, label="Cluster " +
                     str(i+1), color=pallete[i])
        xlabel = "KDA values" if metric == "KDA" else "GDM values"
        plt.xlabel(xlabel)
        plt.ylabel("CDF")
        plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8])
        plt.legend()
        file_name = "img/" + folder + "/cdf_" + metric + ".pdf"
        plt.savefig(file_name, bbox_inches='tight', pad_inches=0.01, dpi=600)
        plt.clf()
        print('Graph %s saved.' % file_name)
    '''


if __name__ == "__main__":
    main()
