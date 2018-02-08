#=================================================================================
# Versão 1: (K + A - D) / Npartidas
# Versão 2: (K + A - D + max(LH, denies)) / Npartidas
#
# - 10 execuções com random_state distintas, para K = 3, 4 e 5
#   - Para cada 10 execuções do passo acima, computar média e desvio para inércia
# - Manter normalização
# - Deixar outliers
# - No arquivo output_n_partidas.txt, incluir min e max absoluto (antes de normalizar)
#=================================================================================

import numpy as np
from sklearn.cluster import KMeans


def normaliza(x):
    xNorm = []
    minimo = np.min(x)
    maximo = np.max(x)
    for i in x:
        xNorm.append((i - minimo) / (maximo - minimo))

    return xNorm


def sumario(arq, eff):
    arq.write('Media: ' + str(np.average(eff)) + '\n')
    arq.write('Desvio: ' + str(np.std(eff)) + '\n')
    arq.write('Coef. Variacao: ' + str(np.std(eff) / np.average(eff)) + '\n')
    arq.write('Minimo: ' + str(np.min(eff)) + '\n')
    arq.write('Maximo: ' + str(np.max(eff)) + '\n')


def classification(k, data_all, data_kda):
    file_all = open('files/kmeans_all_' + str(k) + '.txt', 'w')
    file_kda = open('files/kmeans_kda_' + str(k) + '.txt', 'w')

    '''data_all = normaliza(data_all)
    data_kda = normaliza(data_kda)'''

    inertia = []

    # All attributes
    for i in range(0, 10):
        print('All: Semente %d...' % i)
        file_all.write('Iteracao ' + str(i) + ':\n')
        km = KMeans(n_clusters=k, random_state=i, n_jobs=4)
        labels = km.fit_predict(data_all)

        inertia.append(km.inertia_)
        file_all.write('\tInertia da Iteracao ' + str(i) + ':\n')
        file_all.write('\t' + str(km.inertia_) + '\n\n')
        contagens = [0] * k
        for l in labels:
            contagens[l] += 1
        file_all.write('\tContagem da Iteracao ' + str(i) + ':\n')
        file_all.write('\t' + str(contagens) + '\n\n')
        
        file_all.write('\tCentroides da Iteracao ' + str(i) + ':\n')
        file_all.write('\t' + str(km.cluster_centers_) + '\n\n')

    file_all.write('Dados da metrica inertia: \n')
    sumario(file_all, inertia)

    inertia.clear()

    # KDA attributes
    for i in range(0, 10):
        print('KDA: Semente %d...' % i)
        file_kda.write('Iteracao ' + str(i) + ':\n\n')
        km = KMeans(n_clusters=k, random_state=i, n_jobs=4)
        labels = km.fit_predict(data_kda)

        inertia.append(km.inertia_)
        file_kda.write('\tInertia da Iteracao ' + str(i) + ':\n')
        file_kda.write('\t' + str(km.inertia_) + '\n\n')
        contagens = [0] * k
        for l in labels:
            contagens[l] += 1
        file_kda.write('\tContagem da Iteracao ' + str(i) + ':\n')
        file_kda.write('\t' + str(contagens) + '\n\n')
        
        file_kda.write('\tCentroides da Iteracao ' + str(i) + ':\n')
        file_kda.write('\t' + str(km.cluster_centers_) + '\n\n')

    file_kda.write('Dados da metrica inertia: \n')
    sumario(file_kda, inertia)

    file_all.close()
    file_kda.close()


def main():
    data_all = []
    data_kda = []

    fp = open('files/atributes.txt', 'rU')

    for l in fp:
        partes = l.strip().split()
        for i, p in enumerate(partes):
            partes[i] = int(p)
        if partes[4] >= 5:
            data_all.append(list(np.array(partes[1:4] + [partes[5]] + [partes[9]])/partes[4]))
            data_kda.append(list(np.array(partes[1:4])/partes[4]))

    fp.close()
    
    for k in [3,4,5]:
        classification(k, data_all, data_kda)


if __name__ == "__main__":
    main()
