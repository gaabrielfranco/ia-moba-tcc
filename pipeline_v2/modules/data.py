import numpy as np
import scipy.stats as sci


def remove_outliers(data, c=2.698):
    new_data = {}
    new_data['all'] = []
    new_data['kda'] = []
    new_data['kills'] = []
    new_data['deaths'] = []
    new_data['assists'] = []
    new_data['denies'] = []
    new_data['gpm'] = []
    new_data['hd'] = []
    new_data['hh'] = []
    new_data['lh'] = []
    new_data['xpm'] = []

    outliers = []
    outliers_attr = []
    attributes = ["kills", "deaths",
                  "assists", "denies", "gpm", "hd", "hh", "lh", "xpm"]
    index_attr = {"kills": 0, "deaths": 1,
                  "assists": 2, "denies": 3, "gpm": 4, "hd": 5, "hh": 6, "lh": 7, "xpm": 8}

    q1 = np.percentile(data, 25, axis=0)
    q3 = np.percentile(data, 75, axis=0)
    iqr = sci.iqr(data, axis=0)

    for d in data:
        att_v = []
        att_v.append(d >= q1 - 1.5 * iqr)
        att_v.append(d <= q3 + 1.5 * iqr)
        validation_outiers = np.all(att_v, axis=0)

        if validation_outiers.all():
            for key in new_data.keys():
                if key == 'all':
                    new_data[key].append(d)
                elif key == 'kda':
                    new_data[key].append(d[0:3])
                else:
                    new_data[key].append([d[index_attr[key]]])
        else:
            outliers.append(d)
            attr = []

            for index, value in enumerate(validation_outiers):
                if not(value):
                    attr.append(attributes[index])
            outliers_attr.append(attr)

    print("\n================ Summary about outliers ================\n")
    print("Number of outliers = ", len(outliers_attr))
    teste = [0 for i in range(10)]
    for i in outliers_attr:
        teste[len(i)] += 1

    print("Number of outliers in 1, ..., 9 attributes: ")
    print(teste[1:])
    print()
    print("Number of outliers per attribute: ")
    count_out_att = {}
    count_out_att['kills'] = 0
    count_out_att['deaths'] = 0
    count_out_att['assists'] = 0
    count_out_att['denies'] = 0
    count_out_att['gpm'] = 0
    count_out_att['hd'] = 0
    count_out_att['hh'] = 0
    count_out_att['lh'] = 0
    count_out_att['xpm'] = 0

    for i in outliers_attr:
        for j in i:
            count_out_att[j] += 1

    for i in count_out_att.keys():
        print(i, count_out_att[i], sep=': ')
    print()
    return new_data, outliers, outliers_attr
