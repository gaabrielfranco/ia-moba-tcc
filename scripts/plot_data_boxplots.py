from modules.data import read_data
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def main():
    df = read_data('df_data_pruned')
    df_norm = (df - df.mean()) / (df.max() - df.min())

    sns.set_style("whitegrid")
    for i in df:
        ax = sns.boxplot(data=df[i])
        #ax.set_yscale('log')
        ax.set_xlabel('Attribute')
        ax.set_ylabel('Value')
        plt.title('Attributes distribution')
        plt.show()


if __name__ == "__main__":
    main()
