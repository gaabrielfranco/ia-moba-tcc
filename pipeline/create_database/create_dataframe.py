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

    db_name = "df_database_all"  # 13641 valid matches, 1342 outliers
    '''
    attributes = {"kills": 0, "deaths": 0, "assists": 0, "denies": 0,
                  "gold_per_min": 0, "xp_per_min": 0, "hero_damage": 0,
                  "hero_healing": 0, "last_hits": 0, "n_matches": 0,
                  "firstblood_claimed": 0, "obs_placed": 0, "rune_pickups": 0,
                  "sen_placed": 0, "teamfight_participation": 0, "tower_damage": 0,
                  "towers_killed": 0, "neutral_kills": 0, "courier_kills": 0,
                  "observer_kills": 0, "sentry_kills": 0, "ancient_kills": 0}
    '''
    attributes = {"kills": 0, "deaths": 0, "assists": 0, "denies": 0,
                  "gold_per_min": 0, "xp_per_min": 0, "hero_damage": 0,
                  "hero_healing": 0, "last_hits": 0, "n_matches": 0,
                  "firstblood_claimed": 0, "obs_placed": 0, "rune_pickups": 0,
                  "sen_placed": 0, "teamfight_participation": 0, "tower_damage": 0,
                  "towers_killed": 0, "neutral_kills": 0, "tower_kills": 0,
                  "lane_kills": 0, "roshan_kills": 0, "necronomicon_kills": 0,
                  "courier_kills": 0, "observer_kills": 0, "sentry_kills": 0,
                  "ancient_kills": 0, "camps_stacked": 0, "gold_spent": 0,
                  "pings": 0, "roshans_killed": 0, "stuns": 0,
                  "buyback_count": 0, "observer_uses": 0, "sentry_uses": 0,
                  "lane_efficiency": 0, "purchase_tpscroll": 0, "actions_per_min": 0}
    '''
    db_name = "df_database"  # 38976 valid matches, 893 outliers
    attributes = {"kills": 0, "deaths": 0, "assists": 0, "denies": 0,
                  "gold_per_min": 0, "xp_per_min": 0, "hero_damage": 0,
                  "hero_healing": 0, "last_hits": 0, "n_matches": 0}
    '''
    data_dict = {}
    valid_matches = 0
    invalid_matches = 0

    for match in matches:
        print("Partida", match)
        with open(match, "r") as f:
            data = json.load(f)
            valid = True
            for player in data["players"]:
                if not valid:
                    break
                if not(player["account_id"] in data_dict):
                    data_dict[player["account_id"]] = copy.deepcopy(attributes)
                for attr in attributes.keys():
                    if attr != "n_matches":
                        try:
                            if player[attr] is not None:
                                data_dict[player["account_id"]
                                          ][attr] += player[attr]
                            else:
                                invalid_matches += 1
                                valid = False
                                break
                        except:
                            invalid_matches += 1
                            valid = False
                            break
                    else:
                        data_dict[player["account_id"]][attr] += 1
            if valid:
                valid_matches += 1

    df = pd.DataFrame.from_dict(data_dict, orient='index')

    print("Number of valid matches: ", valid_matches)
    print("Number of invalid matches: ", invalid_matches)

    # Only players with 5 or more matches
    df = df[df.n_matches >= 5]

    # Attributes per match
    for attr in df:
        df[attr] /= df["n_matches"]
    df = df.drop(columns=["n_matches"])

    df.to_csv(db_name + "_w_outliers.csv")

    # Removing outliers
    q1 = np.percentile(df, 25, axis=0)
    q3 = np.percentile(df, 75, axis=0)
    iqr = sci.iqr(df, axis=0)
    outliers = []
    for index, row in df.iterrows():
        if not((row >= q1 - 1.5 * iqr).all() and (row <= q3 + 1.5 * iqr).all()):
            outliers.append(index)
    df = df.drop(outliers, axis=0)
    print("Outliers: ", len(outliers))
    df.to_csv(db_name + ".csv")


if __name__ == "__main__":
    main()
