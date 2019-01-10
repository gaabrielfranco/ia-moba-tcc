import pandas as pd


def main():
    df = pd.read_csv("create_database/df_database.csv")

    print(df.keys())


if __name__ == "__main__":
    main()
