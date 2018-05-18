from statsmodels.distributions.empirical_distribution import ECDF
from modules.data import read_data
import matplotlib.pyplot as plt


def main():
    plt.rcParams["figure.figsize"] = (25, 16)
    plt.rcParams['font.size'] = 18

    plots_path = "files/output_ecdf/"
    data = read_data("df_w_metrics_all")

    for metric in ["kda", "adg", "g", "x"]:
        for cluster in range(0, 10):
            data_cluster = data[data.cluster == cluster]
            ecdf = ECDF(data_cluster[metric])
            plt.plot(ecdf.x, ecdf.y, label="Cluster " + str(cluster + 1))
        plt.legend()
        plt.title(metric + " ECDF")
        # plt.show()
        file_name = plots_path + metric + "_ecdf.png"
        plt.savefig(file_name)
        plt.clf()
        print('Graph %s saved.' % file_name)


if __name__ == "__main__":
    main()
