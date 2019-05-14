#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  8 12:24:06 2019

@author: dpi
"""

def get_top_n(filename, n_attr, top, ini_line=7):
    fp = open(filename, 'r')
    lines = fp.readlines()
    fp.close()
    
    headers = lines[ini_line-1].split(';')
    data = []
    for i in range(ini_line, ini_line+top):
        items = lines[i].split(';')
        solution = {}
        solution['evaluation'] = float(items[0].replace(',', '.'))
        
        attributes = []
        bin_seq = ''
        for j in range(1, n_attr+1):
            if int(items[j]):
                attributes.append(headers[j])
            bin_seq += str(items[j])
            
        attributes.sort()
        solution['size'] = len(attributes)
        solution['description'] = '[' + ', '.join(attributes) + ']'
        solution['signature'] = int(bin_seq, 2)
        
        data.append(solution)
        
    return data
        
def main():
    basefilename = 'output_ga/all/dez_execucoes/ga_setpack_cosine_new_%02d.csv'
    ini_line = 7
    top = 25
    n_attr = 36
    
    for n in range(1, 11):
        filename = basefilename % n    
        data = get_top_n(filename, n_attr, top, ini_line)
    
    print(data)

if __name__ == '__main__':
    main()
    