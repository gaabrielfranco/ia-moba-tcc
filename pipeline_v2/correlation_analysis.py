import pandas as pd
import seaborn as sns
from statsmodels.distributions.empirical_distribution import ECDF
import matplotlib.pyplot as plt


def main():
    df = pd.read_csv("create_database/df_database_all.csv", index_col=0)
    folder = "all"

    # ECDF
    fig = plt.figure(figsize=(5.55, 4.7))
    plt.rc('font', size=7)
    colors_vec = ["#e6194b", "#3cb44b", "#ffe119", "#0082c8",
                  "#f58231", "#911eb4", "#46f0f0", "#f032e6", "#fabebe", "#008080"]

    pallete = sns.color_palette(colors_vec)

    df_corr = df.corr()

    for attr in df_corr:
        ecdf = ECDF(df_corr[attr].drop(labels=[attr]))
        plt.plot(ecdf.x, ecdf.y, label=attr)  # , color=pallete[cluster])
    plt.legend()
    plt.tight_layout()
    file_name = "img/" + folder + "/correlation/ecdf"
    plt.savefig(file_name, bbox_inches='tight', pad_inches=0.01)
    plt.clf()
    print('Graph %s saved.' % file_name)


if __name__ == "__main__":
    main()
