import pandas as pd
from copy import deepcopy
from modules.plots import radarplot
import seaborn as sns
from statsmodels.distributions.empirical_distribution import ECDF
import matplotlib.pyplot as plt

def main():
    df = pd.read_csv("create_database/df_database_norm_w_metrics_all.csv", index_col=0)
    df_cluster = pd.read_csv("create_database/df_database_clusters_all.csv", index_col=0)
    data = pd.read_csv("create_database/df_database_all.csv", index_col=0)

    metrics = ["Metric_" + str(i) for i in range(1, 11)]
    metrics.append("KDA")

    '''
    # Radarplots of top10 for each metric
    folder = "all/starplots_top10"

    for metric in metrics:
        df_ord = df.sort_values(by=[metric], ascending=False)
        df_top10 = df_ord.loc[:, data.columns].iloc[:10]
        df_top10.index = list(range(10))
        label = ["Top " + str(i) for i in range(1, 11)]
        file_name = "img/" + folder + "/" + metric + "_starplot"

        radarplot(df_top10, file_name, label=label, figsize=(12, 9))
    '''

    # CDF for each metric per cluster
    folder = "all/ecdf_per_cluster"
    
    df.insert(len(df.columns), column="cluster", value=df_cluster["cluster"])

    #PRECISO DOS DADOS NÃO PODADOS (fazer)
    for metric in metrics:
        #fig = plt.figure(figsize=(5.55, 4.7))
        #plt.rc('font', size=7)
        for i in range(10):
            #print(df[df.cluster == i][metric])
            ecdf = ECDF(df[df.cluster == i][metric].values)
            plt.plot(ecdf.x, ecdf.y, label="Cluster " + str(i+1))
        plt.legend()
        plt.show()
        #plt.tight_layout()
        file_name = "img/" + folder + "/" + metric
        plt.savefig(file_name, bbox_inches='tight', pad_inches=0.01)
        plt.clf()
        print('Graph %s saved.' % file_name)
        break
        

if __name__ == "__main__":
    main()
