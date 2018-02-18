import pandas as pd
import matplotlib.pyplot as plt
import sys


def plot_attributes_analysis():
    data = pd.read_json(
        'files/output_attributes_analysis/output_attribute_analysis.json')

    for k, v in data.items():
        data_plot = [[] for x in range(5)]

        for j in range(1, 5):
            data_plot[0].append(v[j]["media"])
            data_plot[1].append(v[j]["desvio"])
            data_plot[2].append(v[j]["coef_var"])
            data_plot[3].append(v[j]["min"])
            data_plot[4].append(v[j]["max"])

        plt.boxplot(data_plot, labels=[
                    "medias", "desvios", "coef. var", "min", "max"])
        plt.title(k)
        plt.savefig('files/output_plots/plot_' + k + '.png')
        plt.clf()


def plot_k_means():
    data = pd.read_json('files/output_k-means/output_kmeans.json')


def main():
    if len(sys.argv) == 1 or len(sys.argv) > 2:
        print('Opções:\n')
        print('box_plot.py -att : Plota a análise dos atributos')
        print('box_plot.py -km : Plota os dados do k-means')
        print('box_plot.py -all : Plota os dois acima')
    elif sys.argv[1] == '-att':
        print('Plot da análise dos atributos')
        plot_attributes_analysis()
    elif sys.argv[1] == '-km':
        # plotar k-means
        print('Plot do k-means')
        print("oi")
    elif sys.argv[1] == '-all':
        # plotar os dois
        print('Plot de ambos')
        plot_attributes_analysis()
    else:
        print('Opções:\n')
        print('box_plot.py -att : Plota a análise dos atributos')
        print('box_plot.py -km : Plota os dados do k-means')
        print('box_plot.py -all : Plota os dois acima')


if __name__ == "__main__":
    main()
