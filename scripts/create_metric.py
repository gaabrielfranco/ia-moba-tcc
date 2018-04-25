from modules.data import read_data, normalizes

########################################
#          About attributes            #
# K: higher => better                  #
# D: lower => melhor                   #
# A: higher => better                  #
# denies: higher => better             #
# gpm: higher => better                #
# hd: higher => better                 #
# hh: higher => better                 #
# lh: higher => better                 #
# xpm: higher => better                #
########################################

# Feature selection result: (assists, deaths, denies, gpm, hh)


def main():
    data_pruned = read_data('pruned')
    data, _, _ = normalizes(data_pruned['all'])
    A1, B1, A2, B2 = 0.0, 0.0, 0.0, 0.0

    for player in data:
        A1 += (player[0] + player[2] + player[3] +
               player[4] + player[5] + player[6] + player[7] + player[8])
        B1 += player[1]
        A2 += (player[2] + player[3] + player[4] + player[6])
        B2 += player[1]

    print('All attributes')
    print('A1 = ', A1)
    print('B1 = ', B1)
    print('S1 = A1 - B1 = ', A1 - B1)
    print('\nFeature selection attributes')
    print('A2 = ', A2)
    print('B2 = ', B2)
    print('S2 = A2 - B2 = ', A2 - B2)


if __name__ == "__main__":
    main()
