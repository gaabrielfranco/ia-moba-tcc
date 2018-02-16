'''
Implementado por Gabriel Franco

Ordem dos atributos:
    (id_player,K, D, A, Npartidas, denies, gpm, hero_damage, hero_healing, LH, xp_p_min)

eff_kda = (K + A - D) / n_partidas
eff_all = (K - D + A + max(denies, LH) + max(hero_damage, hero_healing) / n_partidas

'''

import numpy as np
from sklearn.cluster import KMeans
import json


def normalizes(x):
    xNorm = []
    minimum = np.min(x)
    maximum = np.max(x)
    for i in x:
        xNorm.append((i - minimum) / (maximum - minimum))

    return xNorm


def remove_outliers(dados, c=2.0):
    new = []
    avg = np.average(dados)
    std = np.std(dados)
    count = 0
    for d in dados:
        if np.abs(avg - d) < c * std:
            new.append(d)
        else:
            count += 1
    return new, count


def summary(arq, eff, out_json, attribute, it, label):
    avg = np.average(eff)
    std = np.std(eff)
    coef_var = std / avg
    maximum = np.max(eff)
    minimum = np.min(eff)

    out_json[attribute][it] = {
        "label": label,
        "media": avg,
        "desvio": std,
        "coef_var": coef_var,
        "min": minimum,
        "max": maximum
    }
    arq.write('Media: ' + str(avg) + '\n')
    arq.write('Desvio: ' + str(std) + '\n')
    arq.write('Coef. Variacao: ' +
              str(coef_var) + '\n')
    arq.write('Minimo: ' + str(minimum) + '\n')
    arq.write('Maximo: ' + str(maximum) + '\n')


def classification(attribute, received_eff, n, out_json):
    file_name = 'output_' + attribute + '.txt'
    arq = open("files/output_attributes_analysis/" + file_name, 'w')

    defaut_object = {"label": None, "media": None, "desvio": None,
                     "coef_var": None, "min": None, "max": None}

    out_json[attribute] = [defaut_object] * 5

    eff_normalized = list(np.array(received_eff) / np.array(n))

    eff = normalizes(received_eff)

    arq.write("Sumario de valores normalizados por partida (minimo 5 partidas):\n")
    summary(arq, eff_normalized, out_json, attribute, 0,
            "Sumario de valores normalizados por partida")

    arq.write(
        '\n==================================================================\n\n')

    arq.write("Antes da poda de outliers com normalizacao min-max:\n")
    summary(arq, eff, out_json, attribute, 1,
            "Antes da poda de outliers com normalizacao min-max")

    podado, nout = remove_outliers(eff)
    arq.write('\nRemovidos %d de %d jogadores\n' % (nout, len(eff)))

    arq.write('\nDepois da poda de outliers com normalizacao min-max:\n')
    summary(arq, podado, out_json, attribute, 2,
            "Depois da poda de outliers com normalizacao min-max")

    arq.write(
        '\n==================================================================\n\n')

    eff_normalized = normalizes(eff_normalized)
    arq.write("Antes da poda de outliers com normalizacao por partidas e min-max:\n")
    summary(arq, eff_normalized, out_json, attribute, 3,
            "Antes da poda de outliers com normalizacao por partidas e min-max")

    podado, nout = remove_outliers(eff_normalized)
    arq.write('\nRemovidos %d de %d jogadores\n' % (nout, len(eff_normalized)))

    arq.write(
        '\nDepois da poda de outliers com normalizacao por partidas e min-max:\n')
    summary(arq, podado, out_json, attribute, 4,
            "Depois da poda de outliers com normalizacao por partidas e min-max")


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
    out_json = {}

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

    classification("all_attributes", eff_all, n, out_json)
    classification("kda", eff_kda, n, out_json)
    classification("kills", k, n, out_json)
    classification("deaths", d, n, out_json)
    classification("assists", a, n, out_json)
    classification("denies", denies, n, out_json)
    classification("gpm", gpm, n, out_json)
    classification("hero_damage", hero_damage, n, out_json)
    classification("hero_healing", hero_healing, n, out_json)
    classification("lh", lh, n, out_json)
    classification("xp_p_min", xp_p_min, n, out_json)

    outfile = open('files/output_attributes_analysis/outputs.json', 'w')
    json.dump(out_json, outfile, indent=4)
    outfile.close()


if __name__ == "__main__":
    main()
