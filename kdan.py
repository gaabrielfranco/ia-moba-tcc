# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 14:32:34 2017

@author: marcos
"""

#==============================================================================
# PASSO 1: montar uma base equivalente ao KDAN, porem completa, com os atributos abaixo - Feito
# PASSO 2: bolar uma metrica de eficiencia INDEPENDENTE de funcao (normalizar as variaveis da formula) - Feito
#        (K - D + A + max(denies, LH) + max(hero_damage, hero_healing) + max(gpm, xp_p_min)) / Npartidas
#        (K - D + A) / Npartidas
# PASSO 3: bolar uma metrica de eficiencia especifica para cada funcao (normalizar) - Pular
# PASSO 4: comparar media, desvio padrao, coef. de variacao e maximo e minimo antes e depois da poda por outliers em cada metrica - Feito
# PASSO 5: Fazer a mesma analise pra cada atributo individualmente (pra ver se surge algum insight) - Feito
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
import sys


def normaliza(x):
    xNorm = []
    minimo = np.min(x)
    maximo = np.max(x)
    for i in x:
        xNorm.append((i - minimo) / (maximo - minimo))

    return xNorm

# Parametro c arbitrario. Indica o quao relaxado se eh na poda


def removeOutliers(dados, c=2.0):
    novo = []
    media = np.average(dados)
    desvio = np.std(dados)
    count = 0
    for d in dados:
        if np.abs(media - d) < c * desvio:
            novo.append(d)
        else:
            count += 1
    return novo, count


def sumario(arq, eff):
    arq.write('Media: ' + str(np.average(eff)) + '\n')
    arq.write('Desvio: ' + str(np.std(eff)) + '\n')
    arq.write('Coef. Variacao: ' + str(np.std(eff) / np.average(eff)) + '\n')
    arq.write('Minimo: ' + str(np.min(eff)) + '\n')
    arq.write('Maximo: ' + str(np.max(eff)) + '\n')


def classification(file_name, received_data, received_eff):
    arq = open("files/" + file_name, 'w')

    data = normaliza(received_data)
    eff = normaliza(received_eff)

    arq.write("Antes da poda:\n")
    sumario(arq, eff)

    podado, nout = removeOutliers(eff)
    arq.write('\nRemovidos %d de %d jogadores\n' % (nout, len(eff)))

    arq.write('\nDepois da poda:\n')
    sumario(arq, podado)

    if file_name == "output_all_atributes.txt" or file_name == "output_kda.txt":
        km = KMeans(5)
        labels = km.fit_predict(data)

        contagens = [0] * 5
        for l in labels:
            contagens[l] += 1

        arq.write("\nResultado das classificacoes:\n")
        arq.write(str(contagens))


fp = open('files/atributes.txt', 'rU')
k = []
d = []
a = []
n = []
denies = []
gpm = []
hero_damage = []
hero_healing = []
lh = []
xp_p_min = []
eff_all = []
eff_kda = []
data_all = []
data_kda = []

for l in fp:
    partes = l.strip().split()
    for i, p in enumerate(partes):
        partes[i] = int(p)
    k.append(partes[1])
    d.append(partes[2])
    a.append(partes[3])
    n.append(partes[4])
    denies.append(partes[5])
    gpm.append(partes[6])
    hero_damage.append(partes[7])
    hero_healing.append(partes[8])
    lh.append(partes[9])
    xp_p_min.append(partes[10])

    data_all.append(partes[1:11])
    data_kda.append(partes[1:5])

    eff_kda.append((partes[1] + partes[3] - partes[2]) /
                   partes[4])  # (K + A - D / Npartidas)
    eff_all.append((partes[1] + partes[3] - partes[2] + max(partes[5], partes[9]) +
                    max(partes[7], partes[8]) + max(partes[6], partes[10])) / partes[4])

    # (K - D + A + max(denies, LH) + max(hero_damage, hero_healing) + max(gpm, xp_p_min)) / Npartidas

    # Ordem dos atributos:
    # (id_player,K, D, A, Npartidas, denies, gpm, hero_damage, hero_healing, LH, xp_p_min)

classification("output_all_atributes.txt", data_all, eff_all)
classification("output_kda.txt", data_kda, eff_kda)
classification("output_kills.txt", k, k)
classification("output_deaths.txt", d, d)
classification("output_assists.txt", a, a)
classification("output_n_partidas.txt", n, n)
classification("output_denies.txt", denies, denies)
classification("output_gpm.txt", gpm, gpm)
classification("output_hero_damage.txt", hero_damage, hero_damage)
classification("output_hero_healing.txt", hero_healing, hero_healing)
classification("output_lh.txt", lh, lh)
classification("output_xp_p_min.txt", xp_p_min, xp_p_min)
