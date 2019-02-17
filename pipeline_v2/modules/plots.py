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
    plt.rc('font', size=7)
    ax = fig.add_subplot(111, polar=True)
    colors_vec = ["#e6194b", "#3cb44b", "#ffe119", "#0082c8",
                  "#f58231", "#911eb4", "#46f0f0", "#f032e6", "#fabebe", "#008080"]
    pallete = sns.color_palette(colors_vec)
    for index, i in enumerate(data.index):
        values = data[dimensions].loc[i].values
        values = np.concatenate((values, [values[0]]))
        ax.plot(angles, values, 'o-', linewidth=2,
                label=label[i], color=pallete[index])
        ax.fill(angles, values, alpha=0.25)
    ax.set_thetagrids(angles * 180/np.pi, dimensions)
    if title is not None:
        ax.set_title(title)
    ax.grid(True)
    plt.tight_layout()
    plt.legend(loc="center right", bbox_to_anchor=(1.32, 0.5),
               title="Centroid")  # bbox_to_anchor=(1.1, 0.5)
    if show_plots:
        plt.show()
    plt.savefig(file_name, bbox_inches='tight', pad_inches=0.01)
    plt.clf()
    print('Graph %s saved.' % file_name)
