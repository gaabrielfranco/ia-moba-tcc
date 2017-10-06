import json
import os
import glob
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

'''
Implementado por Gabriel Franco

Monta o grafo com as requisições e exporta o KDAN e o grafico

'''

G = nx.Graph()  #Grafo G
lista = []  #Lista de arquivos que não são partidas válidas
KDAN = {}   #Para cada player: (K, D, A, Npartidas)
arquivos = glob.glob(os.getcwd() + '\\Arquivos\\Partidas\\*.json')

print('Gerando grafo...')
it = 0
for j in arquivos:

    it += 1
    file = open(j, 'r')

    txt = file.read()

    txt_json = json.loads(txt)

    #Se existem 10 jogadores humanos na partida
    try:
        if (txt_json['result']['human_players'] == 10):
                dire_name = txt_json['result']['dire_name']
                radiant_name = txt_json['result']['radiant_name']
                
                #Relação jogador->time
                for k in range (0, len(txt_json['result']['players'])):
                    jogador = txt_json['result']['players'][k]['account_id']
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
                    
                
                #Relação jogador->jogador
                for k in range (0, len(txt_json['result']['players'])):
                    for l in range(k+1, len(txt_json['result']['players'])):
                        if txt_json['result']['players'][k]['player_slot'] < 5 and txt_json['result']['players'][l]['player_slot'] < 5:
                            G.add_edge(txt_json['result']['players'][k]['account_id'], txt_json['result']['players'][l]['account_id'])
                        elif txt_json['result']['players'][k]['player_slot'] > 5 and txt_json['result']['players'][l]['player_slot'] > 5:
                            G.add_edge(txt_json['result']['players'][k]['account_id'], txt_json['result']['players'][l]['account_id'])

        #Quando é um modelo de partida não válido, ele só ignora pra depois excluir
    except Exception:
            lista.append(j)

print('Grafo gerado com sucesso!')
print('Salvando Jogador/K/D/A/Numero de partidas em KDAN.txt')
arq = open('KDAN.txt', 'w')
for i in KDAN:
    arq.writelines(str(i) + ' ' + str(KDAN[i][0]) + ' '+ str(KDAN[i][1]) + ' ' + str(KDAN[i][2])+ ' ' + str(KDAN[i][3]) + '\n')
arq.close()

print('Salvando grafo em grafo.txt')
arq = open('grafo.txt', 'w', encoding='utf-16')
for i in G.edges():
    arq.writelines(str(i[0]) + ' -> ' + str(i[1]) + '\n')
arq.close()