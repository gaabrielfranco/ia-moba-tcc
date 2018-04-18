#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 14:46:03 2018

@author: marcos
"""

import sympy

x,y,z = sympy.symbols('x y z')

expr = x**2 + 2*x
print(sympy.solve(expr, x))

print(expr)
