from joblib import load
import pandas as pd
from modules.plots import radarplot


def main():
    df = pd.read_csv("create_database/df_database_all.csv", index_col=0)
    folder = "all"

    clf = load("kmeans.joblib")

    df_centroids = pd.DataFrame(clf.cluster_centers_, columns=df.columns)

    label = ["Centroid " + str(i) for i in range(1, 11)]
    file_name = "img/" + folder + "/metric_starplot"
    radarplot(df_centroids.loc[:, ["deaths", "gold_per_min", "xp_per_min", "hero_healing"]],
              file_name, label=label, figsize=(12, 9))


if __name__ == "__main__":
    main()
