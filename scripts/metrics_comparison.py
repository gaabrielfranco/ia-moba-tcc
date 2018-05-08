#!/usr/bin/env python3

from modules.data import read_data
import argparse
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# =============================================================================
# GABRIEL:
# - Note que incluí resultados para a clusterização segundo também cada conjunto de atributos selecionados
# - Veja os plots salvos na pasta nova que criei
# - Sendo assim, botei métodos diferentes para se obter os labels dos clusters, variando o conjunto de 
#       atributos utilizados para agrupoar os dados, gerando 5 casos:
#       - Todos atributos (all)
#       - kda (considerando-se apenas kills, deaths e assists para clusterizar)
#       - adg (considerando-se apenas denies, deaths, assists, gpm e hh para clusterizar)
#       - g (considerando-se apenas deaths, gpm e hh para clusterizar)
#       - x (considerando-se apenas deaths, xpm e hh para clusterizar)
# - Foram utilizadas projeções diferentes da base de dados apenas pra gerar os rótulos dos clusters, mas
#       a database continua contendo todos atributos, para fins de cálculos das médias das métricas
#
# - Para Fazer:
#       1. Plot de distribuição dentro dos clusters (intra cluster), como vc mesmo sugeriu
#               (Não precisa fazer o inter cluster, os plots de barra que coloquei já substituem isso)
#       2. Gerar a matriz de correlações entre as métricas para cada um dos 5 casos descritos acima
# - Quaisquer dúvidas, entre em contato
# =============================================================================

def compute_stats(data, metric, n_clusters=10, normed_mean=False):
    avg_metric = np.empty(n_clusters)
    std_metric = np.empty(n_clusters)
    var_coef_metric = np.empty(n_clusters)
    
    for cluster_id in range(n_clusters):
        avg_metric[cluster_id] = data[metric][data.cluster == cluster_id].mean()
        std_metric[cluster_id] = data[metric][data.cluster == cluster_id].std()
        var_coef_metric[cluster_id] = std_metric[cluster_id] / avg_metric[cluster_id]
        
    if normed_mean:
        avg_metric = (avg_metric - avg_metric.min()) / (avg_metric.max() - avg_metric.min())
        std_metric = (std_metric - avg_metric.min()) / (avg_metric.max() - avg_metric.min())
        return avg_metric+0.5, std_metric
    
    return avg_metric, std_metric, var_coef_metric

def main():
    default_path = 'files/output_metrics_comparison/'
    
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
    parser.add_argument('--normed_mean', '-nm', action='store_true',
                        help='plot normed values for mean in line plot (default = False)')

    args = parser.parse_args()
    with_outliers = args.with_outliers

    if with_outliers:
        data = read_data('df_data')
    else:
        data = read_data('df_data_pruned')
        
    if not args.output_path.endswith('/'):
        output_path = args.output_path + '/'
    else:
        output_path = args.output_path

    ### Normalizing data
    for col in data.columns:
        data[col] = (data[col] - data[col].min()) / (data[col].max() - data[col].min())
        
    ### Clustering
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
    
    ### Compute metrics and add them to the database, as well as the clusters labels
    kda = (data['kills'] + data['assists']) / (1 + data['deaths'])
    adg = (data['denies'] + data['assists'] + data['gpm'] + data['hh']) / (1 + data['deaths'])
    g = (data['gpm'] + data['hh']) / (1 + data['deaths'])
    x = (data['xpm'] + data['hh']) / (1 + data['deaths'])
    
    data.insert(len(data.columns), 'kda', kda)
    data.insert(len(data.columns), 'adg', adg)
    data.insert(len(data.columns), 'g', g)
    data.insert(len(data.columns), 'x', x)
    data.insert(len(data.columns), 'cluster', labels)
    
    ### Compute intra-clusters stats
    averages = {}
    stds = {}
    coeffs = {}
    averages['KDA'], stds['KDA'], coeffs['KDA'] = compute_stats(data, 'kda')
    averages['ADG'], stds['ADG'], coeffs['ADG'] = compute_stats(data, 'adg')
    averages['G'], stds['G'], coeffs['G'] = compute_stats(data, 'g')
    averages['X'], stds['X'], coeffs['X'] = compute_stats(data, 'x')
    
    if args.normed_mean:
        averages_normed = {}
        stds_normed = {}
        averages_normed['KDA'], stds_normed['KDA'] = compute_stats(data, 'kda', normed_mean=True)
        averages_normed['ADG'], stds_normed['ADG'] = compute_stats(data, 'adg', normed_mean=True)
        averages_normed['G'], stds_normed['G'] = compute_stats(data, 'g', normed_mean=True)
        averages_normed['X'], stds_normed['X'] = compute_stats(data, 'x', normed_mean=True)
    
    clusters = np.array(range(args.n_clusters))
    
    ### Plots
    subset = 'Clustered with %s attributes' % args.projection
    for metric in averages.keys():
        if metric != 'KDA':
            metrics = ('KDA', metric)
            
            fig, ax = plt.subplots()
            ax.bar(clusters, averages[metrics[0]], width=0.5, color='r', yerr=stds[metrics[0]], label=metrics[0])
            ax.bar(clusters+0.5, averages[metrics[1]], width=0.5, color='b', yerr=stds[metrics[1]], label=metrics[1])
            plt.suptitle('Average %s versus Average %s' % metrics)
            plt.title(subset)
            plt.legend()
            plt.xlabel('Cluster ID')
            plt.ylabel('Metrics')
            plt.xticks(clusters + 0.25)
            xlabels = tuple(['C%d' % (i+1) for i in clusters])
            ax.set_xticklabels(xlabels)
            file_name = '%savg_%s_%s_%s.png' % (output_path, metrics[0], metrics[1], args.projection)
            plt.savefig(file_name)
            print(file_name, 'saved')
            if args.show_plots:
                plt.show()
            plt.clf()
            
            if args.normed_mean:
                fig, ax = plt.subplots()
                ax.bar(clusters, averages_normed[metrics[0]], width=0.5, color='r', yerr=stds_normed[metrics[0]], label=metrics[0])
                ax.bar(clusters+0.5, averages_normed[metrics[1]], width=0.5, color='b', yerr=stds_normed[metrics[1]], label=metrics[1])
                plt.suptitle('Average %s versus Average %s (normed)' % metrics)
                plt.title(subset)
                plt.legend()
                plt.xlabel('Cluster ID')
                plt.ylabel('Metrics')
                plt.xticks(clusters + 0.25)
                xlabels = tuple(['C%d' % (i+1) for i in clusters])
                ax.set_xticklabels(xlabels)
                file_name = '%savg_%s_%s_%s_normed.png' % (output_path, metrics[0], metrics[1], args.projection)
                plt.savefig(file_name)
                print(file_name, 'saved')
                if args.show_plots:
                    plt.show()
                plt.clf()
"""
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
"""

if __name__ == "__main__":
    main()
