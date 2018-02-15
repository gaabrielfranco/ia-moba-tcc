import json
import os
import glob
import numpy as np

'''
Implementado por Gabriel Franco

Cria arquivos de atributos e de partidas inválidas

Atributos do player: (id_player,K, D, A, Npartidas, denies, gpm, hero_damage, hero_healing, LH, xp_p_min)
'''

invalids_matches_without_team_name = []
invalids_matches_with_another_error = []
valid_matches = []

atributes = {}
arquivos = glob.glob(os.getcwd() + os.path.sep + 'Arquivos' +
                     os.path.sep + 'Partidas' + os.path.sep + '*.json')

it = 0
for j in arquivos:

    print('Iteration %d' % it)
    it += 1
    file = open(j, 'r')

    txt = file.read()

    txt_json = json.loads(txt)

    try:
        if (txt_json['result']['human_players'] == 10):

            try:
                dire_name = txt_json['result']['dire_name']
                radiant_name = txt_json['result']['radiant_name']
            except Exception:
                invalids_matches_without_team_name.append(j)

            for k in range(0, len(txt_json['result']['players'])):
                player = txt_json['result']['players'][k]['account_id']
                if player in atributes:
                    atributes[player] = (atributes[player][0] + txt_json['result']['players'][k]['kills'], atributes[player][1] +
                                         txt_json['result']['players'][k]['deaths'], atributes[player][2] +
                                         txt_json['result']['players'][k]['assists'],
                                         atributes[player][3] + 1, atributes[player][4] +
                                         txt_json['result']['players'][k]['denies'], atributes[player][5]
                                         + txt_json['result']['players'][k]['gold_per_min'], atributes[player][6] +
                                         txt_json['result']['players'][k]['hero_damage'],
                                         atributes[player][7] + txt_json['result']['players'][k]['hero_healing'], atributes[player][8] +
                                         txt_json['result']['players'][k]['last_hits'],
                                         atributes[player][9] + txt_json['result']['players'][k]['xp_per_min'])
                else:
                    atributes[player] = (txt_json['result']['players'][k]['kills'], txt_json['result']['players'][k]['deaths'],
                                         txt_json['result']['players'][k]['assists'], 1, txt_json['result'][
                        'players'][k]['denies'], txt_json['result']['players'][k]['gold_per_min'],
                        txt_json['result']['players'][k]['hero_damage'], txt_json['result']['players'][k]['hero_healing'],
                        txt_json['result']['players'][k]['last_hits'], txt_json['result']['players'][k]['xp_per_min'])
    except Exception:
        if not(j in invalids_matches_without_team_name):
            invalids_matches_with_another_error.append(j)
        continue

    if not(j in invalids_matches_without_team_name) and not(j in invalids_matches_with_another_error):
        valid_matches.append(j)


print('Saving files...')
arq = open(os.getcwd() + os.path.sep + 'files' +
           os.path.sep + 'atributtes.txt', 'w')
for i in atributes:
    arq.writelines(str(i) + ' ' + str(atributes[i][0]) + ' ' + str(atributes[i][1]) + ' ' + str(atributes[i][2]) + ' ' + str(atributes[i][3])
                   + ' ' + str(atributes[i][4]) + ' ' + str(atributes[i][5]) + ' ' + str(
                       atributes[i][6]) + ' ' + str(atributes[i][7]) + ' ' + str(atributes[i][8])
                   + ' ' + str(atributes[i][9]) + '\n')
arq.close()

arq = open(os.getcwd() + os.path.sep + 'files' +
           os.path.sep + 'invalids_matches_without_team_name.txt', 'w')
for i in invalids_matches_without_team_name:
    arq.writelines(str(i) + '\n')
arq.close()

arq = open(os.getcwd() + os.path.sep + 'files' +
           os.path.sep + 'invalids_matches_with_another_error.txt', 'w')
for i in invalids_matches_with_another_error:
    arq.writelines(str(i) + '\n')
arq.close()

arq = open(os.getcwd() + os.path.sep + 'files' +
           os.path.sep + 'valid_matches.txt', 'w')
for i in valid_matches:
    arq.writelines(str(i) + '\n')
arq.close()
