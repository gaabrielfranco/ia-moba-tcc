import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import numbers


def radarplot(data, file_name, title=None, exclude=None, label=None, show_plots=False, figsize=(5, 3.4)):
    matplotlib.rcParams['pdf.fonttype'] = 42
    matplotlib.rcParams['ps.fonttype'] = 42
    matplotlib.style.use('ggplot')

    candidates = list(data.columns)
    if exclude is None:
        dimensions = np.array(data.columns)
    else:
        dimensions = []
        for i, c in enumerate(candidates):
            if isinstance(data.loc[0, c], numbers.Number):
                if exclude is not None:
                    if c not in exclude:
                        dimensions.append(candidates[i])
                else:
                    dimensions.append(candidates[i])
        dimensions = np.array(dimensions)

    angles = np.linspace(0, 2*np.pi, len(dimensions), endpoint=False)
    angles = np.concatenate((angles, [angles[0]]))

    fig = plt.figure(figsize=figsize)
    #plt.rc('font', size=7)
    plt.rc('font', size=3)
    ax = fig.add_subplot(111, polar=True)
    colors_vec = ["#e6194b", "#3cb44b", "#ffe119", "#0082c8",
                  "#f58231", "#911eb4", "#46f0f0", "#f032e6", "#fabebe", "#008080"]
    pallete = sns.color_palette(colors_vec)
    for index, i in enumerate(data.index):
        values = data[dimensions].loc[i].values
        values = np.concatenate((values, [values[0]]))
        # ax.plot(angles, values, 'o-', linewidth=2,
        #        label=label[i], color=pallete[index])
        ax.plot(angles, values, 'o-', linewidth=2, color=pallete[index])
        ax.fill(angles, values, alpha=0.25)
    ax.set_thetagrids(angles * 180/np.pi, dimensions)
    if title is not None:
        ax.set_title(title)
    ax.grid(True)
    plt.tight_layout()
    # plt.legend(loc="center right", bbox_to_anchor=(1.32, 0.5),
    #           title="Centroid")  # bbox_to_anchor=(1.1, 0.5)
    if show_plots:
        plt.show()
    plt.savefig(file_name, bbox_inches='tight', pad_inches=0.01, dpi=600)
    plt.clf()
    print('Graph %s saved.' % file_name)


def radarplot_multi(data, file_name, size_plot=(2, 5), title=None, exclude=None, label=None, show_plots=False, figsize=(3.8, 2.3)):
    matplotlib.rcParams['pdf.fonttype'] = 42
    matplotlib.rcParams['ps.fonttype'] = 42
    matplotlib.style.use('ggplot')

    candidates = list(data.columns)
    if exclude is None:
        dimensions = np.array(data.columns)
    else:
        dimensions = []
        for i, c in enumerate(candidates):
            if isinstance(data.loc[0, c], numbers.Number):
                if exclude is not None:
                    if c not in exclude:
                        dimensions.append(candidates[i])
                else:
                    dimensions.append(candidates[i])
        dimensions = np.array(dimensions)

    angles = np.linspace(0, 2*np.pi, len(dimensions), endpoint=False)
    angles = np.concatenate((angles, [angles[0]]))

    matplotlib.rcParams["figure.figsize"] = figsize
    matplotlib.rc('xtick', labelsize=4)
    matplotlib.rc('ytick', labelsize=4)
    n_lines, n_columns = size_plot
    fig, axarr = plt.subplots(n_lines, n_columns, subplot_kw=dict(polar=True))
    plt.rc('font', size=3)
    # colors_vec = ["#e6194b", "#3cb44b", "#ffe119", "#0082c8",
    #             "#f58231", "#911eb4", "#46f0f0", "#f032e6", "#fabebe", "#008080"]
    #pallete = sns.color_palette(colors_vec)
    idx = 0
    lines = [0] * (n_lines * n_columns)
    for i in range(n_lines):
        for j in range(n_columns):
            values = data[dimensions].loc[idx].values
            values = np.concatenate((values, [values[0]]))
            lines[idx], = axarr[i, j].plot(
                angles, values, 'o-', linewidth=.2, markersize=1)  # , color=pallete[idx])
            # , color=pallete[idx])
            axarr[i, j].fill(angles, values, alpha=0.25)
            axarr[i, j].set_thetagrids(
                angles * 180/np.pi, ["" for i in range(len(dimensions))])
            axarr[i, j].set_rticks([0.2, 0.4, 0.6, 0.8, 1.0])
            axarr[i, j].set_yticklabels(["", "", "", "", ""], fontsize=1)
            axarr[i, j].grid(True)
            axarr[i, j].set_title("Centroid " + str(idx + 1))
            plt.tight_layout()
            idx += 1

    # plt.legend(lines, label, loc="best", bbox_to_anchor=(1.32, 0.5),
    #           title="Centroid")  # bbox_to_anchor=(1.1, 0.5)
    if title is not None:
        plt.title(title)
    if show_plots:
        plt.show()

    plt.subplots_adjust(hspace=0.01)
    plt.savefig(file_name, bbox_inches='tight', pad_inches=0.01, dpi=600)
    plt.clf()
    print('Graph %s saved.' % file_name)


def radarplot_comp(data, data_2, file_name, size_plot=(2, 5), title=None, exclude=None, label=None, show_plots=False, figsize=(3.8, 2.3)):
    matplotlib.rcParams['pdf.fonttype'] = 42
    matplotlib.rcParams['ps.fonttype'] = 42
    matplotlib.style.use('ggplot')

    candidates = list(data.columns)
    if exclude is None:
        dimensions = np.array(data.columns)
    else:
        dimensions = []
        for i, c in enumerate(candidates):
            if isinstance(data.loc[0, c], numbers.Number):
                if exclude is not None:
                    if c not in exclude:
                        dimensions.append(candidates[i])
                else:
                    dimensions.append(candidates[i])
        dimensions = np.array(dimensions)

    angles = np.linspace(0, 2*np.pi, len(dimensions), endpoint=False)
    angles = np.concatenate((angles, [angles[0]]))

    matplotlib.rcParams["figure.figsize"] = figsize
    matplotlib.rc('xtick', labelsize=2)
    matplotlib.rc('ytick', labelsize=2)
    n_lines, n_columns = size_plot
    fig, axarr = plt.subplots(n_lines, n_columns, subplot_kw=dict(polar=True))
    plt.rc('font', size=5)
    # colors_vec = ["#e6194b", "#3cb44b", "#ffe119", "#0082c8",
    #             "#f58231", "#911eb4", "#46f0f0", "#f032e6", "#fabebe", "#008080"]
    #pallete = sns.color_palette(colors_vec)
    idx = 0
    #lines = [0] * (n_lines * n_columns)
    for i in range(n_lines):
        for j in range(n_columns):
            values = data[dimensions].loc[idx].values
            values = np.concatenate((values, [values[0]]))
            values_2 = data_2[dimensions].loc[idx].values
            values_2 = np.concatenate((values_2, [values_2[0]]))
            axarr[i, j].plot(angles, values, 'o-', linewidth=.2,
                             markersize=1)  # , color=pallete[idx])
            axarr[i, j].fill(angles, values, alpha=0.25)
            axarr[i, j].plot(angles, values_2, 'o-',
                             linewidth=.2, markersize=1)
            # , color=pallete[idx])
            axarr[i, j].fill(angles, values_2, alpha=0.25)
            axarr[i, j].set_thetagrids(
                angles * 180/np.pi, ["" for i in range(len(dimensions))])
            axarr[i, j].set_rticks([0.2, 0.4, 0.6, 0.8, 1.0])
            axarr[i, j].set_yticklabels(["", "", "", "", ""], fontsize=1)
            axarr[i, j].grid(True)
            axarr[i, j].set_title("Top " + str(idx + 1))
            plt.tight_layout()
            idx += 1

    # plt.legend(lines, label, loc="best", bbox_to_anchor=(1.32, 0.5),
    #           title="Centroid")  # bbox_to_anchor=(1.1, 0.5)
    if title is not None:
        plt.title(title)
    if show_plots:
        plt.show()

    plt.subplots_adjust(hspace=0.01)
    plt.savefig(file_name, bbox_inches='tight', pad_inches=0.01, dpi=600)
    plt.clf()
    print('Graph %s saved.' % file_name)
