#!/usr/bin/env python3

from modules.data import read_data
import argparse
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import pandas as pd
from scipy.stats import kendalltau

# =============================================================================
#   Reunião de sexta (11/05)
#       - Computar dois vetores, cada um com uma métrica por jogador de toda base (data já tem isso)
#       - Pegar os k melhores jogadores e fazer a correlação entre as métricas, variando o k
#       - Fazer esse procedimento por cluster também
#       - Fazer startplot dos 10 melhores jogadores de cada métrica agrupando os atributos
#         pelo jeito decidido na reunião
#       - Pegar o resto das coisas pra fazer no log da reunião
#
#   IDEIA DO GIOVANNI (TEM FOTO NO CELULAR):
#       -CDF P(X <= x) - implementação ECDF no Stats Model
# =============================================================================


def radarplot_same_img(data, plots_path, show_plots=False):
    plt.rcParams["figure.figsize"] = (30, 20)
    plt.rcParams['font.size'] = 12.0

    for metric in ['kda', 'adg', 'g', 'x']:
        cx, cy = 0, 0
        f, axarr = plt.subplots(4, 3, subplot_kw=dict(projection='polar'))
        for cluster_label in range(0, 10):
            data_cluster = data[data.cluster == cluster_label]

            data_cluster = data_cluster.sort_values(
                by=[metric], ascending=False)[:10]

            label = {}
            for index, player in enumerate(data_cluster.index):
                label[player] = 'Top ' + str(index + 1)
            exclude_list = ['kda', 'adg', 'g', 'x', 'cluster']
            data_cluster = data_cluster.drop(exclude_list, axis=1)

            colunms_order = ['kills', 'hd', 'assists', 'hh',
                             'deaths', 'denies', 'lh', 'gpm', 'xpm']
            data_cluster = data_cluster.reindex(columns=colunms_order)
            dimensions = np.array(list(data_cluster.columns))
            angles = np.linspace(0, 2*np.pi, len(dimensions), endpoint=False)
            angles = np.concatenate((angles, [angles[0]]))

            for i in data_cluster.index:
                values = data_cluster[dimensions].loc[i].values
                values = np.concatenate((values, [values[0]]))
                axarr[cx, cy].plot(angles, values, 'o-', linewidth=2,
                                   label=label[i])
                axarr[cx, cy].fill(angles, values, alpha=0.25)
            axarr[cx, cy].set_thetagrids(angles * 180/np.pi, dimensions)
            axarr[cx, cy].set_title('Cluster ' + str(cluster_label))
            axarr[cx, cy].grid(True)

            cy += 1
            if cy > 2:
                cy = 0
                cx += 1

        axarr[3, 0].legend(loc='best', bbox_to_anchor=(1.1, 0.5))
        f.suptitle('Top 10 ' + metric + ' per cluster', fontsize=20)
        f.delaxes(axarr.flatten()[10])
        f.delaxes(axarr.flatten()[11])
        f.subplots_adjust(wspace=0.4, hspace=0.4)
        if show_plots:
            plt.show()
        file_name = plots_path + metric + '_per_cluster'
        plt.savefig(file_name)
        plt.clf()
        print('Graph %s saved.' % file_name)


def radarplot(data, file_name, exclude_list, title=None, show_plots=False):
    plt.rcParams["figure.figsize"] = (25, 16)
    plt.rcParams['font.size'] = 18.0

    label = {}
    for index, player in enumerate(data.index):
        label[player] = 'Top ' + str(index + 1)
    data = data.drop(exclude_list, axis=1)

    colunms_order = ['kills', 'hd', 'assists', 'hh',
                     'deaths', 'denies', 'lh', 'gpm', 'xpm']
    data = data.reindex(columns=colunms_order)

    dimensions = np.array(list(data.columns))
    angles = np.linspace(0, 2*np.pi, len(dimensions), endpoint=False)
    angles = np.concatenate((angles, [angles[0]]))

    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)
    for i in data.index:
        values = data[dimensions].loc[i].values
        values = np.concatenate((values, [values[0]]))
        ax.plot(angles, values, 'o-', linewidth=2,
                label=label[i])
        ax.fill(angles, values, alpha=0.25)
    ax.set_thetagrids(angles * 180/np.pi, dimensions)
    if title is not None:
        ax.set_title(title)
    ax.grid(True)
    plt.legend(loc='center left', bbox_to_anchor=(1.1, 0.5))
    if show_plots:
        plt.show()
    plt.savefig(file_name)
    plt.clf()
    print('Graph %s saved.' % file_name)


def main():
    default_path = 'files/output_metrics_comparison_new/'

    parser = argparse.ArgumentParser(
        description='Comparison between the four metrics', prog="metrics_comparation.py")
    parser.add_argument('--with_outliers', '-wo', action='store_true',
                        help='use data with outliers (defaut = False)')
    parser.add_argument('--n_clusters', '-k', type=int, default=10,
                        help='number of clusters (default = 10)')
    parser.add_argument('--output_path', '-op', default=default_path,
                        help='path to store output data (default = %s)' % default_path)
    parser.add_argument('--show_plots', '-sp', action='store_true',
                        help='show plots during execution (default = False)')
    parser.add_argument('--projection', '-prj', choices=['all', 'kda', 'adg', 'g', 'x'],
                        default='all', help='projection of the database used for clustering data (all | kda | adg | g | x) (default=all)')

    args = parser.parse_args()

    with_outliers = args.with_outliers

    if with_outliers:
        data = read_data('df_data')
    else:
        data = read_data('df_data_pruned')

    if not args.output_path.endswith('/'):
        output_path = args.output_path + '/' + args.projection + '/'
    else:
        output_path = args.output_path + args.projection + '/'

    # Normalizing data
    for col in data.columns:
        data[col] = (data[col] - data[col].min()) / \
            (data[col].max() - data[col].min())

    # Clustering
    km = KMeans(n_clusters=args.n_clusters, random_state=None, n_jobs=-1)
    if args.projection == 'all':
        labels = km.fit_predict(data)
    else:
        if args.projection == 'kda':
            attr_list = ['kills', 'assists', 'deaths']
        elif args.projection == 'adg':
            attr_list = ['denies', 'assists', 'deaths', 'gpm', 'hh']
        elif args.projection == 'g':
            attr_list = ['deaths', 'gpm', 'hh']
        elif args.projection == 'x':
            attr_list = ['deaths', 'xpm', 'hh']
        labels = km.fit_predict(data[attr_list])

    # Compute metrics and add them to the database, as well as the clusters labels
    kda = (data['kills'] + data['assists']) / (1 + data['deaths'])
    adg = (data['denies'] + data['assists'] +
           data['gpm'] + data['hh']) / (1 + data['deaths'])
    g = (data['gpm'] + data['hh']) / (1 + data['deaths'])
    x = (data['xpm'] + data['hh']) / (1 + data['deaths'])

    data.insert(len(data.columns), 'kda', kda)
    data.insert(len(data.columns), 'adg', adg)
    data.insert(len(data.columns), 'g', g)
    data.insert(len(data.columns), 'x', x)
    data.insert(len(data.columns), 'cluster', labels)

    # Maximum values in each metric
    max_data = {}
    for k in [10, 100, 500, 1000, 2000]:
        max_kda = data['kda'].sort_values(ascending=False)[:k]
        max_adg = data['adg'].sort_values(ascending=False)[:k]
        max_g = data['g'].sort_values(ascending=False)[:k]
        max_x = data['x'].sort_values(ascending=False)[:k]
        max_data[k] = {'kda e adg': {}, 'kda e g': {},
                       'kda e x': {}, 'adg e g': {}, 'g e x': {}}

        cont = 0
        cont_eq = 0
        for index, value in enumerate(max_kda.index):
            if value in max_adg.index:
                cont += 1
            if value == max_adg.index[index]:
                cont_eq += 1

        max_data[k]['kda e adg'] = {'Número de repetições': cont,
                                    'Valores na mesma posição': cont_eq}

        cont = 0
        cont_eq = 0
        for index, value in enumerate(max_kda.index):
            if value in max_g.index:
                cont += 1
            if value == max_g.index[index]:
                cont_eq += 1

        max_data[k]['kda e g'] = {'Número de repetições': cont,
                                  'Valores na mesma posição': cont_eq}

        cont = 0
        cont_eq = 0
        for index, value in enumerate(max_kda.index):
            if value in max_x.index:
                cont += 1
            if value == max_x.index[index]:
                cont_eq += 1

        max_data[k]['kda e x'] = {'Número de repetições': cont,
                                  'Valores na mesma posição': cont_eq}

        cont = 0
        cont_eq = 0
        for index, value in enumerate(max_adg.index):
            if value in max_g.index:
                cont += 1
            if value == max_g.index[index]:
                cont_eq += 1

        max_data[k]['adg e g'] = {'Número de repetições': cont,
                                  'Valores na mesma posição': cont_eq}

        cont = 0
        cont_eq = 0
        for index, value in enumerate(max_x.index):
            if value in max_g.index:
                cont += 1
            if value == max_g.index[index]:
                cont_eq += 1

        max_data[k]['g e x'] = {'Número de repetições': cont,
                                'Valores na mesma posição': cont_eq}

    max_data_df = pd.DataFrame(max_data)
    max_data_df.to_csv(output_path + 'max_values_comparison.csv')

    # Top 10 Radar Plot
    top_10_kda = data.sort_values(by=['kda'], ascending=False)[:10]
    top_10_adg = data.sort_values(by=['adg'], ascending=False)[:10]
    top_10_g = data.sort_values(by=['g'], ascending=False)[:10]
    top_10_x = data.sort_values(by=['x'], ascending=False)[:10]

    exclude_list = ['kda', 'adg', 'g', 'x', 'cluster']

    radarplot(top_10_kda, output_path + 'radar_plot_top_10_kda.png', exclude_list,
              'Top 10 by KDA')

    radarplot(top_10_adg, output_path + 'radar_plot_top_10_adg.png', exclude_list,
              'Top 10 by ADG')

    radarplot(top_10_g, output_path + 'radar_plot_top_10_g.png', exclude_list,
              'Top 10 by G')

    radarplot(top_10_x, output_path + 'radar_plot_top_10_x.png', exclude_list,
              'Top 10 by X')

    # Top 10 per cluster Radar Plot
    for cluster_label in range(0, 10):
        data_cluster = data[data.cluster == cluster_label]

        top_10 = data_cluster.sort_values(by=['kda'], ascending=False)[:10]
        radarplot(top_10, output_path + 'radar_plot_top_10_kda_C' + str(cluster_label) + '.png', exclude_list,
                  'Cluster ' + str(cluster_label) + ' - Top 10 by KDA')

        top_10 = data_cluster.sort_values(by=['adg'], ascending=False)[:10]
        radarplot(top_10, output_path + 'radar_plot_top_10_adg_C' + str(cluster_label) + '.png', exclude_list,
                  'Cluster ' + str(cluster_label) + ' - Top 10 by ADG')

        top_10 = data_cluster.sort_values(by=['g'], ascending=False)[:10]
        radarplot(top_10, output_path + 'radar_plot_top_10_g_C' + str(cluster_label) + '.png', exclude_list,
                  'Cluster ' + str(cluster_label) + ' - Top 10 by G')

        top_10 = data_cluster.sort_values(by=['x'], ascending=False)[:10]
        radarplot(top_10, output_path + 'radar_plot_top_10_x_C' + str(cluster_label) + '.png', exclude_list,
                  'Cluster ' + str(cluster_label) + ' - Top 10 by X')

    # Top 10 per cluster Radar Plot in same img
    radarplot_same_img(data, output_path)


if __name__ == "__main__":
    main()
