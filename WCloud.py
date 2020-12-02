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
import pandas as pd
import nltk
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


class WCloud():
    
    def Build_Nuvem_Palavras(self, lista_tweets):
        all_tweets = " ".join(t for t in lista_tweets)

        # carrega stopwords
        stopword = set(nltk.corpus.stopwords.words('portuguese'))

        # set stopwords
        stopword.update(["da", "meu", "em", "você", "de", "ao", "os", "voce", "voces", "vcs", 'vc','voce', 'todos', 'cara', 'onde', 'b', 'fala', 'inteira', 'so', 'sabado', 'caiu', 'domingo','mim', 'ter', 'amg', 'ja', 'toda', 'hoje', 'conta', 'dar', 'sempre', 'ai','h', 'menos','via', 'at', 'ontem', 'assim', 'modo', 'noite', 'olha', 'tarde', 'vou', 'vai', 'to', 'tao', 'tava', 'ta', 'tamo', 'tanta', 'tanto', 'q', 'sei', 'ser', 'pra', 'pq', 'porque', 'quanto', 'ne', 'muitos', 'muitas', 'muito', 'muita', 'nao', 'nada', 'n', 'mesmo', 'mesma', 'live', 'fazer', 'fica', 'ficar', 'ficava', 'fiz', 'enquanto', 'diria', 'diriam', 'dessa', 'desse', 'desses', 'dessas', 'desde', 'cmg', 'acha', 'acho'])

        # wordcloud
        wordcloud = WordCloud(stopwords=stopword, 
                                background_color='white', width=1600, 
                                height=800).generate(all_tweets)
        # cria arquivo png
        fig, ax = plt.subplots(figsize=(16,8))            

        ax.imshow(wordcloud, interpolation='bilinear')       

        ax.set_axis_off()

        plt.imshow(wordcloud)                 

        wordcloud.to_file('arquivos/data/wordcloud/wordcloud_tweet.png')
