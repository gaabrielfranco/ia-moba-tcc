'''
Implementado por Gabriel Franco
'''

import numpy as np
from sklearn.cluster import KMeans


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


def classification(file_name, received_eff, n):
    arq = open("files/output_atributtes_analysis/" + file_name, 'w')
    eff_normalized = list(np.array(received_eff) / np.array(n))

    eff = normaliza(received_eff)

    arq.write("Sumario de valores normalizados por partida (minimo 5 partidas):\n")
    sumario(arq, eff_normalized)

    arq.write(
        '\n==================================================================\n\n')

    arq.write("Antes da poda de outliers com normalizacao min-max:\n")
    sumario(arq, eff)

    podado, nout = removeOutliers(eff)
    arq.write('\nRemovidos %d de %d jogadores\n' % (nout, len(eff)))

    arq.write('\nDepois da poda de outliers com normalizacao min-max:\n')
    sumario(arq, podado)

    arq.write(
        '\n==================================================================\n\n')

    eff_normalized = normaliza(eff_normalized)
    arq.write("Antes da poda de outliers com normalizacao por partidas e min-max:\n")
    sumario(arq, eff_normalized)

    podado, nout = removeOutliers(eff_normalized)
    arq.write('\nRemovidos %d de %d jogadores\n' % (nout, len(eff_normalized)))

    arq.write(
        '\nDepois da poda de outliers com normalizacao por partidas e min-max:\n')
    sumario(arq, podado)


fp = open('files/atributtes.txt', 'rU')
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

for l in fp:
    partes = l.strip().split()
    for i, p in enumerate(partes):
        partes[i] = int(p)

    # Considerar esse if reduz a base de 74133 jogadores para 20544 jogadores
    if partes[4] >= 5:
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

        eff_kda.append((partes[1] + partes[3] - partes[2]) /
                       partes[4])  # (K + A - D / Npartidas)
        eff_all.append((partes[1] + partes[3] - partes[2] + max(partes[5], partes[9]) +
                        max(partes[7], partes[8]) + max(partes[6], partes[10])) / partes[4])

        # (K - D + A + max(denies, LH) + max(hero_damage, hero_healing) + max(gpm, xp_p_min)) / n_partidas

        # Ordem dos atributos:
        # (id_player,K, D, A, Npartidas, denies, gpm, hero_damage, hero_healing, LH, xp_p_min)

classification("output_all_atributtes.txt", eff_all, n)
classification("output_kda.txt", eff_kda, n)
classification("output_kills.txt", k, n)
classification("output_deaths.txt", d, n)
classification("output_assists.txt", a, n)
classification("output_denies.txt", denies, n)
classification("output_gpm.txt", gpm, n)
classification("output_hero_damage.txt", hero_damage, n)
classification("output_hero_healing.txt", hero_healing, n)
classification("output_lh.txt", lh, n)
classification("output_xp_p_min.txt", xp_p_min, n)
