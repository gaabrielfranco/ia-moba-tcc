from modules.plots import plot_distributions, plot_f
from modules.data import read_data


def main():
    data = read_data('pruned')
    data_dict = {}

    for index, value in enumerate(data['all']):
        data['all'][index] = (value[0] + value[2]) / value[1]

    data_dict['eff_metric'] = data['all']

    plot_distributions(data_dict, ['eff_metric'],
                       'files/output_plot_metric/', False, True)

    plot_distributions(data_dict, ['eff_metric'],
                       'files/output_plot_metric/', False, False)

    _, _, kmeans_pruned = read_data('k-means_experiments')

    plot_f(kmeans_pruned, 'pruned', 'files/output_plot_metric/', False)

    for experiment in kmeans_pruned:
        if experiment.split('_')[0] == 'all' or experiment.split('_')[0] == 'kda':
            for k, cluster in enumerate(kmeans_pruned[experiment]['clusters']):
                data = {}
                data[experiment + '_C' + str(k + 1)] = [0] * \
                    len(kmeans_pruned[experiment]['clusters'])
                for player in cluster:
                    data[experiment + '_C' + str(k + 1)].append(
                        (player[0] + player[2]) / player[1])
                plot_distributions(
                    data, [experiment + '_C' + str(k + 1)], 'files/output_plot_metric/', False, True)
                plot_distributions(
                    data, [experiment + '_C' + str(k + 1)], 'files/output_plot_metric/', False, False)


if __name__ == "__main__":
    main()
