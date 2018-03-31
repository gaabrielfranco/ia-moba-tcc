from modules.data import read_data
import json


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


if __name__ == "__main__":
    main()
