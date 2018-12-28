import pandas as pd
import json
import glob


def main():
    matches = glob.glob("pro_database/*.json")
    for match in matches:
        with open(match, "r") as f:
            data = json.load(f)
        for player in data["players"]:
            print(player)
        return

    #data_dict = json.loads()


if __name__ == "__main__":
    main()
