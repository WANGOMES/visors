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
import pymysql
from Manipulador_arquivos import Arquivo
from interface import interface_terminal as terminal

class Conexao():
    conn = pymysql.connect("localhost","root","", "tw")
    c = conn.cursor()
    Arquivo_Carregado = []
    carregado = False
    
    # O método QUERY faz uma query para selecionar os termos nos tweets e retira os Retweets (RT)
    def query(self, keywords, query=''):
        q0 = "SELECT * FROM `tweet_tb` WHERE (tweet like '%{}%'"
        q1 = " OR (tweet like '%{}%')"
        q2=''
        q3 = ") AND NOT tweet like 'RT%'"
        if query == '':
            q4 = ''
        else:
            q4 = query
        k1 = keywords[0]
        i = 1
        q0 = q0.format(k1)
        while(i<len(keywords)):
            q2 += q1.format(keywords[i])
            i += 1
        _query = q0 + q2 + q3 + q4
        return _query
    
    def consulta_base(self, keywords, query='COMPLETA'):
        if query == 'COMPLETA':
            self.c.execute(self.query(keywords,''))
        else:
            self.c.execute(self.query(keywords,query))

        lista = []
        arq = Arquivo()

        count = 0
        while True:
            res = self.c.fetchall()
            tamanho = len(res)
            if not res:
                break
            for result in res:
                if (self.Verifica_Dados(str(result[0]),'arquivos/ids_selecionados.txt')):
                    lista.append(str(result[0]))
                    terminal.printProgressBar(count, tamanho,length=50)
                    self.Inserir_selecionados(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8], result[9], result[10], result[11], result[12], result[13])
                    count +=1
        
        arq.Gravar_Arquivo(lista, 'arquivos/ids_selecionados.txt')
        self.Fechar_Conexao()
        return count
       
    def Inserir_selecionados(self,id_table_tw, id_tweet, source, user_id, username, user_url, user_description, user_local, date_tweet, geo, coordinates, tweet, place, datetime_table_tw):
        self.c.execute("INSERT INTO selecionados_notRT_tb (id_table_tw, id_tweet, source, user_id, username, user_url, user_description, user_local, date_tweet, geo, coordinates, tweet, place, datetime_table_tw) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", 
                (id_table_tw, id_tweet, source, user_id, username, user_url, user_description, user_local, date_tweet, geo, coordinates, tweet, place, datetime_table_tw))
        self.conn.commit()
    
    def Fechar_Conexao(self):
        self.conn.close()

    def Verifica_Dados(self, id_table, nome_arquivo):
        if (len(self.Arquivo_Carregado) == 0 and not self.carregado):
            arq = Arquivo()
            lista = arq.Carregar_Arquivo(nome_arquivo)
            self.Arquivo_Carregado = lista
            self.carregado = True
        else:
            lista = self.Arquivo_Carregado
        count = 0
        for item in lista:
            item = item.rstrip()
            if (item == id_table):
                count += 1
        
        if count == 0:
            return True
        else:
            return False
      
class Selector(): 
    def __init__(self):
        self.arq = Arquivo()
        self.consulta = Conexao()
        self.Run()

    def Run(self):
        terminal.Mensagem('Iniciando em Seletor', 'd')
        print('Informe o tipo de Consulta: C - COMPLETA | A - ATUALIZAÇÃO: \t', end='')
        tipo = str(input())
        print('Informe a Data INICIAL para a Consulta [YYYY-MM-DD]: \t', end='')
        data_inicio = str(input())
        print('Informe a Data FINAL para a Consulta [YYYY-MM-DD]: \t', end='')
        data_final = str(input())
        self.select(tipo, data_inicio, data_final)

    # RETORNA A BASE DE TWEETS SELECIONADOS, CONFORME AS PALAVRAS ESCOLHIDAS
    def select(self, tipo, data_inicio, data_final):
        '''
        parametro tipo de consulta: informe C - COMPLETA | A - ATUALIZAÇÃO
        '''
        keywords = self.arq.Carregar_Arquivo_UTF8('arquivos/stem_termos.txt') #palavras chave vulnerabilidade e risco sociais
        lista_aux = self.arq.Carregar_Arquivo('arquivos/ids_selecionados.txt')
        id_final = lista_aux[-1]
        if(len(lista_aux)==0):
            tipo = 'C'
        if tipo.upper() == 'C':
            quant_tweet = self.consulta.consulta_base(keywords, 'COMPLETA')
        else:
            quant_tweet = self.consulta.consulta_base(keywords, query=" AND (id > %s) AND (datetime BETWEEN '%s 00:00:00.000000' AND '%s 23:59:59.999999')" % (id_final, data_inicio, data_final))
        terminal.Mensagem('%i Tweets Selecionados com Sucesso!' % quant_tweet, 'ok')