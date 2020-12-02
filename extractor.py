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
from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener
import pymysql
import threading
import time
from datetime import datetime
import json
from twitter_credenciais import User_password
from interface import interface_terminal as terminal

conn = pymysql.connect("localhost","root","", "tw")
c = conn.cursor()

class listener(StreamListener):
    def __init__(self, _futuro):
        self.futuro = _futuro
        self.contador = 0

    def on_data(self, data):
        all_data = json.loads(data)
        if((json.dumps(all_data).startswith('{"limit":')==False)):
            self.contador += 1
            id_tweet = all_data["id"]

            source = all_data["source"]

            user_id = all_data["user"]["id"]
            username = all_data["user"]["screen_name"]
            user_url = all_data["user"]["url"]
            user_description = all_data["user"]["description"]
            user_local = all_data["user"]["location"]
            
            date_tweet = all_data["created_at"]

            if(all_data["geo"] != None):
                geo = json.dumps(all_data["geo"])
            elif(all_data["geo"] == None):
                geo = all_data["geo"]

            if(all_data["coordinates"] != None):
                coordinates = json.dumps(all_data["coordinates"])
            elif(all_data["coordinates"] == None):
                coordinates = all_data["coordinates"]
            
            tweet = all_data["text"]

            if(all_data["place"] != None):
                place = json.dumps(all_data["place"])
            elif(all_data["place"] == None):
                place = all_data["place"]

            c.execute("INSERT INTO tweet_tb (id_tweet, source, user_id, username, user_url, user_description, user_local, date_tweet, geo, coordinates, tweet, place) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", 
                (id_tweet, source, user_id, username, user_url, user_description, user_local, date_tweet, geo, coordinates, tweet, place))

            conn.commit()

            print(username,tweet)
            if time.time() > self.futuro:
                terminal.Mensagem('TOTAL TWEETS: %s' % self.contador, 'w')
                return False
            else:
                return True
        elif(json.dumps(all_data).startswith('{"limit":')):
            print('\n'+'*' * 30 + ' Dict Json ' + '*' * 30 + '\n')

    def on_error(self, status):
        if status == 420:
            # Retorna Falso quando on_data exceder o limite da API
            print (status)
            terminal.Mensagem('TOTAL TWEETS: %s' % self.contador, 'w')
            return False
        print (status)
        terminal.Mensagem('TOTAL TWEETS: %s' % self.contador, 'w')

class Extractor():
    def __init__(self, tempo_segundos):
        terminal.Mensagem('Iniciando em Extrator','d')
        inicio = time.time()
        
        futuro = (inicio + tempo_segundos)
        t = threading.Timer(3.0, self.Run(futuro))
        t.setName('Thread-Extractor')
        t.start()
        if True:
            terminal.Mensagem('Cancelando a Thread....', 'w')
            t.cancel()
            fim = time.time()
            duracao = fim - inicio
            strfim = time.strftime("\nFim: %A, %d %b %Y %H:%M:%S +0000", time.localtime(fim))
            strinicio = time.strftime("\nInício: %A, %d %b %Y %H:%M:%S +0000", time.localtime(inicio))
            texto = '%s Cancelada!%s%s\nDuração: %s' % (str(t.getName()), strinicio, strfim, duracao)
            terminal.Mensagem(texto, 'ok')

    def Run(self, futuro):
        up = User_password()
        auth = OAuthHandler(up.CONSUMER_KEY(), up.CONSUMER_SECRET())
        auth.set_access_token(up.ACCESS_TOKEN(), up.ACCESS_TOKEN_SECRET())
        
        twitterStream = Stream(auth, listener(futuro))
        twitterStream.filter(follow=None,track=['a'],languages=['pt'])