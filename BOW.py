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
import numpy as np
from analyzer import AnaliseLexica, Tokenizacao
from interface import interface_terminal as terminal

class BagOfWords():
    def __init__(self):
        self.vocabulario = []
        self.al = AnaliseLexica()
        self.token = Tokenizacao()
        self.freq_vocabulario = {}

    def Construtor_Vocabulario(self, sentencas):
        lista = []
        sentencas = self.al.Remocao_caracteres_Tweets(sentencas)
        sentencas = self.al.Remocao_acentuacao_lista(sentencas)
        lista.append(sentencas)
        sentencas = self.al.Remocao_Stopword(sentencas)
        sentencas = self.al.Remocao_Pontuacao(sentencas)
    
        for sent in sentencas:
            # sent = self.al.Stemmers_lista(sent)
            for word in sent:
                if word not in self.vocabulario:
                    self.vocabulario.append(word)
                    
        self.vocabulario.sort()
        for voc in self.vocabulario:
            self.freq_vocabulario.update({voc: 0.0})
        
        return lista

    def Vetor(self, sentenca):
        words = self.token.Token(sentenca)
        vetor = np.zeros(len(self.vocabulario))
        for word in words:
            for i, w in enumerate(self.vocabulario):
                if word == w:
                    vetor[i] = 1.0
        return vetor
    
    def Verifica_Freq_Vocabulario(self, vetor):
        for i in range(len(vetor)):
            if vetor[i] > 0:
                key = self.freq_vocabulario[self.vocabulario[i]] + vetor[i]
                self.freq_vocabulario.update({self.vocabulario[i]: key})