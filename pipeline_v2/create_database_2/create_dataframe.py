import pandas as pd
import json
import glob
import copy
from sklearn import preprocessing
import sys
import numpy as np
import scipy.stats as sci


def main():
    matches = glob.glob("pro_database/*.json")
    attributes = {"kills": 0, "deaths": 0, "assists": 0, "denies": 0,
                  "gold_per_min": 0, "xp_per_min": 0, "hero_damage": 0,
                  "hero_healing": 0, "last_hits": 0, "n_matches": 0}

    data_dict = {}
    for match in matches:
        with open(match, "r") as f:
            data = json.load(f)
            for player in data["players"]:
                try:
                    for attr in attributes.keys():
                        if attr != "n_matches":
                            data_dict[player["account_id"]
                                      ][attr] += player[attr]
                        else:
                            data_dict[player["account_id"]][attr] += 1
                except:
                    data_dict[player["account_id"]] = copy.deepcopy(attributes)
                    for attr in attributes.keys():
                        if attr != "n_matches":
                            data_dict[player["account_id"]
                                      ][attr] += player[attr]
                        else:
                            data_dict[player["account_id"]][attr] += 1

    df = pd.DataFrame.from_dict(data_dict, orient='index')

    # Only players with 5 or more matches
    df = df[df.n_matches >= 5]

    # Raw database
    df.to_csv("df_raw_database.csv")

    # Attributes per match
    for attr in df:
        df[attr] /= df["n_matches"]
    df = df.drop(columns=["n_matches"])
    df.to_csv("df_database_outliers.csv")

    # Removing outliers
    q1 = np.percentile(df, 25, axis=0)
    q3 = np.percentile(df, 75, axis=0)
    iqr = sci.iqr(df, axis=0)
    outliers = []
    for index, row in df.iterrows():
        if not((row >= q1 - 1.5 * iqr).all() and (row <= q3 + 1.5 * iqr).all()):
            outliers.append(index)
    df = df.drop(outliers, axis=0)
    df.to_csv("df_database.csv")


if __name__ == "__main__":
    main()
