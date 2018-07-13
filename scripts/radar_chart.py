import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from modules.data import read_data, normalizes
from modules.plots import radarplot

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
