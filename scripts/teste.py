from modules.data import read_data, create_data, remove_outliers
import numpy as np
create_data('files/attributes.txt', True, False)
a = read_data('corr')
# print(b)
