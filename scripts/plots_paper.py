from modules.data import read_data
import matplotlib.pyplot as plt
import argparse

# C:\Users\gabgo\Documents\github\ia-moba-tcc\scripts\files\output_k-analysis


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
    # if args.fig1 or args.all:

    # ARRUMAR O PLOT
    if args.fig2 or args.all:
        plots_path = "files/plots_paper/"

        file_name = plots_path + "players_distribution_per_cluster"
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
