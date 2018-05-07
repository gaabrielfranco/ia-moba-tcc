#!/usr/bin/env python3

'''
    Código quebrado.
    TODO: 
        - rerun nos k-means usando o dataframe? (acho a opção melhor)
        - fazer std e coef. variação
'''
from modules.data import read_data, normalizes
import argparse
import numpy as np
import matplotlib.pyplot as plt


def main():
    parser = argparse.ArgumentParser(
        description='Comparison between the four metrics', prog="metrics_comparation.py")
    parser.add_argument('--with_outliers', '-wo', action='store_true',
                        help='use data with outliers (defaut = False)')

    args = parser.parse_args()
    with_outliers = args.with_outliers

    if with_outliers:
        data = read_data('df_data')
        k_means, _, _ = read_data('k-means_experiments')
    else:
        data = read_data('df_data_pruned')
        _, _, k_means = read_data('k-means_experiments')

    minimum = []
    maximum = []

    for attr in ["kills", "deaths", "assists", "denies", "gpm", "hd", "hh", "lh", "xpm"]:
        minimum.append(data.min()[attr])
        maximum.append(data.max()[attr])

    for experiment in k_means:
        if experiment.split('_')[0] == 'all':
            metric_kda = []
            metric_adg = []
            metric_g = []
            metric_x = []
            for label in k_means[experiment]:
                if label == 'clusters':
                    for cluster in k_means[experiment][label]:
                        kda, adg, g, x = 0.0, 0.0, 0.0, 0.0
                        for player in cluster:
                            player_norm = (np.array(player) -
                                           np.array(minimum)) / (np.array(maximum) - np.array(minimum))

                            kda += (player_norm[0] +
                                    player_norm[2]) / (1 + player_norm[1])

                            adg += (player_norm[2] + player_norm[3] +
                                    player_norm[4] + player_norm[6]) / (1 + player_norm[1])

                            g += (player_norm[4] +
                                  player_norm[6]) / (1 + player_norm[1])

                            x += (player_norm[8] +
                                  player_norm[6]) / (1 + player_norm[1])

                        metric_kda.append(kda/len(cluster))
                        metric_adg.append(adg/len(cluster))
                        metric_g.append(g/len(cluster))
                        metric_x.append(x/len(cluster))

            x = np.arange(len(metric_kda))

            metric_kda.sort()
            metric_adg.sort()
            metric_g.sort()
            metric_x.sort()

            f, axarr = plt.subplots(2, 2)
            f.suptitle(
                "Distribution of average metric value per cluster", fontsize=14)

            axarr[0, 0].bar(x, metric_kda)
            axarr[0, 0].set_title('metric_kda with experiment ' + experiment)
            axarr[0, 0].set_xticks(x)
            axarr[0, 0].set_xlabel('Clusters')
            axarr[0, 0].set_ylabel('Average Metric Value')

            axarr[0, 1].bar(x, metric_adg)
            axarr[0, 1].set_title('metric_adg with experiment ' + experiment)
            axarr[0, 1].set_xticks(x)
            axarr[0, 1].set_xlabel('Clusters')
            axarr[0, 1].set_ylabel('Average Metric Value')

            axarr[1, 0].bar(x, metric_g)
            axarr[1, 0].set_title('metric_g with experiment ' + experiment)
            axarr[1, 0].set_xticks(x)
            axarr[1, 0].set_xlabel('Clusters')
            axarr[1, 0].set_ylabel('Average Metric Value')

            axarr[1, 1].bar(x, metric_x)
            axarr[1, 1].set_title('metric_x with experiment ' + experiment)
            axarr[1, 1].set_xticks(x)
            axarr[1, 1].set_xlabel('Clusters')
            axarr[1, 1].set_ylabel('Average Metric Value')

            # Fine-tune figure; hide x ticks for top plots and y ticks for right plots
            plt.setp([a.get_xticklabels() for a in axarr[0, :]], visible=False)
            plt.setp([a.get_yticklabels() for a in axarr[:, 1]], visible=False)

            plt.show()


if __name__ == "__main__":
    main()
