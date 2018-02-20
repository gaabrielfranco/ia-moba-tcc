import pandas as pd
import matplotlib.pyplot as plt
import sys
import numpy as np


def normalizes(x):
    x_norm = []
    minimum = np.min(x)
    maximum = np.max(x)
    for i in x:
        x_norm.append((i - minimum) / (maximum - minimum))

    return x_norm


def plot_kmeans():
    data_km = pd.read_json('files/output_k-means/clusters_kmeans.json')

    for k, v in data_km.items():
        data = []
        labels = []
        for i, j in v.items():
            if j is not None:
                data.append(j)
                labels.append(i)

        plt.boxplot(data, labels=labels)
        plt.title(k)
        plt.savefig('files/output_plots/k-means/plot_attribute_' + k + '.png')
        plt.clf()


def plot_attributes():
    data_att = pd.read_json(
        'files/output_attributes_analysis/output_attributes.json')

    for k, v in data_att.items():
        plt.boxplot(v, labels=[k])
        plt.title(k)
        plt.savefig(
            'files/output_plots/attributes/plot_attribute_' + k + '.png')
        plt.clf()


def plot_all():
    data_att = pd.read_json(
        'files/output_attributes_analysis/output_attributes.json')
    data_km = pd.read_json('files/output_k-means/clusters_kmeans.json')

    for k, v in data_km.items():
        data = []
        labels = []
        for i, j in v.items():
            if j is not None:
                data.append(j)
                labels.append(i)

        att_general = []
        for i in data_att[k]:
            att_general.append(i)

        att_general = normalizes(att_general)

        data.append(att_general)
        labels.append('general')

        plt.boxplot(data, labels=labels)
        plt.title(k)
        plt.savefig('files/output_plots/all/plot_attribute_' + k + '.png')
        plt.clf()


def main():
    if len(sys.argv) == 1 or len(sys.argv) > 2:
        print('Opções:\n')
        print('boxplot.py -att : Plota os dados dos atributos')
        print('boxplot.py -km : Plota os dados do k-means')
        print('boxplot.py -all : Plota os dados do k-means e dos atributos juntos')
    elif sys.argv[1] == '-att':
        print('Plot dos atributos')
        plot_attributes()
    elif sys.argv[1] == '-km':
        print('Plot do k-means')
        plot_kmeans()
    elif sys.argv[1] == '-all':
        print('Plot de todos juntos')
        plot_all()
    else:
        print('Opções:\n')
        print('boxplot.py -att : Plota os dados dos atributos')
        print('boxplot.py -km : Plota os dados do k-means')
        print('boxplot.py -all : Plota os dados do k-means e dos atributos juntos')


if __name__ == "__main__":
    main()
