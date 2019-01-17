import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np
import json


def main():
    df = pd.read_csv("create_database/df_database.csv", index_col=0)

    # Normalize data
    df = (df - df.min()) / (df.max() - df.min())

    output_data = {}

    for attr in df.keys():
        output_data[attr] = []

        for k in range(3, 101):
            print("Executing experiment %s with %d clusters..." % (attr, k))
            km = KMeans(n_clusters=k, n_jobs=-1)
            km.fit_predict(df[attr].values.reshape(-1, 1))

            # Init data matrix with k lists
            output_data[attr].append(km.inertia_)

    # All attributes
    output_data["all"] = []

    for k in range(3, 101):
        print("Executing experiment %s with %d clusters..." % ("all", k))
        km = KMeans(n_clusters=k, n_jobs=-1)
        km.fit_predict(df)

        # Init data matrix with k lists
        output_data["all"].append(km.inertia_)

    # Save result
    df_out = pd.DataFrame(output_data)
    df_out.to_csv("k_analysis.csv")

    # Plot result
    df_out = (df_out - df_out.min()) / (df_out.max() - df_out.min())
    df_out.plot()
    plt.show()


if __name__ == "__main__":
    main()
