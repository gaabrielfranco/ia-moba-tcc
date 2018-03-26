from modules.plots import plot_distributions
from modules.data import read_data


def main():
    data = read_data('pruned')
    data_dict = {}

    for index, value in enumerate(data['all']):
        data['all'][index] = (value[0] + value[2]) / value[1]

    data_dict['eff metric'] = data['all']

    plot_distributions(data_dict, ['eff metric'],
                       'files/output_plot_metric/', True, True)

    plot_distributions(data_dict, ['eff metric'],
                       'files/output_plot_metric/', False, False)


if __name__ == "__main__":
    main()
