'''
Implementado por Gabriel Franco

Ordem dos atributos:
    (id_player,K, D, A, Npartidas, denies, gpm, hero_damage, hero_healing, LH, xp_p_min)

eff_kda = (K + A - D) / n_partidas
eff_all = (K - D + A + max(denies, LH) + max(hero_damage, hero_healing) / n_partidas

'''

import numpy as np
from sklearn.cluster import KMeans


def normalizes(x):
    xNorm = []
    minimo = np.min(x)
    maximo = np.max(x)
    for i in x:
        xNorm.append((i - minimo) / (maximo - minimo))

    return xNorm


def remove_outliers(dados, c=2.0):
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


def summary(arq, eff):
    arq.write('Media: ' + str(np.average(eff)) + '\n')
    arq.write('Desvio: ' + str(np.std(eff)) + '\n')
    arq.write('Coef. Variacao: ' + str(np.std(eff) / np.average(eff)) + '\n')
    arq.write('Minimo: ' + str(np.min(eff)) + '\n')
    arq.write('Maximo: ' + str(np.max(eff)) + '\n')


def classification(file_name, received_eff, n):
    arq = open("files/output_atributtes_analysis/" + file_name, 'w')
    eff_normalized = list(np.array(received_eff) / np.array(n))

    eff = normalizes(received_eff)

    arq.write("Sumario de valores normalizados por partida (minimo 5 partidas):\n")
    summary(arq, eff_normalized)

    arq.write(
        '\n==================================================================\n\n')

    arq.write("Antes da poda de outliers com normalizacao min-max:\n")
    summary(arq, eff)

    podado, nout = remove_outliers(eff)
    arq.write('\nRemovidos %d de %d jogadores\n' % (nout, len(eff)))

    arq.write('\nDepois da poda de outliers com normalizacao min-max:\n')
    summary(arq, podado)

    arq.write(
        '\n==================================================================\n\n')

    eff_normalized = normalizes(eff_normalized)
    arq.write("Antes da poda de outliers com normalizacao por partidas e min-max:\n")
    summary(arq, eff_normalized)

    podado, nout = remove_outliers(eff_normalized)
    arq.write('\nRemovidos %d de %d jogadores\n' % (nout, len(eff_normalized)))

    arq.write(
        '\nDepois da poda de outliers com normalizacao por partidas e min-max:\n')
    summary(arq, podado)


def main():
    fp = open('files/attributes.txt', 'rU')
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
        parts = l.strip().split()
        for i, p in enumerate(parts):
            parts[i] = int(p)

        # This if reduces the database of 74133 players to 20544 players
        if parts[4] >= 5:
            k.append(parts[1])
            d.append(parts[2])
            a.append(parts[3])
            n.append(parts[4])
            denies.append(parts[5])
            gpm.append(parts[6])
            hero_damage.append(parts[7])
            hero_healing.append(parts[8])
            lh.append(parts[9])
            xp_p_min.append(parts[10])

            eff_kda.append((parts[1] + parts[3] - parts[2]) /
                           parts[4])
            eff_all.append((parts[1] + parts[3] - parts[2] + max(parts[5], parts[9]) +
                            max(parts[7], parts[8]) + max(parts[6], parts[10])) / parts[4])

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


if __name__ == "__main__":
    main()
