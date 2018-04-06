from modules.data import read_data, normalizes
import pandas as pd
import matplotlib.pyplot as plt
import argparse


def main():
    plt.rcParams["figure.figsize"] = (25, 16)
    plt.rcParams['font.size'] = 12.0

    plots_path = 'files/output_plot_hexbin/'
    show_plots = False

    parser = argparse.ArgumentParser(
        description='Plot hexbin from data pruned', prog="plot_hexbin.py")
    parser.add_argument('--show', '-s', action='store_true',
                        help='shows the plots (defaut = False)')

    args = parser.parse_args()
    show_plots = args.show

    data = read_data('df_data_pruned')

    for experiment in data:
        data[experiment] = normalizes(data[experiment])[0]

    for i, x in enumerate(data):
        for j, y in enumerate(data):
            if x != y and i <= j:
                data.plot.hexbin(x=x, y=y, gridsize=25)
                plt.title('Hexbin plot: ' + x + ' and ' + y)
                if show_plots:
                    plt.show()
                file_name = plots_path + x + '_' + y
                plt.savefig(file_name)
                plt.clf()
                print('Graph %s saved.' % file_name)


if __name__ == "__main__":
    main()
