#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 11:39:28 2018

@author: marcos
"""

# https://seaborn.pydata.org/tutorial/distributions.html

import numpy as np
import seaborn as sns

sns.set(color_codes=True)
x = np.random.normal(size=100)
sns.distplot(x)
