from modules.data import read_data
import matplotlib
import matplotlib.pyplot as plt
import argparse
import json


def main():
    parser = argparse.ArgumentParser(
        description='Plots for paper', prog="plots_paper.py")
    parser.add_argument('--all', '-a', action='store_true',
                        help='plot all figures (defaut = False)')
    parser.add_argument('--fig1', '-f1', action='store_true',
                        help='plot fig1 - inértia x k (defaut = False)')
    parser.add_argument('--fig2', '-f2', action='store_true',
                        help='plot fig2 - players distribution per cluster (defaut = False)')
    parser.add_argument('--show', '-s', action='store_true',
                        help='show plots (defaut = False)')
    args = parser.parse_args()

    plots_path = "files/plots_paper/"
    matplotlib.rcParams['pdf.fonttype'] = 42
    matplotlib.rcParams['ps.fonttype'] = 42
    # matplotlib.use('Agg')
    matplotlib.style.use('ggplot')

    if args.fig1 or args.all:
        file_name = plots_path + "inertia_x_k.pdf"

        with open("files/output_k-analysis/output_k_analysis.json") as file:
            data = json.load(file)

        fig = plt.figure(figsize=(3.5, 2.5))
        plt.rc('font', size=7)
        plt.ylabel("Inertia")
        plt.xlabel("Number of clusters")
        plt.xticks(list(range(0, 101, 10)))

        plt.plot(data["all"]["n_clusters"], data["all"]["inertia"])
        plt.xlim((0, 100))
        plt.tight_layout()
        plt.savefig(file_name, bbox_inches='tight', pad_inches=0.01)
        if args.show:
            plt.show()
        plt.clf()

    # ARRUMAR O PLOT
    if args.fig2 or args.all:
        file_name = plots_path + "players_distribution_per_cluster.pdf"
        data = read_data("df_w_metrics_all")

        clusters = data["cluster"].values
        num_occur = [0] * (max(clusters) + 1)

        for i in clusters:
            num_occur[i] += 1

        labels = []

        for i in num_occur:
            labels.append((i / len(clusters)) * 100)

        plt.bar(range(1, max(clusters) + 2), labels)
        plt.ylabel("Porcentagem")
        plt.xlabel("Número do grupo")
        plt.xticks(range(1, max(clusters) + 2))
        plt.title("Distribuição dos jogadores por grupo")
        plt.savefig(file_name)
        print('Graph %s saved.' % file_name)
        if args.show:
            plt.show()
        plt.clf()


if __name__ == "__main__":
    main()
