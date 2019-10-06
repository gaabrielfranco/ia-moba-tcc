import pandas as pd
from scipy.stats import kendalltau
from copy import deepcopy


def main():
    df = pd.read_csv("create_database/df_database_all.csv", index_col=0)

    # Normalize data
    df = (df - df.min()) / (df.max() - df.min())

    # Metrics
    kda = ["kills", "assists"]
    gdm = ["camps_stacked",
           "gold_per_min", "hero_healing", "obs_placed"]

    df_kda = df[kda].sum(axis=1) / (df["deaths"] + 1)
    df_gdm = df[gdm].sum(axis=1) / (df["deaths"] + 1)

    tau, p_value = kendalltau(df_kda, df_gdm)

    print("Tau = %.4f, p-value = %f" % (tau, p_value))

    df.insert(len(df.columns), "KDA", df_kda)
    df.insert(len(df.columns), "GDM", df_gdm)

    df.to_csv("create_database/df_database_norm_w_metrics_all.csv")


if __name__ == "__main__":
    main()
