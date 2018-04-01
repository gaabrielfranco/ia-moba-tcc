import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.decomposition import PCA
from sklearn import datasets
from modules.data import read_data
from sklearn.preprocessing import StandardScaler


def main():
    show_plots = False

    df = read_data('df_data_pruned')

    df = StandardScaler().fit_transform(df)

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
    file_name = 'files/output_pca/PCA_3_dimension'
    plt.savefig(file_name)
    print('Graph %s saved.' % file_name)
    if show_plots:
        plt.show()
    plt.clf()

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
    file_name = 'files/output_pca/PCA_2_dimension'
    plt.savefig(file_name)
    print('Graph %s saved.' % file_name)
    if show_plots:
        plt.show()
    plt.clf()

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
    file_name = 'files/output_pca/PCA_1_dimension'
    plt.savefig(file_name)
    print('Graph %s saved.' % file_name)
    if show_plots:
        plt.show()
    plt.clf()

    variance = pca.explained_variance_ratio_
    num_dim = list(range(1, 10))

    for i, j in enumerate(variance):
        variance[i] = sum(variance[i-1:i+1]) if i > 0 else variance[i]

    plt.plot(num_dim, variance, 'o')
    plt.title("Variance captured in each dimension")
    plt.xlabel("Number of dimensions")
    plt.ylabel("Variance")
    file_name = 'files/output_pca/Variance'
    plt.savefig(file_name)
    print('Graph %s saved.' % file_name)
    if show_plots:
        plt.show()


if __name__ == "__main__":
    main()
