from modules.data import read_data, create_data, remove_outliers
from modules.clusters import clusterization
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
create_data('files/attributes.txt', True, False)
#a = read_data('corr_pruned')

'''
    TODO:
    - Refatorar read data pra TAMBÉM retornar obj pandas e salvar os attrs de correlação
    - Arrumar plots_distribution (feito)
    - Persistir data (feito)
    - Arrumar k-analysis
    - Arrumar k-means_experiments
    - Refatorar os outros códigos (todo nos códigos)
'''
