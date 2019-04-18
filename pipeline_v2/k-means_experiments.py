import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns
import numpy as np
import numbers
from statsmodels.distributions.empirical_distribution import ECDF
from modules.plots import radarplot
from joblib import dump, load


def main():
    # All attributes database
    df = pd.read_csv("create_database/df_database_all.csv", index_col=0)
    folder = "all"

    # Standard attributes database
    #df = pd.read_csv("create_database/df_database.csv", index_col=0)
    #folder = "std"

    # Plot params
    matplotlib.rcParams['pdf.fonttype'] = 42
    matplotlib.rcParams['ps.fonttype'] = 42
    matplotlib.style.use('ggplot')

    # Normalize data
    df = (df - df.min()) / (df.max() - df.min())

    # K-means
    clusterer = KMeans(n_clusters=10, n_jobs=-1).fit(df)
    cluster_labels = clusterer.labels_

    # Persisting the k-means model
    dump(clusterer, "kmeans.joblib")

    # Cluster distribution
    count = [0] * 10

    count = (np.array([(cluster_labels == i).sum()
                       for i in range(0, 10)]) / len(df.index)) * 100
    fig = plt.figure(figsize=(6, 4))
    plt.rc('font', size=7)
    plt.ylabel("Percentage")
    plt.xlabel("Clusters")
    plt.xticks(range(1, 11))
    plt.bar(list(range(1, 11)), count)
    plt.tight_layout()
    file_name = "img/" + folder + "/cluster_dist.png"
    plt.savefig(file_name, bbox_inches='tight', pad_inches=0.01)
    print('Graph %s saved.' % file_name)

    # Centroids starplot
    df_centroids = pd.DataFrame(clusterer.cluster_centers_, columns=df.columns)

    label = ["Centroid " + str(i) for i in range(1, 11)]
    file_name = "img/" + folder + "/cluster_starplot"
    radarplot(df_centroids, file_name, label=label, figsize=(12, 9))

    # Only KDA atributes starplot
    radarplot(df_centroids.loc[:, ["kills", "deaths", "assists"]],
              file_name + "_kda", label=label, figsize=(12, 9))

    # Pairwise centrois startplot
    for i in range(len(df_centroids)):
        for j in range(i + 1, len(df_centroids)):
            file_name = "img/" + folder + \
                "/clusters_centers_pairwise/cluster_starplot_" + \
                str(i) + "_" + str(j)
            radarplot(df_centroids.iloc[[i, j]],
                      file_name, label=label, figsize=(12, 9))

    matplotlib.rcParams['pdf.fonttype'] = 42
    matplotlib.rcParams['ps.fonttype'] = 42
    matplotlib.style.use('ggplot')

    df_centroids = pd.DataFrame(clusterer.cluster_centers_, columns=df.columns)

    label = ["Centroid " + str(i) for i in range(1, 11)]

    candidates = list(df_centroids.columns)
    dimensions = []
    for i, c in enumerate(candidates):
        if isinstance(df_centroids.loc[0, c], numbers.Number):
            dimensions.append(candidates[i])

    dimensions = np.array(dimensions)
    angles = np.linspace(0, 2*np.pi, len(dimensions), endpoint=False)
    angles = np.concatenate((angles, [angles[0]]))

    fig = plt.figure(figsize=(10, 7))
    plt.rc('font', size=7)
    ax = fig.add_subplot(111, polar=True)
    colors_vec = ["#e6194b", "#3cb44b", "#ffe119", "#0082c8",
                  "#f58231", "#911eb4", "#46f0f0", "#f032e6", "#fabebe", "#008080"]
    pallete = sns.color_palette(colors_vec)
    for index, i in enumerate(df_centroids.index):
        values = df_centroids[dimensions].loc[i].values
        values = np.concatenate((values, [values[0]]))
        ax.plot(angles, values, 'o-', linewidth=2,
                label=label[i], color=pallete[index])
        ax.fill(angles, values, alpha=0.25)
    ax.set_thetagrids(angles * 180/np.pi, dimensions)
    ax.grid(True)
    plt.tight_layout()
    plt.legend(loc="center right", bbox_to_anchor=(1.32, 0.5),
               title="Centroid")
    file_name = "img/" + folder + "/cluster_starplot"
    plt.savefig(file_name, bbox_inches='tight', pad_inches=0.01)
    plt.clf()
    print('Graph %s saved.' % file_name)

    # Silhouette score analysis

    n_clusters = 10

    fig = plt.figure(figsize=(3.8, 2.3))
    plt.tight_layout()
    plt.rc('font', size=7)

    #ax1.set_xlim([-0.1, 1])
    #ax1.set_ylim([0, len(df) + (n_clusters + 1) * 10])

    silhouette_avg = silhouette_score(df, cluster_labels)
    print("For n_clusters =", n_clusters,
          "The average silhouette_score is :", silhouette_avg)

    sample_silhouette_values = silhouette_samples(df, cluster_labels)

    y_lower = 10
    for i in range(n_clusters):
        ith_cluster_silhouette_values = sample_silhouette_values[cluster_labels == i]

        ith_cluster_silhouette_values.sort()

        size_cluster_i = ith_cluster_silhouette_values.shape[0]
        y_upper = y_lower + size_cluster_i

        color = (sns.color_palette("husl", 10))
        plt.fill_betweenx(np.arange(y_lower, y_upper),
                          0, ith_cluster_silhouette_values,
                          facecolor=color[i], edgecolor=color[i], alpha=0.7)

        plt.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

        y_lower = y_upper + 10

    plt.xlabel("The silhouette coefficient values")
    plt.ylabel("Cluster label")

    plt.axvline(x=silhouette_avg, color="red", linestyle="--")

    plt.yticks([])
    plt.xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

    plt.tight_layout()
    file_name = "img/" + folder + "/silhouette_score.pdf"
    plt.savefig(file_name, bbox_inches='tight', pad_inches=0.01, dpi=600)
    print('Graph %s saved.' % file_name)
    plt.clf()

    # Create data with cluster result
    df.insert(loc=len(df.columns), column="cluster", value=cluster_labels)
    df.to_csv("create_database/df_database_clusters_" + folder + ".csv")


if __name__ == "__main__":
    main()
