import json
import sys
import os
import time
import urllib3
import glob

'''
Implementado por Gabriel Franco

Faz as requisições de todas as partidas das ligas disponíveis na API e salva tudo em arquivos json
'''

ligas = []
partidas = []

#COLETA DAS LIGAS E PARTIDAS DAS LIGAS
print('Fazendo a coleta das ligas...')
http = urllib3.PoolManager(num_pools=110000)

r = http.request('GET', 'http://api.steampowered.com/IDOTA2Match_570/GetLeagueListing/v1?key=EAF3EC985E0B67D77A2B0321A2066AC7')
resultJSON = json.loads(r.data.decode('utf-8'))

print('Salvando o resultado no arquivo ligas.json...')
try:
    os.mkdir('files')
except Exception as e:
    print('Erro', 'O seguinte erro ocorreu: %s' % str(e.args))
outfile = open('files\\ligas.json', 'w')

json.dump(resultJSON , outfile, sort_keys=True, indent= 4)

for i in range(len(resultJSON['result']['leagues'])):
    ligas.append(resultJSON['result']['leagues'][i]['leagueid'])

a = input('A pasta Arquivos e suas subpastas, que contem todas as requisições de ligas e partidas, será criada. Aperte alguma tecla para continuar...')
try:
    os.mkdir('Arquivos')
    os.mkdir('Arquivos\\Ligas')
    os.mkdir('Arquivos\\Partidas')
except Exception as e:
    print('Erro', 'O seguinte erro ocorreu: %s' % str(e.args))

print('Salvando as lista de partidas das ligas na subpasta Ligas...')
for i in ligas:
    try:
        r = http.request('GET', 'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v1?key=EAF3EC985E0B67D77A2B0321A2066AC7&league_id=' + str(i))
        resultJSON = json.loads(r.data.decode('utf-8'))
        with open('Arquivos\\Ligas\\Partidas da liga ' + str(i) + '.json', 'w') as outfile:
            json.dump(resultJSON, outfile, sort_keys = True, indent = 4)
    except Exception as e:
        print('Erro', 'O seguinte erro ocorreu: %s' % str(e.args))

#COLETA INDIVIDUAL DAS PARTIDAS
print('Coletando os id\'s das partidas das ligas (ligas com menos de 20 partidas são ignoradas)...')
partidasLigas = glob.glob(os.getcwd() + '\\Arquivos\\Ligas\\*.json')

for i in partidasLigas:
    file = open(i, 'r')
    txt = file.read()
    txt_json = json.loads(txt)

    #Liga ter pelo menos 20 partidas
    if (len(txt_json['result']['matches']) > 20):
        for j in range(len(txt_json['result']['matches'])):
            partidas.append(txt_json['result']['matches'][j]['match_id'])

print('Fazendo a coleta das partidas...')
for i in partidas:
    try:
        r = http.request('GET', 'http://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v1?key=EAF3EC985E0B67D77A2B0321A2066AC7&match_id=' + str(i))
        resultJSON = json.loads(r.data.decode('utf-8'))
        with open('Arquivos\\Partidas\\Partida ' + str(i) + '.json', 'w') as outfile:
            json.dump(resultJSON, outfile, sort_keys = True, indent = 4)
    except Exception as e:
        print('Erro', 'O seguinte erro ocorreu: %s' % str(e.args))