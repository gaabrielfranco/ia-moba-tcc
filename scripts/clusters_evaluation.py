from modules.data import read_data
import json
from scipy.spatial.distance import euclidean


def main():
    kmeans, kmeans_corr, kmeans_pruned = read_data('k-means_experiments')

    f = open('files/output_cluster_evaluation/cluster_eval.txt', 'w')
    for experiment in kmeans:
        if experiment.split('_')[0] == 'all' or experiment.split('_')[0] == 'kda':
            f.writelines("================ " +
                         experiment + " ================\n")
            for centroid in kmeans[experiment]['centroids']:
                f.writelines(str(centroid) + '\n')
            f.writelines('\n')
    f.close()

    f = open('files/output_cluster_evaluation/cluster_eval_corr.txt', 'w')
    for experiment in kmeans_corr:
        f.writelines("================ " +
                     experiment + " ================\n")
        for centroid in kmeans_corr[experiment]['centroids']:
            f.writelines(str(centroid) + '\n')
        f.writelines('\n')
    f.close()

    f = open('files/output_cluster_evaluation/cluster_eval_pruned.txt', 'w')
    for experiment in kmeans_pruned:
        if experiment.split('_')[0] == 'all' or experiment.split('_')[0] == 'kda':
            f.writelines("================ " +
                         experiment + " ================\n")
            for centroid in kmeans_pruned[experiment]['centroids']:
                f.writelines(str(centroid) + '\n')
            f.writelines('\n')
    f.close()

    distance = {}
    for experiment in kmeans:
        distance[experiment] = []
        for k, cluster in enumerate(kmeans[experiment]['clusters']):
            dist = 10000000
            player_dist = []
            for player in cluster:
                euc_dist = euclidean(
                    kmeans[experiment]['centroids'][k], player)
                if euc_dist < dist:
                    dist = euc_dist
                    player_dist = player
            distance[experiment].append(
                {"distance": dist, "player": player_dist})

    distance_corr = {}
    for experiment in kmeans_corr:
        distance_corr[experiment] = []
        for k, cluster in enumerate(kmeans_corr[experiment]['clusters']):
            dist = 10000000
            player_dist = []
            for player in cluster:
                euc_dist = euclidean(
                    kmeans_corr[experiment]['centroids'][k], player)
                if euc_dist < dist:
                    dist = euc_dist
                    player_dist = player
            distance_corr[experiment].append(
                {"distance": dist, "player": player_dist})

    distance_pruned = {}
    for experiment in kmeans_pruned:
        distance_pruned[experiment] = []
        for k, cluster in enumerate(kmeans_pruned[experiment]['clusters']):
            dist = 10000000
            player_dist = []
            for player in cluster:
                euc_dist = euclidean(
                    kmeans_pruned[experiment]['centroids'][k], player)
                if euc_dist < dist:
                    dist = euc_dist
                    player_dist = player
            distance_pruned[experiment].append(
                {"distance": dist, "player": player_dist})

    f = open('files/output_cluster_evaluation/distance_eval.txt', 'w')
    for experiment in distance:
        f.writelines("===================== " +
                     experiment + " =====================\n")
        for i in range(len(distance[experiment])):
            f.writelines("\tCluster " + str(i+1) + ":\n")
            f.writelines(
                "\t\tDistance = " + str(distance[experiment][i]['distance']) + '\n')
            f.writelines("\t\tPlayer = " +
                         str(distance[experiment][i]['player']) + '\n')
            f.writelines("\t\tCentroid = " +
                         str(kmeans[experiment]['centroids'][i]) + '\n')
            f.writelines("\n")
    f.close()

    f = open('files/output_cluster_evaluation/distance_eval_corr.txt', 'w')
    for experiment in distance_corr:
        f.writelines("===================== " +
                     experiment + " =====================\n")
        for i in range(len(distance_corr[experiment])):
            f.writelines("\tCluster " + str(i+1) + ":\n")
            f.writelines(
                "\t\tDistance = " + str(distance_corr[experiment][i]['distance']) + '\n')
            f.writelines("\t\tPlayer = " +
                         str(distance_corr[experiment][i]['player']) + '\n')
            f.writelines("\t\tCentroid = " +
                         str(kmeans_corr[experiment]['centroids'][i]) + '\n')
            f.writelines("\n")
    f.close()

    f = open('files/output_cluster_evaluation/distance_eval_pruned.txt', 'w')
    for experiment in distance_pruned:
        f.writelines("===================== " +
                     experiment + " =====================\n")
        for i in range(len(distance_pruned[experiment])):
            f.writelines("\tCluster " + str(i+1) + ":\n")
            f.writelines(
                "\t\tDistance = " + str(distance_pruned[experiment][i]['distance']) + '\n')
            f.writelines("\t\tPlayer = " +
                         str(distance_pruned[experiment][i]['player']) + '\n')
            f.writelines("\t\tCentroid = " +
                         str(kmeans_pruned[experiment]['centroids'][i]) + '\n')
        f.writelines("\n")
    f.close()


if __name__ == "__main__":
    main()
