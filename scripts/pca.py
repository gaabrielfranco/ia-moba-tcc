import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.decomposition import PCA
from sklearn import datasets
from modules.data import read_data, normalizes
from sklearn.preprocessing import StandardScaler
import pandas as pd
import seaborn as sns


def main():

    plt.rcParams["figure.figsize"] = (25, 16)
    plt.rcParams['font.size'] = 12.0

    show_plots = False

    df = read_data('df_data_pruned')

    for i in df:
        df[i] = (normalizes(df[i]))[0]

    df -= df.mean()

    # PCA n_dim = 3
    fig = plt.figure(1, figsize=(8, 6))
    ax = Axes3D(fig, elev=-150, azim=110)
    pca = PCA(n_components=9, svd_solver='full')
    X_reduced = pca.fit_transform(df)
    ax.scatter(X_reduced[:, 0], X_reduced[:, 1], X_reduced[:, 2],
               cmap=plt.cm.Set1, edgecolor='k', s=40)
    ax.set_title("First three PCA directions")
    ax.set_xlabel("1st eigenvector")
    ax.w_xaxis.set_ticklabels([])
    ax.set_ylabel("2nd eigenvector")
    ax.w_yaxis.set_ticklabels([])
    ax.set_zlabel("3rd eigenvector")
    ax.w_zaxis.set_ticklabels([])
    if show_plots:
        plt.show()
    plt.clf()

    # PCA n_dim = 2
    fig = plt.figure(1, figsize=(8, 6))
    ax = Axes3D(fig, elev=-150, azim=110)
    ax.scatter(X_reduced[:, 0], X_reduced[:, 1],
               cmap=plt.cm.Set1, edgecolor='k', s=40)
    ax.set_title("First two PCA directions")
    ax.set_xlabel("1st eigenvector")
    ax.w_xaxis.set_ticklabels([])
    ax.set_ylabel("2nd eigenvector")
    ax.w_yaxis.set_ticklabels([])
    ax.w_zaxis.set_ticklabels([])
    if show_plots:
        plt.show()
    plt.clf()

    # PCA n_dim = 1
    fig = plt.figure(1, figsize=(8, 6))
    ax = Axes3D(fig, elev=-150, azim=110)
    y_new = np.zeros((len(X_reduced)), dtype=int)
    ax.scatter(X_reduced[:, 0], y_new,
               cmap=plt.cm.Set1, edgecolor='k', s=40)
    ax.set_title("First PCA direction")
    ax.set_xlabel("1st eigenvector")
    ax.w_xaxis.set_ticklabels([])
    ax.w_yaxis.set_ticklabels([])
    ax.w_zaxis.set_ticklabels([])
    if show_plots:
        plt.show()
    plt.clf()

    # Variance plot
    with plt.style.context('seaborn-whitegrid'):
        plt.bar(range(1, 10), pca.explained_variance_ratio_, alpha=0.5, align='center',
                label='individual explained variance')

        variance = pca.explained_variance_ratio_
        for i, j in enumerate(variance):
            variance[i] = sum(variance[i - 1:i + 1]) if i > 0 else variance[i]

        plt.step(range(1, 10), variance, where='mid',
                 label='cumulative explained variance')

        plt.xticks(range(1, 10))
        plt.ylabel('Explained variance ratio')
        plt.xlabel('Principal components')
        plt.legend(loc='best')
        plt.title('Variance explained with PCA')
        plt.tight_layout()
        if show_plots:
            plt.show()

        file_name = 'files/output_pca/Variance'
        plt.savefig(file_name)
        print('Graph %s saved.' % file_name)
        plt.clf()

    # Creating dataframe with first, second and third components
    data_comp = pd.DataFrame(X_reduced[:, 0:3], columns=[
                             '1st eigenvector', '2nd eigenvector', '3rd eigenvector'])

    plots_path = 'files/output_pca/'

    for i, x in enumerate(data_comp):
        for j, y in enumerate(data_comp):
            if i < j and x != y:
                data_comp.plot.hexbin(x=x, y=y, gridsize=25)
                plt.title('Hexbin plot: ' + x + ' and ' + y)
                if show_plots:
                    plt.show()
                file_name = plots_path + x + '_' + y
                plt.savefig(file_name)
                plt.clf()
                print('Graph %s saved.' % file_name)

    # Feature Selection
    pca_inv_data = pca.inverse_transform(np.eye(9))

    fig = plt.figure(figsize=(10, 6.5))
    sns.heatmap(pca.inverse_transform(
        np.eye(9)), cmap="hot", cbar=False)
    plt.ylabel('principal component', fontsize=20)
    plt.xlabel('original feature index', fontsize=20)
    plt.tick_params(axis='both', which='major', labelsize=18)
    plt.tick_params(axis='both', which='minor', labelsize=12)

    plt.show()
    plt.clf()

    fig = plt.figure(figsize=(10, 6.5))
    plt.plot(pca_inv_data.mean(axis=0), '--o', label='mean')
    plt.plot(np.square(pca_inv_data.std(axis=0)), '--o', label='variance')
    plt.legend(loc='lower right')
    plt.ylabel('feature contribution', fontsize=20)
    plt.xlabel('feature index', fontsize=20)
    plt.tick_params(axis='both', which='major', labelsize=18)
    plt.tick_params(axis='both', which='minor', labelsize=12)
    plt.xlim([0, 10])
    plt.legend(loc='lower left', fontsize=18)

    plt.show()
    plt.clf()


if __name__ == "__main__":
    main()
