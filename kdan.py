# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 14:32:34 2017

@author: marcos
"""

#==============================================================================
# PASSO 1: montar uma base equivalente ao KDAN, porem completa, com os atributos abaixo - Feito
# PASSO 2: bolar uma metrica de eficiencia INDEPENDENTE de funcao (normalizar as variaveis da formula)
# PASSO 3: bolar uma metrica de eficiencia especifica para cada funcao (normalizar)
# PASSO 4: comparar media, desvio padrao, coef. de variacao e maximo e minimo antes e depois da poda por outliers em cada metrica
# PASSO 5: Fazer a mesma analise pra cada atributo individualmente (pra ver se surge algum insight)
# PASSO 6: Cluster por atributos dependentes de funcao (5 clusters = 5 funcoes)
#==============================================================================

#==============================================================================
# k => kills
# d => deaths
# a => assists
# n => n partidas
# den => denies (depende de funcao)
# gold_per_min (depende de funcao)
# hero_damage (depende de funcao)
# hero_healing (depende de fcn)
# last_hits => numero de unidades mortas (morte: gold + xp) (depende de fcn)
# level => analogo a rpg (não vai ter utilidade)
# xp_per_min
# Os seguintes atributos estarao em arquivo separado
# item_0 a item_5 (array de itens influencia na funcao do player) 
#==============================================================================

import numpy as np
from sklearn.cluster import KMeans

def normaliza(x):
    xNorm = []
    minimo = np.min(x)
    maximo = np.max(x)
    for i in x:
        xNorm.append((x-minimo)/(maximo-minimo))

    return xNorm

# Parametro c arbitrario. Indica o quao relaxado se eh na poda
def removeOutliers(dados, c=2.0):
    novo = []
    media = np.average(dados)
    desvio = np.std(dados)
    count = 0
    for d in dados:
        if np.abs(media - d) < c*desvio:
            novo.append(d)
        else:
            count += 1
    return novo, count

def sumario(eff):
    print('Media:', np.average(eff))
    print('Desvio:', np.std(eff))
    print('Coef. Variacao:', np.std(eff)/np.average(eff))
    print('Minimo:', np.min(eff))
    print('Maximo:', np.max(eff))

arq = '\\files\\KDAN.txt'

fp = open(arq, 'rU')
k = []
d = []
a = []
n = []
eff = []
data = []
for l in fp:
    partes = l.strip().split()
    for i,p in enumerate(partes):
        partes[i] = int(p)
    k.append(partes[1])
    d.append(partes[2])
    a.append(partes[3])
    n.append(partes[4])
    data.append(partes[1:5])
    eff.append((partes[1]+partes[3]-partes[2])/partes[4])

print("Antes da poda:")
sumario(eff)

podado, nout = removeOutliers(eff)
print('\nRemovidos %d de %d jogadores' % (nout, len(eff)))

print('\nDepois da poda')
sumario(podado)

km = KMeans(4)
labels = km.fit_predict(data)

contagens = [0]*4
for l in labels:
    contagens[l] += 1

print(contagens)

print("Antes da poda:")
sumario(n)

n2,nout = removeOutliers(n)
print('\nRemovidos %d de %d jogadores' % (nout, len(n)))
print('\nDepois da poda')
sumario(n2)
