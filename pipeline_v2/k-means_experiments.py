import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


def main():
    df = pd.read_csv("create_database/df_database.csv", index_col=0)

    # Normalize data
    df = (df - df.min()) / (df.max() - df.min())

    km = KMeans(n_clusters=10, n_jobs=-1)
    labels = km.fit_predict(df)
    count = [0] * 10

    count = [(labels == i).sum() for i in range(0, 10)]
    plt.pie(count, autopct='%1.1f%%')
    plt.show()


if __name__ == "__main__":
    main()
