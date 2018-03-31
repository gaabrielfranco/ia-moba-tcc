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

    kmeans, kmeans_corr, kmeans_pruned = read_data('k-means_experiments')

    plot_f(kmeans_pruned, 'pruned', 'files/output_plot_metric/', False)


if __name__ == "__main__":
    main()
