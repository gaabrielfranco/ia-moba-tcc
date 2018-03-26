from modules.data import read_data
import json


def main():
    data, data_corr, data_pruned = read_data('k-means_experiments')

    '''data_json = json.dumps(data, indent=4)
    f = open('data.json', 'w')
    f.writelines(data_json)
    f.close()'''


if __name__ == "__main__":
    main()
