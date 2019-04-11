import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np
import json


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

    output_data = {}

    # K-means using all attributes
    output_data["all"] = []

    for k in range(3, 101):
        print("Executing experiment %s with %d clusters..." % ("all", k))
        km = KMeans(n_clusters=k, n_jobs=-1)
        km.fit_predict(df)

        # Init data matrix with k lists
        output_data["all"].append(km.inertia_)

    # Save result
    df_out = pd.DataFrame(output_data)
    df_out.to_csv("k_analysis_" + folder + ".csv")

    # Plot params
    matplotlib.rcParams['pdf.fonttype'] = 42
    matplotlib.rcParams['ps.fonttype'] = 42
    matplotlib.style.use('ggplot')
    # Plot result
    fig = plt.figure(figsize=(3.8, 2.3))
    plt.rc('font', size=7)
    plt.plot(list(df_out.index), df_out[folder])
    plt.ylabel("Inertia")
    plt.xlabel("k Value")
    plt.tight_layout()
    file_name = "img/" + folder + "/k_analysis.pdf"
    plt.savefig(file_name, bbox_inches='tight', pad_inches=0.01, dpi=600)
    print('Graph %s saved.' % file_name)


if __name__ == "__main__":
    main()
