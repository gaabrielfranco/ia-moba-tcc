#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  8 18:09:27 2019

@author: dpi
"""

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

def get_short_name(name, var):
    parts = name.split('_')
    sigla = ''
    for part in parts:
        sigla += part[0]
    
    sigla += '\n%.3f' % var
    
    return sigla

corr_threshold = 0.8

# Cria um grafo G
G = nx.Graph()
nodes = []
arestas = []

### Le dados
data = pd.read_csv("../create_database/df_database_all.csv", index_col=0)
### Normalizing data
data = (data - data.min()) / (data.max() - data.min())

### Computa correlacoes
corr = data.corr()
var = data.var()
attributes = list(data.columns)

for i in range(0, len(attributes)-1):
    for j in range(i+1, len(attributes)):
        correlacao = abs(corr[attributes[i]][attributes[j]])
        if correlacao >= corr_threshold:
            if attributes[i] not in nodes:
                label1 = get_short_name(attributes[i], var[attributes[i]])
                nodes.append(label1)
            if attributes[j] not in nodes:
                label2 = get_short_name(attributes[j], var[attributes[j]])
                nodes.append(label2)
            arestas.append((label1, label2, {'peso': round(correlacao, 3)}))

# Adiciona nos e arestas ao grafo
G.add_nodes_from(nodes)
G.add_edges_from(arestas)

# Desenha grafo
pos = nx.circular_layout(G)
pesos = nx.get_edge_attributes(G, 'peso')

labels = {}
for node_name in nodes:
    labels[node_name] = node_name

nx.draw_networkx_nodes(G, pos, node_size=800, node_shape='s')
nx.draw_networkx_labels(G, pos, labels, font_size=8)
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_edge_labels(G, pos, edge_labels=pesos)
plt.axis('off')
plt.show()
