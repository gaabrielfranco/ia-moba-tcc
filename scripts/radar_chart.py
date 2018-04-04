import pandas as pd
import numbers
import matplotlib.pyplot as plt
import numpy as np

# =============================================================================
# Parametros: dados => DataFrame Pandas com os dados
#             titulo => titulo do grafico
#             excluir => lista de campos que nao participam do plot
#             rotulo => nome do campo que sera utilizado como rotulo de cada serie de dados (individuo/linha do DataFrame)
# =============================================================================

def radarplot(dados, titulo=None, excluir=None, rotulo=None):
    candidatos = list(dados.columns)
    dimensoes = []
    for i,c in enumerate(candidatos):
        if isinstance(dados.loc[0, c], numbers.Number):
            if excluir is not None:
                if c not in excluir:
                    dimensoes.append(candidatos[i])
            else:
                dimensoes.append(candidatos[i])
                
    dimensoes = np.array(dimensoes)
    angulos = np.linspace(0, 2*np.pi, len(dimensoes), endpoint=False)
    angulos = np.concatenate((angulos, [angulos[0]]))
    
    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)
    for i in dados.index:
        valores = dados[dimensoes].loc[i].values
        valores = np.concatenate((valores, [valores[0]]))
        ax.plot(angulos, valores, 'o-', linewidth=2, label=dados[rotulo].loc[i])
        ax.fill(angulos, valores, alpha=0.25)
    ax.set_thetagrids(angulos * 180/np.pi, dimensoes)
    if titulo is not None:
        ax.set_title(titulo)
    ax.grid(True)
    plt.legend(loc='center left', bbox_to_anchor=(1.1, 0.5))
    plt.show()
    

xls = pd.ExcelFile('alunos.xlsx')
dados = pd.read_excel(xls, 'Notas')
radarplot(dados, titulo='Perfil dos Alunos', excluir=['Matrícula', 'Nota Final'], rotulo='Nome')
