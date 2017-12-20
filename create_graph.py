import json
import os
import glob
import networkx as nx
import numpy as np
#import matplotlib.pyplot as plt
#from scipy.stats import linregress

'''
Implementado por Gabriel Franco

Monta o grafo com as requisições e exporta o KDAN e o grafico

'''

G = nx.Graph()  # Grafo G
lista = []  # Lista de arquivos que não são partidas válidas
lista2 = []
lista3 = []
KDAN = {}  # Para cada player: (K, D, A, Npartidas)

# para cada player, (id_player,K, D, A, Npartidas, denies, gpm, hero_damage, hero_healing, LH, xp_p_min)

atributes = {}
arquivos = glob.glob(os.getcwd() + os.path.sep + 'Arquivos' +
                     os.path.sep + 'Partidas' + os.path.sep + '*.json')

print('Gerando grafo...')
it = 0
print(len(arquivos))
for j in arquivos:

    it += 1
    print(it)
    file = open(j, 'r')

    txt = file.read()

    txt_json = json.loads(txt)

# Se existem 10 jogadores humanos na partida
    try:
        if (txt_json['result']['human_players'] == 10):

            # Criando lista de partidas inválidas
            try:
                dire_name = txt_json['result']['dire_name']
                radiant_name = txt_json['result']['radiant_name']
            except Exception:
                lista.append(j)

            # Relação jogador->time
            for k in range(0, len(txt_json['result']['players'])):
                jogador = txt_json['result']['players'][k]['account_id']

                '''
                if jogador < 5:
                    G.add_edge(txt_json['result']['players'][k]['account_id'], dire_name)
                else:
                    G.add_edge(txt_json['result']['players'][k]['account_id'], radiant_name)

                #KDA do jogador
                if jogador in KDAN:
                    KDAN[jogador] = (KDAN[jogador][0] + txt_json['result']['players'][k]['kills'], KDAN[jogador][1] + \
                    txt_json['result']['players'][k]['deaths'], KDAN[jogador][2] + txt_json['result']['players'][k]['assists'], KDAN[jogador][3] + 1)
                else:
                    KDAN[jogador] = (txt_json['result']['players'][k]['kills'], txt_json['result']['players'][k]['deaths'], \
                    txt_json['result']['players'][k]['assists'], 1)
                '''
                if jogador in atributes:
                    atributes[jogador] = (atributes[jogador][0] + txt_json['result']['players'][k]['kills'], atributes[jogador][1] +
                                          txt_json['result']['players'][k]['deaths'], atributes[jogador][2] +
                                          txt_json['result']['players'][k]['assists'],
                                          atributes[jogador][3] + 1, atributes[jogador][4] +
                                          txt_json['result']['players'][k]['denies'], atributes[jogador][5]
                                          + txt_json['result']['players'][k]['gold_per_min'], atributes[jogador][6] +
                                          txt_json['result']['players'][k]['hero_damage'],
                                          atributes[jogador][7] + txt_json['result']['players'][k]['hero_healing'], atributes[jogador][8] +
                                          txt_json['result']['players'][k]['last_hits'],
                                          atributes[jogador][9] + txt_json['result']['players'][k]['xp_per_min'])
                else:
                    atributes[jogador] = (txt_json['result']['players'][k]['kills'], txt_json['result']['players'][k]['deaths'],
                                          txt_json['result']['players'][k]['assists'], 1, txt_json['result'][
                        'players'][k]['denies'], txt_json['result']['players'][k]['gold_per_min'],
                        txt_json['result']['players'][k]['hero_damage'], txt_json['result']['players'][k]['hero_healing'],
                        txt_json['result']['players'][k]['last_hits'], txt_json['result']['players'][k]['xp_per_min'])
    except Exception:
        if not(j in lista):
            lista2.append(j)
        continue

    # Sem nenhum pau
    if not(j in lista) and not(j in lista2):
        lista3.append(j)
        '''
            #Relação jogador->jogador
            for k in range (0, len(txt_json['result']['players'])):
                for l in range(k+1, len(txt_json['result']['players'])):
                    if txt_json['result']['players'][k]['player_slot'] < 5 and txt_json['result']['players'][l]['player_slot'] < 5:
                        G.add_edge(txt_json['result']['players'][k]['account_id'], txt_json['result']['players'][l]['account_id'])
                    elif txt_json['result']['players'][k]['player_slot'] > 5 and txt_json['result']['players'][l]['player_slot'] > 5:
                        G.add_edge(txt_json['result']['players'][k]['account_id'], txt_json['result']['players'][l]['account_id'])
            '''
    # Quando é um modelo de partida não válido, ele só ignora pra depois excluir


print('Salvando arquivos...')
arq = open(os.getcwd() + os.path.sep + 'files' +
           os.path.sep + 'atributes.txt', 'w')
for i in atributes:
    arq.writelines(str(i) + ' ' + str(atributes[i][0]) + ' ' + str(atributes[i][1]) + ' ' + str(atributes[i][2]) + ' ' + str(atributes[i][3])
                   + ' ' + str(atributes[i][4]) + ' ' + str(atributes[i][5]) + ' ' + str(
                       atributes[i][6]) + ' ' + str(atributes[i][7]) + ' ' + str(atributes[i][8])
                   + ' ' + str(atributes[i][9]) + '\n')
arq.close()


arq = open(os.getcwd() + os.path.sep + 'files' +
           os.path.sep + 'invalids_matches_without_team_name.txt', 'w')
for i in lista:
    arq.writelines(str(i) + '\n')
arq.close()

arq = open(os.getcwd() + os.path.sep + 'files' +
           os.path.sep + 'invalids_matches_with_another_error.txt', 'w')
for i in lista2:
    arq.writelines(str(i) + '\n')
arq.close()

arq = open(os.getcwd() + os.path.sep + 'files' +
           os.path.sep + 'valid_matches.txt', 'w')
for i in lista3:
    arq.writelines(str(i) + '\n')
arq.close()

'''
print('Salvando grafo em grafo.txt')
arq = open('\\files\\grafo.txt', 'w', encoding='utf-16')
for i in G.edges():
    arq.writelines(str(i[0]) + ' -> ' + str(i[1]) + '\n')
arq.close()
'''
