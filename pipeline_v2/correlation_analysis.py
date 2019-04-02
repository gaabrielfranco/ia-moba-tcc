import pandas as pd
import seaborn as sns
from statsmodels.distributions.empirical_distribution import ECDF
import matplotlib.pyplot as plt


def main():
    df = pd.read_csv("create_database/df_database_all.csv", index_col=0)
    folder = "all"
    fig = plt.figure(figsize=(5.55, 4.7))
    plt.rc('font', size=7)

    df_corr = df.corr()
    corr_values = []
    for idx, attr in enumerate(df_corr):
        corr_values += list(df_corr[attr].iloc[idx+1:].values)

    ecdf = ECDF(corr_values)
    plt.plot(ecdf.x, ecdf.y, label="Valores de correlação abaixo da diagonal principal")
    plt.legend()
    plt.tight_layout()
    file_name = "img/" + folder + "/ecdf_corr"
    plt.savefig(file_name, bbox_inches='tight', pad_inches=0.01)
    plt.clf()
    print('Graph %s saved.' % file_name)

if __name__ == "__main__":
    main()
