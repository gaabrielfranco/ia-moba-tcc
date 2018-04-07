import pandas as pd
import numbers
import matplotlib.pyplot as plt
import numpy as np
from modules.data import read_data, normalizes


def radarplot(data, file_name, title=None, exclude=None, label=None, show_plots=False):
    plt.rcParams["figure.figsize"] = (25, 16)
    plt.rcParams['font.size'] = 12.0

    candidates = list(data.columns)
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

    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)
    for i in data.index:
        values = data[dimensions].loc[i].values
        values = np.concatenate((values, [values[0]]))
        ax.plot(angles, values, 'o-', linewidth=2,
                label=label[i])
        ax.fill(angles, values, alpha=0.25)
    ax.set_thetagrids(angles * 180/np.pi, dimensions)
    if title is not None:
        ax.set_title(title)
    ax.grid(True)
    plt.legend(loc='center left', bbox_to_anchor=(1.1, 0.5))
    if show_plots:
        plt.show()
    plt.savefig(file_name)
    plt.clf()
    print('Graph %s saved.' % file_name)


_, _, data = read_data('k-means_experiments')

for i in data:
    type_experiment = i.split('_')[0]
    if type_experiment == 'all' or type_experiment == 'kda':
        data_norm = normalizes(data[i]['centroids'])[0]
        columns = ['kills', 'deaths', 'assists', 'denies', 'gpm', 'hd', 'hh', 'lh',
                   'xpm'] if type_experiment == 'all' else ['kills', 'deaths', 'assists']
        df = pd.DataFrame(data_norm, columns=columns)
        label = ['Centroid ' + str(x + 1) for x in range(len(data_norm))]
        file_name = 'files/output_radar_chart/radar_plot_' + i
        radarplot(df, file_name, title='Centroids of experiment ' + i, label=label)
