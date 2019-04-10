import pandas as pd
from scipy.stats import kendalltau
from copy import deepcopy


def main():
    df_metrics = pd.read_csv(
        "feature_selection/output_ga/all/top10_metrics_07.csv", index_col=0)
    df = pd.read_csv("create_database/df_database_all.csv", index_col=0)

    # Normalize data
    df = (df - df.min()) / (df.max() - df.min())

    # DF with metrics
    df_w_metrics = deepcopy(df)

    kendall = pd.DataFrame(columns=["metric_1", "metric_2", "tau", "p_value"])

    # Adding KDA
    df_metrics.loc[len(df_metrics)] = ["kills,deaths,assists,", "0.0"]

    for i in range(len(df_metrics)):
        attr_i = list(df_metrics.at[i, "Solution"].split(","))
        attr_i.remove("")
        a_i = deepcopy(attr_i)
        attr_i.remove("deaths")
        df_attr_i = df.loc[:, attr_i]
        metric_i = df_attr_i.sum(axis=1) / (df["deaths"] + 10e-5)

        name = "Metric_" + str(i + 1) if i < len(df_metrics) - 1 else "KDA"
        df_w_metrics.insert(len(df_w_metrics.columns), column=name, value=metric_i)
        for j in range(i + 1, len(df_metrics)):
            attr_j = list(df_metrics.at[j, "Solution"].split(","))
            attr_j.remove("")
            a_j = deepcopy(attr_j)
            attr_j.remove("deaths")
            df_attr_j = df.loc[:, attr_j]
                
            metric_j = df_attr_j.sum(axis=1) / (df["deaths"] + 10e-5)

            tau, p_value = kendalltau(metric_i, metric_j)

            kendall.loc[len(kendall.index)] = [a_i, a_j, tau, p_value]

    df_w_metrics.to_csv("create_database/df_database_norm_w_metrics_all.csv")
    kendall.sort_values(by=["tau"], ascending=False).to_csv(
        "kendall_all_07.csv")


if __name__ == "__main__":
    main()
