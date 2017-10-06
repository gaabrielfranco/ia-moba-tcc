import networkx as nx
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np
from scipy.optimize import curve_fit
import math
import os

'''
Implementado por Gabriel Franco

Gera alguns gráficos

'''

KDAN = {}
xK = []
yK = []
xD = []
yD = []
xA = []
yA = []
xKM = []
yKM = []
xDM = []
yDM = []
xAM = []
yAM = []

file = open('\\files\\KDAN.txt', 'r')
txt = file.readlines()

for i in txt:
    l = i.split(' ')
    if (int(l[4]) > 10):
        KDAN[int(l[0])] = (int(l[1]), int(l[2]), int(l[3]), int(l[4]))
        
Kills = [0 for x in range(1, len(KDAN))]
Deaths = [0 for x in range(1, len(KDAN))]
Assists = [0 for x in range(1, 2*len(KDAN))]
KillsMedio = [0 for x in range(1, len(KDAN))]
DeathsMedio = [0 for x in range(1, len(KDAN))]
AssistsMedio = [0 for x in range(1, len(KDAN))]

for i in KDAN.values():
    Kills[i[0]] += 1 #frequencia desse numero j[1] de kills
    KillsMedio[math.ceil(i[0]/i[3])] += 1 #frequencia desse numero j[1]/j[3] (numero medio) de kills
    Deaths[i[1]] += 1 
    DeathsMedio[i[1]//i[3]] += 1 
    Assists[i[2]] += 1 
    AssistsMedio[i[2]//i[3]] += 1

for i,j in enumerate(Kills):
    if (j > 0):
        xK.append(i)
        yK.append(j)

for i,j in enumerate(KillsMedio):
    if i > 0:
        if (j > 0):
            xKM.append(i)
            yKM.append(j)

for i,j in enumerate(Deaths):
    if (j > 0):
        xD.append(i)
        yD.append(j)

for i,j in enumerate(DeathsMedio):
    if (j > 0):
        xDM.append(i)
        yDM.append(j)

for i,j in enumerate(Assists):
    if (j > 0):
        xA.append(i)
        yA.append(j)

for i,j in enumerate(AssistsMedio):
    if (j > 0):
        xAM.append(i)
        yAM.append(j)

print('Plot dos graficos')

try:
    os.mkdir('Gráficos')
except Exception as e:
    print('Erro', 'O seguinte erro ocorreu: %s' % str(e.args))

#Plot das kills
fig = plt.figure()
plt.ylabel("Número de jogadores")
#plt.title('Abates')
plt.xlabel("Abates")
plt.plot(xK, yK, 'ko', ms = 2.5, alpha=0.15)
#plt.plot(xK, yK, 'ko', ms = 2.5)   #Exemplo de plot em log. Só em um eixo é semilogx ou semilogy  (depois testar log só no eixo x), mudar base = basex=2
fig.savefig('Gráficos\\abates.png', dpi=fig.dpi)

#Plot das kills/numero de partidas
fig = plt.figure()
plt.ylabel("Número de jogadores")
plt.xlabel("Abates/número de partidas")
plt.plot(xKM, yKM, 'ko', ms = 2.5)
fig.savefig('Gráficos\\abates_medio.png', dpi=fig.dpi)


#Plot das deaths
fig = plt.figure()
plt.ylabel("Número de jogadores")
plt.xlabel("Mortes")
plt.plot(xD, yD, 'ko', ms = 2.5, alpha=0.15)
fig.savefig('Gráficos\\mortes.png', dpi=fig.dpi)


#Plot das deaths/numero de partidas
fig = plt.figure()
plt.ylabel("Número de jogadores")
plt.xlabel("Mortes/número de partidas")
plt.plot(xDM, yDM, 'ko', ms = 2.5)
fig.savefig('Gráficos\\mortes_medio.png', dpi=fig.dpi)


#Plot das assists
fig = plt.figure()
plt.ylabel("Número de jogadores")
plt.xlabel("Assistências")
plt.plot(xA, yA, 'ko', ms = 2.5, alpha=0.15)
fig.savefig('Gráficos\\assistencias.png', dpi=fig.dpi)


#Plot das assists/numero de partidas
fig = plt.figure()
plt.ylabel("Número de jogadores")
plt.xlabel("Assistências/número de partidas")
plt.plot(xAM, yAM, 'ko', ms = 2.5)
plt.axis([-2, 30, -10, 2000])

fig.savefig('Gráficos\\assistencias_medio.png', dpi=fig.dpi)

print('Gráficos salvos na subpasta Gráficos')