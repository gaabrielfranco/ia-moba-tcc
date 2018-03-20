from pprint import PrettyPrinter
from modules.data import normalizes, de_normalize
from sklearn.cluster import KMeans
import pandas as pd


def clusterization(data, cluster_list, seed, json_file, verbose):
    output_data = {}

    for attr_set in data.keys():
        for k in cluster_list:
            print('Executing experiment with %s attributes and %d clusters...' % (
                attr_set, k))
            data_norm, min_norm, max_norm = normalizes(data[attr_set])
            km = KMeans(n_clusters=k, random_state=seed, n_jobs=-1)
            labels = km.fit_predict(data_norm)

            experiment = attr_set + '_' + str(k)
            output_data[experiment] = {}

            # Init data matrix with k lists
            output_data[experiment]['clusters'] = []
            for i in range(k):
                output_data[experiment]['clusters'].append([])

            # Assign each individual from the database to its corresponding cluster
            for i, instance in enumerate(data[attr_set]):
                output_data[experiment]['clusters'][labels[i]].append(instance)

            output_data[experiment]['inertia'] = km.inertia_
            output_data[experiment]['centroids'] = de_normalize(
                km.cluster_centers_, min_norm, max_norm)
            output_data[experiment]['seed'] = seed

    if verbose:
        print('\n\nOutput data summary:')
        pp = PrettyPrinter(depth=3)
        pp.pprint(output_data)

    data_out = pd.DataFrame(output_data)
    data_out.to_json(json_file)

    print('\nOutput data successfully exported to file %s\n' % json_file)

    return output_data
