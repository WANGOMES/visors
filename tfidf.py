'''
#################################################################################################
AUTOR: WANDERSON ANTONIO COSTA GOMES
TRABALHO ACADEMICO: VIGILANCIA SOCIOASSISTENCIAL: MONITORAMENTO DE RISCOS E VULNERABILIDADES EM 
TEMPO REAL POR MEIO DE MINERAÇÃO DE TEXTO NO TWITTER
UNIVERSIDADE: PONTIFÍCIA UNIVERSIDADE CATÓLICA DE MINAS GERAIS - PUCMINAS (UNID. SÃO GABRIEL)
CIDADE: BELO HORIZONTE / MG - BRASIL                            ANO: 2020
NOME PROTOTIPO: VISORS - VIGILANCIA SOCIOASSISTENCIAL EM REDES SOCIAIS
PALAVRAS-CHAVE: Vigilância Socioassistencial. Monitoramento em Tempo Real. Mineração de Dados. 
Mineração de Texto.
#################################################################################################
'''
# ==================================      ATENÇÃO      ==========================================
# Para utilização desta aplicação é necessário obter as bibliotecas abaixo:
# sklearn - Disponível em <https://scikit-learn.org/stable/index.html>
# nltk - Disponível em <https://www.nltk.org/>
# pandas - Disponível em <https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html>
# numpy - Disponível	em <https://numpy.org/install/>
# matplotlib - Disponível	em <https://matplotlib.org/3.3.3/users/installing.html>
# time - Disponível em <https://pypi.org/project/times/>
# pickle - Disponível em <https://pypi.org/project/pickle5/>
# wordcloud  - Disponível em <https://pypi.org/project/wordcloud/>
# pymysql - Disponível em <https://pypi.org/project/PyMySQL/>
# tweepy - Disponível em <http://docs.tweepy.org/en/latest/install.html>
# ================================================================================================
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from matplotlib import pyplot as plt
from pickle import dump, load
import numpy as np
from Manipulador_arquivos import Arquivo
from interface import interface_terminal as terminal

class TF_IDF():
    def __init__(self):
        self.data = []
        self.arq = Arquivo()
    
    def Gravar_PKL(self, arquivo, nome_arquivo):
        output = open(nome_arquivo, 'wb')
        dump(arquivo, output, -1)
        output.close()
    
    def Gerar_Dados(self, lista_tweets, dados=False):
        vectorizer = TfidfVectorizer()
        V = vectorizer.fit_transform(lista_tweets)

        row_label = ['Tweet %i'% i for i in range(V.shape[0])]
        col_label = vectorizer.get_feature_names()
        self.arq.Gravar_Arquivo(col_label, 'arquivos/data/tf-idf/feature_names.txt')

        aux = []
        aux2 = []
        [aux2.append(0.0) for i in range(len(col_label))]
        for item in range(len(row_label)):
            aux.append(aux2.copy())

        p = 0
        i = 0
        for indice in range(len(V.indices)):
            if indice < V.indptr[i+1]:
                aux[p][V.indices[indice]] = V.data[indice]
            else:
                p += 1
                i += 1
                aux[p][V.indices[indice]] = V.data[indice]
        self.data = aux.copy()
        self.Gravar_PKL(self.data,'arquivos/data/tf-idf/vetor_tfidf.pkl')

        print('Imprimir Tabela?[S/N] ', end='')
        opcao = str(input()).upper()

        if opcao == 'S':
            print('Informe os dados necessários:\nQuantidade de Linhas: ', end='')
            row = int(input())
            print('Quantidade de Colunas: ', end='')
            col = int(input())          
            self.Gerar_tabela(row,5,col,row_label,col_label,self.data)
        else:
            return False

        
    def Gerar_tabela(self,tam_inicio, tam_final, col_tam, row_label, col_label, lista):
            if col_tam > len(col_label):
                col_tam = len(col_label)
            if len(lista) > tam_inicio + tam_final:
                linha1 = 'Tweet\t'
                for ind in range(col_tam):
                    linha1 += '{:<8} '.format(col_label[ind])
                if col_tam < len(col_label):
                    linha1 += '{:<8} '.format('...')
                print(linha1)
                for i in range(tam_inicio):
                    linha = '%s '%row_label[i]
                    for k in range(col_tam):
                        if lista[i][k] == 0.0:
                            linha += '{:<8} '.format('-')
                        else:
                            linha += '{:<8,.5f} '.format(lista[i][k])
                    if col_tam < len(col_label):
                        linha += '{:<8} '.format('...')
                    print(linha)
                linha_intervalo = '{:<8} '.format('...')
              
                linha_intervalo = linha_intervalo*(col_tam+2)
                print(linha_intervalo)
                for i in range(-1,tam_final*-1,-1):
                    linha = '%s '%row_label[i]
                    for k in range(col_tam):
                        if lista[i][k] == 0.0:
                            linha += '{:<8} '.format('-')
                        else:
                            linha += '{:<8,.5f} '.format(lista[i][k])
                    if col_tam < len(col_label):
                        linha += '{:<8} '.format('...')
                    print(linha)
            else:
                linha1 = 'Tweet\t'
                for ind in range(col_tam):
                    linha1 += '{:<8} '.format(col_label[ind])
                if col_tam < len(col_label):
                        linha1 += '{:<8} '.format('...')
                print(linha1)
                for i in range(len(lista)):
                    linha = '%s '%row_label[i]
                    for k in range(col_tam):
                        if lista[i][k] == 0.0:
                            linha += '{:<8} '.format('-')
                        else:
                            linha += '{:<8,.5f} '.format(lista[i][k])
                    if col_tam < len(col_label):
                        linha += '{:<8} '.format('...')
                    print(linha)

    def Gerar_Grafico(self, data):

        plt.style.use(plt.style.available[-1])
        plt.rcParams['figure.figsize'] = (11,7)

        fig, axs = plt.subplots(2, 2, figsize=(5, 5))
        axs[0, 0].hist(data[0])
        axs[1, 0].scatter(data[0], data[1], data[2], data[3])
        axs[0, 1].plot(data[0], data[1], data[2], data[3])
        axs[1, 1].bar(data[0], data[1], data[2], data[3])
        plt.title('SEU TÍTULO LINDO')
        plt.xlabel('NOME DO EIXO X')
        plt.ylabel('NOME DO EIXO Y')
        
        ax.grid(True)
        fig.tight_layout()
        plt.show()
        nome_grafico = 'grafico_teste_01'
        nome_arquivo = 'arquivos/data/tf-idf/graficos/' + nome_grafico + '.png'
