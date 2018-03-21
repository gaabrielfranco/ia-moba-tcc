from modules.data import read_data, create_data, remove_outliers
import numpy as np
#create_data('files/attributes.txt', True, False)
data = read_data()

remove_outliers(data['all'])
