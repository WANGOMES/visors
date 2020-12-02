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
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from nltk.corpus import stopwords
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import os
from pickle import dump, load
import json
from interface import interface_terminal as terminal
from Manipulador_arquivos import Arquivo
import programa_auxiliar as pa

class Latent_Semantic_Analysis:
    def __init__(self):
        self.arq = Arquivo()
        self.feature_tweet = {}
        self.termos_especiais = {}
        self.arquivo_controle = {}
        self.matriz_termos = self.Carregar_Matriz('matriz_termos')
        self.matriz_topicos = self.Carregar_Matriz('matriz_topicos')
        self.ids_tweets_feature_topicos = self.arq.Carregar_Arquivo('arquivos/data/lsa/_ids_tweets_feature_topicos.txt')
        self.feature_topicos = self.Carregar_feature_topicos()
        self.last_id_tweet = 0
        self.TRUNCADO = 100
        # CARREGAR TWEETS
        self.body = self.Carregar_PKL('arquivos/data/bow/lista_tweets_limpos.pkl')[609:]
        self._LSA_()

    def Carregar_feature_topicos(self):
        try:
            with open( 'arquivos/data/lsa/feature_topicos.json', 'r', encoding='utf8') as json_file:
                dados = json.load(json_file)
                return dados
        except Exception as identifier:
            terminal.Mensagem('Erro [%s]: Não foi possível carregar o arquivo.'%identifier, 'e')
 
    def Carregar_PKL(self, nome_arquivo):
        try:
            Input = open(nome_arquivo, 'rb')
            dados = load(Input)
            Input.close()
            return dados
        except Exception as identifier:
            terminal.Mensagem('Erro [%s]: Não foi possível carregar o arquivo.'%identifier, 'e')

    def Gravar_PKL(self, arquivo, nome_arquivo):
        output = open(nome_arquivo, 'wb')
        dump(arquivo, output, -1)
        output.close()

    def carregar_arq_controle(self):
        try:
            with open('arquivos/data/lsa/arq_controle_lsa.json', 'r', encoding='utf8') as json_file:
                self.arquivo_controle = json.load(json_file)
            terminal.Mensagem('arquivo_controle_lsa carregado com sucesso!', 'ok')
        except Exception as identifier:
            terminal.Mensagem('Erro %s ao carregar o arquivo.'%(identifier), 'e')
        
    def carregar_feature_tweet(self):
        self.carregar_arq_controle()
        if self.arquivo_controle['has_feature_tweet']:
            with open( 'arquivos/data/lsa/feature_tweet.json' , 'r', encoding='utf8') as json_file:
                self.feature_tweet = json.load(json_file)
                terminal.Mensagem('feature_tweet carregado com sucesso!', 'ok')
    
    def Carregar_Matriz(self, nome_matriz='matriz_termos ou matriz_topicos'):
        nome = nome_matriz.lower()
        if nome == 'matriz_termos' or nome == None:
            nome_arquivo = 'arquivos/data/lsa/matriz_termos.pkl'
        elif nome == 'matriz_topicos':
            nome_arquivo = 'arquivos/data/lsa/matriz_topicos.pkl'
        try:
            matriz_T = self.Carregar_PKL(nome_arquivo)
            return matriz_T
        except Exception as identifier:
            terminal.Mensagem('Erro [%s]: Não foi possível carregar o arquivo \'%s\'.'%(identifier, nome_arquivo), 'e')

    def gravar_feature_tweet(self, tipo_gravacao='w'):
        with open('arquivos/data/lsa/feature_tweet.json', tipo_gravacao, encoding='utf-8') as json_file:
            json.dump(self.feature_tweet, json_file, indent=4, ensure_ascii=False)

    def Atualiza_arquivo_controle(self, key, value):
        self.arquivo_controle.update({key: value})
        with open('arquivos/data/lsa/arq_controle_lsa.json', 'w') as json_file:
            json.dump(self.arquivo_controle, json_file, indent=4, ensure_ascii=False)
        
    def _LSA_(self):
        inicio = time.time()
        terminal.Mensagem('Iniciando em Análise Semântica Latente', 'd')
        print('0 - Análise Semântica Latente Completa\n1 - Cálculo de Relevância dos tweets\n2 - Seleção de tweets com Maior Relevância\n\t> Informe o que deseja fazer: ',end='')
        _tipo_ = str(input())
        if _tipo_ == '0':
            resposta = 'S'
            self.carregar_arq_controle()
            if self.arquivo_controle['atualizacao_data'] != None:
                terminal.Mensagem('Arquivos Atualizados em %s às %s. Deseja atualizar a LSA?[S/N]' %(self.arquivo_controle['atualizacao_data'], self.arquivo_controle['atualizacao_hora']),'w')
                resposta = str(input()).upper()

            if resposta == 'S':
                # DEFINIR STOPWORDS
                stw = []
                stopword = stopwords.words('portuguese')
                outras_palavras = self.arq.Carregar_Arquivo_UTF8('arquivos/data/lsa/limpeza_feature_names.txt')
                [stw.append(s) for s in stopword]
                [stw.append(s) for s in outras_palavras]

                # CARREGAR LISTA DE TERMOS REFERENTES A VULNERABILIDADE E RISCO
                with open('arquivos/data/lsa/termos_especiais.json', 'r', encoding='utf8') as json_file:
                    self.termos_especiais = json.load(json_file)

                pa.Atualiza_Dict_Termos_especiais(True)

                # VETOR TFIDF / BOW
                vetor = TfidfVectorizer(min_df=1,stop_words=stw)
                bag_of_words = vetor.fit_transform(self.body)
                print(bag_of_words.shape)

                
                LISTA_TRUNCADO = [x for x in range(self.TRUNCADO)]

                # DEFINIR COLUNAS E TRUNCAR O VETOR TFIDF / BOW ==> LSA - ANALISE SEMANTICA LATENTE
                svd = TruncatedSVD(n_components=self.TRUNCADO) #Truncar para X colunas
                lsa = svd.fit_transform(bag_of_words)

                def __matriz_topicos__():
                    topicos = pd.DataFrame(lsa, columns = LISTA_TRUNCADO)
                    topicos['body'] = self.body
                    print(topicos[['body', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 
                                    17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 
                                    34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 
                                    51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 
                                    68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 
                                    85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99]])
                    self.Gravar_PKL(topicos, 'arquivos/data/lsa/matriz_topicos.pkl')
                    self.Atualiza_arquivo_controle('has_matriz_topicos', True)

                # DEFINIÇÃO DOS TOPICOS
                if self.arquivo_controle['has_matriz_topicos']:
                    terminal.Mensagem('Arquivos Atualizados em %s às %s. Deseja atualizar a Matriz de Tópicos?[S/N]' %(self.arquivo_controle['atualizacao_data'], self.arquivo_controle['atualizacao_hora']),'w')
                    resp = str(input()).upper()
                    if resp == 'S':
                        __matriz_topicos__()
                    else:
                        topicos = self.matriz_topicos
                else:
                    __matriz_topicos__()
            
                # DICIONÁRIO DE PALAVRAS - PRODUTO DA LSA
                dicionario = vetor.get_feature_names()
                print('Imprimir dicionário? [S/N] ', end='') 
                if input(str()).upper() == 'S':
                    print(dicionario)
                    print()

                # MATRIZ DE TERMOS - PRODUTO DA LSA
                if not self.arquivo_controle['has_matriz_termos']:
                    matriz = pd.DataFrame(svd.components_, 
                                            index=[LISTA_TRUNCADO],
                                            columns=dicionario).T
                    self.Gravar_PKL(matriz, 'arquivos/data/lsa/matriz_termos.pkl')
                    self.Atualiza_arquivo_controle('has_matriz_termos', True)
                
                print('Imprimir matriz_termos? [S/N] ', end='') 
                if input(str()).upper() == 'S':
                    print(self.Carregar_Matriz('matriz_termos'))
                    print()
                print('Imprimir matriz_topicos? [S/N] ', end='') 
                if input(str()).upper() == 'S':
                    print(self.Carregar_Matriz('matriz_topicos'))
                    print()

                self.last_id_tweet = self.arquivo_controle['last_id_tweet']

                # VETOR AUXILIAR PARA TOPICOS DOS TERMOS
                aux_topic = []
                maior, pos, aux = -1000.0, 0, 0
                for item in self.matriz_termos.values:
                    for j in item:
                        if j > maior:
                            maior = j
                            aux = pos #aux = topico
                        pos += 1
                    aux_topic.append([aux, maior])
                    pos, aux, maior = 0, 0, -1000.0
                    
                def Identificar_Topico(termo):
                    term = termo.lower()
                    achou = False
                    pos = -1
                    for item in dicionario:
                        pos += 1
                        if term == item:
                            achou = True
                            break
                    if achou:
                        return aux_topic[pos]
                    else:
                        return -1

                def Identificar_Topico_Tweet(id_tweet):
                    maior, pos, _top = -1000.0, 0, 0
                    res = []
                    for item in self.matriz_topicos.values[id_tweet]:
                        if type(item) != str:
                            if item > maior:
                                maior = item # média das freq
                                _top = pos #aux = topico
                            pos += 1
                    res.append(_top)
                    res.append(maior)
                    return res

                def Verifica_Dicionario(tweet):
                    count = 0
                    tweet = tweet.split()
                    for tw in tweet:
                        for item in dicionario:
                            if tw == item:
                                count += 1
                    return count

                def Verifica_Termos_Especiais_(tweet):
                    import re
                    caract = [r'\b\"', r'\"\b', r'\b\-', r'\b\'', r'\'\b', r'\“', r'\”', r'\.', r'\.\.\.', 
                            r'\,', r'\?', r'\!', r'\(', r'\)', r'\{', r'\}',r'\[',r'\]', r'\+', r'\*', r'\B\%'
                            r'\b\"+', r'\B\"', r'\"\B', r'\%', r'\\', r'\/', r'\|', r'\<', r'\>', r'\=', 
                            r'\B\-', r'\b\‘', r'\B\‘', r'\b\`', r'\B\`', r'\b\ñ', r'\B\ñ', r'\b\º', r'\B\º', 
                            r'\b\ª', r'\B\ª', r'\b\_', r'\B\_', r'\b\;', r'\B\;', r'\b\^', r'\~', r'\b\è', 
                            r'\_', r'\–', r'\•', r'\#', r'\b\—', r'\B\—', r'\—', r'\°', r'\b\°', r'\B\°',
                            r'\'', r'\B\'', r'\«', r'\b\«', r'\B\«', r'\&', r'\b\&', r'\B\&', r'\¬',
                            r'\b\¬', r'\B\¬', r'\¨', r'\b\¨', r'\B\¨', r'\¢', r'\b\¢', r'\B\¢', r'\£',
                            r'\b\£', r'\B\£' , r'\³', r'\b\³', r'\B\³', r'\³\b', r'\³\B', r'\²', r'\b\²', 
                            r'\B\²', r'\²\b', r'\²\B', r'\¹', r'\b\¹', r'\B\¹', r'\¹\b', r'\¹\B', r'\§', 
                            r'\b\§', r'\B\§', r'\b\·', r'\B\·', r'\·', r'\^', r'\B\^', r'\ö', r'\b\ö', 
                            r'\B\ö', r'\»', r'\b\»', r'\B\»', r'\@', r'\b\@', r'\B\@',  r'\€', r'\b\€', 
                            r'\B\€', r'\÷', r'\b\÷', r'\B\÷',r'\å', r'\b\å', r'\B\å', r'\×', r'\b\×', 
                            r'\B\×', r'\¡', r'\b\¡', r'\B\¡',  r'\¿', r'\b\¿', r'\B\¿', r'\´', r'\b\´',
                            r'\B\´', r'\$', r'\b\$', r'\B\$', r'\¥', r'\b\¥', r'\B\¥', r'\¯', r'\b\¯', 
                            r'\B\¯']
                    
                    espaco2 = re.compile(r'\b\s+')
                    for item in caract:
                            e = re.compile(item)
                            tweet = re.sub(e, ' ', tweet)
                    tweet = re.sub(espaco2, ' ', tweet)
                    
                    count = 0
                    tweet = tweet.split()
                    for word in tweet:
                        inicial = word[0]
                        if self.termos_especiais[inicial] != None:
                            for item in self.termos_especiais[inicial]:
                                if word == item:
                                    count += 1
                    return count

                def feature_tweet_(lista, id_inicial):
                    try:
                        self.carregar_feature_tweet()
                    except Exception as identifier:
                        terminal.Mensagem('Erro %s Não foi possível acessar o arquivo.'%(identifier), 'e')
                    try:
                        contador = 0
                        pos = id_inicial -1
                        for tweet in lista:
                            contador += 1
                            pos += 1
                            _palavras = len(tweet.split())
                            _id = pos
                            _term = Verifica_Termos_Especiais_(tweet)
                            _aux = Identificar_Topico_Tweet(_id)
                            _topico = _aux[0]
                            _word_dicionary = Verifica_Dicionario(tweet)
                            _freq = _aux[1]
                            self.feature_tweet.update({_id:{'words': _palavras, 'special_terms': _term, 'words_dicionary': _word_dicionary, 'topic': _topico, 'score': _freq}})  
                            terminal.printProgressBar(contador,len(lista),length=50)
                        
                        self.Atualiza_arquivo_controle('has_lsa_tweet', True)
                        self.gravar_feature_tweet('w')
                        self.Atualiza_arquivo_controle('has_feature_tweet', True)
                    except Exception as identifier:
                        fim = time.time()
                        duracao = fim - inicio
                        terminal.Mensagem('Erro %s identificado na posição %i.'%(identifier, pos), 'e')
                        terminal.Mensagem('Programa finalizado!\tDuração: %.3f seg'%(duracao),'ok')

                def Gerar_Grafico():
                    topicos = pd.DataFrame(matriz, 
                                            index=['Tweet'],
                                            columns=dicionario).T

                    print(topicos)
                    fig, ax = plt.subplots()
                    top_1 = matriz[0].values
                    top_2 = matriz[1].values

                    ax.scatter(top_1, top_2, alpha=0.3)

                    ax.set_xlabel('Primeiro Topico')
                    ax.set_ylabel('Segundo Topico')
                    ax.axvline(linewidth=0.5)
                    ax.axhline(linewidth=0.5)
                    ax.legend()

                    plt.show()
                
                # Produz Recurso de Tweets
                tamanho = self.last_id_tweet + 15000
                if tamanho > len(self.body):
                    tamanho = len(self.body)

                feature_tweet_(self.body[self.last_id_tweet: tamanho], self.last_id_tweet)
                self.Atualiza_arquivo_controle('last_id_tweet', tamanho)

                # Calcula Relevancia dos Tweets
                if self.arquivo_controle['has_lsa_tweet']:
                    self.Calcular_Relevancia_Tweet()
                else:
                    terminal.Mensagem('lsa_tweet não executado!', 'e')
                # Seleciona Tweets com maior Relevancia
                if self.arquivo_controle['has_calculo_relevancia_tweet']:
                    self.Selecionar_Tweets_Relevancia('positive',0.5)
                else:
                    terminal.Mensagem('calculo_relevancia_tweet não executado!', 'e')
                
                fim = time.time()
                data = time.strftime("%d-%m-%Y", time.localtime(fim))
                hora = time.strftime("%H:%M:%S", time.localtime(fim))
                self.Atualiza_arquivo_controle('atualizacao_data', data)
                self.Atualiza_arquivo_controle('atualizacao_hora', hora)
                duracao = fim - inicio
                terminal.Mensagem('Programa finalizado!\tDuração: %.3f seg'%(duracao),'ok')

            else:
                terminal.Mensagem('Desconectando...','d')
                return False
        
        elif _tipo_ == '1':
            self.Calcular_Relevancia_Tweet()
        elif _tipo_ == '2':
            self.Selecionar_Tweets_Relevancia('positive',0.5)
        else:
            terminal.Mensagem('Desconectando...','d')
            return False
        
    def Calcular_Relevancia_Tweet(self):
        self.carregar_feature_tweet()
        # Atribuição de relevância POSITIVA
        for key in self.feature_tweet.keys():
            if self.feature_tweet[key]['special_terms'] > 0:
                term = (self.feature_tweet[key]['special_terms'])
                dc = (self.feature_tweet[key]['words_dicionary'])
                if dc != 0:
                    imp = (term / dc)
                else:
                    imp = -1
                if imp >= 0.50: # grau de importancia do tweet com o tema (>=50% POSITIVO, menor que 50% NEUTRO, não possui palavras que tenha a ver com o tema NEGATIVO)
                    self.feature_tweet[key].update({'relevance': 'POSITIVE'})
                else:
                    self.feature_tweet[key].update({'relevance': 'NEUTRO'})
            else:
                # Atribuição de relevância NEGATIVA
                self.feature_tweet[key].update({'relevance': 'NEGATIVE'})
        self.gravar_feature_tweet('w')
        self.Atualiza_arquivo_controle('has_calculo_relevancia_tweet', True)

    def Selecionar_Tweets_Relevancia(self, relevancia='POSITIVE', maior_score=0.0):
        self.carregar_feature_tweet()
        self.carregar_arq_controle()
        ''' PERGUNTAR SE DESEJA IMPRIMIR MATRIZ TERMOS E TOPICOS E DICIONARIO'''
        print('\tImprimir matriz_termos? [S/N] ', end='') 
        if input(str()).upper() == 'S':
            print(self.Carregar_Matriz('matriz_termos'))
            print()
        print('\tImprimir matriz_topicos? [S/N] ', end='') 
        if input(str()).upper() == 'S':
            print(self.Carregar_Matriz('matriz_topicos'))
            print()

        relevancia = relevancia.upper()
        encontrado = False
        status_relevancia = ['POSITIVE', 'NEGATIVE', 'NEUTRO']

        def __run__():
            score, posicao, termos, topico, palavras, dicio, importancia, tt = [], [], [], [], [], [], [], []
            for key in self.feature_tweet.keys():
                if self.feature_tweet[key]['relevance'] == relevancia and self.feature_tweet[key]['score'] >= maior_score:
                    term = self.feature_tweet[key]['special_terms']
                    dc = self.feature_tweet[key]['words_dicionary']
                    if dc != 0:
                        imp = (term / dc)
                    else:
                        imp = -1
                    score.append(self.feature_tweet[key]['score'])
                    posicao.append(key)
                    termos.append(term)
                    topico.append(self.feature_tweet[key]['topic'])
                    palavras.append(self.feature_tweet[key]['words'])
                    dicio.append(dc)
                    importancia.append(imp)

            print('\t> Tweets com Score maior que %.2f e com Relevancia \'%s\': %i / %i (%.2f)' %(maior_score, relevancia, len(posicao), len(self.feature_tweet), float(len(posicao)/len(self.feature_tweet)*100)) + '%')
            self.Atualiza_arquivo_controle('count_feature_topicos',len(posicao))

            print()
            for item in posicao: # Imprime os Tweets
                tt.append(self.body[int(item)])
            y = zip(posicao, topico, tt)
            
            topic_unique = [topico[0]]
            achou = False
            for t1 in topico:
                achou = False
                for t2 in topic_unique:
                    if t1 == t2:
                        achou = True
                if not achou:
                    topic_unique.append(t1)
            topic_unique.sort()

            topicos_dict, aux, p1 = {}, {}, 0
            for t0 in topic_unique:
                for t3 in topico:
                    if t3 == t0:
                        aux.update({posicao[p1]: self.feature_tweet[str(posicao[p1])]})
                        aux[posicao[p1]]['importancia'] = importancia[p1]
                        aux[posicao[p1]]['tweet'] = tt[p1]
                        topicos_dict.update({t3: aux.copy()})
                    p1 +=1
                aux.clear()
                p1=0

            if not self.arquivo_controle['has_feature_topicos']:
                with open('arquivos/data/lsa/feature_topicos.json', 'w', encoding='utf-8') as json_file:
                    json.dump(topicos_dict, json_file, indent=4, ensure_ascii=False)
                self.arq.Gravar_Arquivo(posicao,'arquivos/data/lsa/_ids_tweets_feature_topicos.txt')
            
            self.Atualiza_arquivo_controle('has_feature_topicos',True)

            print('\tImprimir feature_topicos? [S/N] ', end='')
            if input(str()).upper() == 'S':
                tam =0
                for t4 in topicos_dict.keys():
                    while tam < 10:
                        for t5 in topicos_dict[t4].keys():
                            print('id: {:<8} score: {:<8,.5f} terms: {:<2} topic: {:<2} words: {:<4} words_dicionary: {:<2} importancia: {:<2,.2f}'
                                    .format(t5, topicos_dict[t4][t5]['score'], topicos_dict[t4][t5]['special_terms'], topicos_dict[t4][t5]['topic'], 
                                    topicos_dict[t4][t5]['words'], topicos_dict[t4][t5]['words_dicionary'], topicos_dict[t4][t5]['importancia']))
                            tam +=1

                print('...\t\t...\t\t...\n')
                tam =0
                for t4 in topicos_dict.keys():
                    while tam < 10:
                        for t5 in topicos_dict[t4].keys():
                            print('id: {:<6} Topic: {:<2} Tweet: {:<80}'
                                    .format(t5, topicos_dict[t4][t5]['topic'], topicos_dict[t4][t5]['tweet']))
                            tam +=1
            print('\tImprimir relatorio_status_lsa_tweet? [S/N] ', end='')
            if input(str()).upper() == 'S':
                relt_topicos, tam_topic = [], 0
                for t_u in topic_unique:
                    tam_topic += len(topicos_dict[t_u])
                    relt_topicos.append([t_u, len(topicos_dict[t_u])])
                print('* * * RELATÓRIO DE STATUS LSA FEATURE * * * ')
                for item in range(0,len(relt_topicos),4):
                    if item <=len(relt_topicos)-4:
                        print('Topic: {:<2} Qtde: {:<4} Topic: {:<2} Qtde: {:<4} Topic: {:<2} Qtde: {:<4} Topic: {:<2} Qtde: {:<4}'
                                .format(relt_topicos[item][0], relt_topicos[item][1],
                                relt_topicos[item+1][0], relt_topicos[item+1][1],
                                relt_topicos[item+2][0], relt_topicos[item+2][1],
                                relt_topicos[item+3][0], relt_topicos[item+3][1]))
                    elif item == len(relt_topicos)-1:
                        print('Topic: {:<2} Qtde: {:<4}'.format(relt_topicos[item][0], relt_topicos[item][1]))
                    elif item == len(relt_topicos)-2:
                        print('Topic: {:<2} Qtde: {:<4} Topic: {:<2} Qtde: {:<4}'
                                .format(relt_topicos[item][0], relt_topicos[item][1],
                                relt_topicos[item+1][0], relt_topicos[item+1][1]))
                    else:
                        print('Topic: {:<2} Qtde: {:<4} Topic: {:<2} Qtde: {:<4} Topic: {:<2} Qtde: {:<4}'
                                .format(relt_topicos[item][0], relt_topicos[item][1],
                                relt_topicos[item+1][0], relt_topicos[item+1][1],
                                relt_topicos[item+2][0], relt_topicos[item+2][1]))
                print('\t > Total Tópicos: {:<2} Total Tweets: {:<4}'.format(len(topic_unique), tam_topic))
        
            print('\n\tRealizar Etiquetagem <Treinamento> da Base de Tweets? [S/N] ', end='')
            if input(str()).upper() == 'S':
                pos, fim = 1, False
                for i in topic_unique:
                    if i > self.arquivo_controle['topico_treinamento']:
                        print('\t> Treino da Base topic_num: \"%i\" [%i de %i tópicos]'%(i, pos, len(topic_unique)))
                        fim = self.Verifica_feature_topicos(i)
                        if fim:
                            return False
                    pos += 1
            print('\n\tImprimir Estimativa de Tweets com Vulnerabilidade TRUE? [S/N] ', end='')
            if input(str()).upper() == 'S':
                pa.Levantamento_Score_Vulnerabilidade()
            
            tweets_localizacao()

        def tweets_localizacao():
            dicts, _ids_tweets_localizacao, aux_ids = {}, [], []
            with open( 'arquivos/data/lsa/feature_topicos.json' , 'r', encoding='utf8') as json_file:
                dicts = json.load(json_file)

            for topico in dicts.keys():
                for _id in dicts[topico].keys():
                    if dicts[topico][_id]['vulnerabilidade'] == 1.0:
                        aux_ids.append(int(_id))
            aux_ids.sort()
            for item in aux_ids:
                _ids_tweets_localizacao.append(str(item))

            self.arq.Gravar_Arquivo(_ids_tweets_localizacao, 'arquivos/data/lsa/_ids_tweets_localizacao.txt')
            print('Arquivo _ids_tweets_localizacao.txt tamanho: %i'%len(_ids_tweets_localizacao))


        # __MAIN__
        for item in status_relevancia:
            if relevancia == item:
                encontrado = True
        if encontrado:
            __run__()
        else:
            terminal.Mensagem('Erro ao inserir o dado [RELEVANCE]: \'%s\'' % (relevancia), 'e')

    def Verifica_feature_topicos(self, _topic):
        _topic = str(_topic)
        _tweet, _id = [], []
        
        clear = lambda: os.system('cls')

        def _retorna_tweet_topico():
            for item in self.feature_topicos[_topic].keys():
                if self.feature_topicos[_topic][item]['vulnerabilidade'] == None:
                    _tweet.append(self.feature_topicos[_topic][item]['tweet'])
                    _id.append(item)
        
        def _atualiza_feature_topicos_( _id, _key, _value):
            self.feature_topicos[_topic][_id].update({_key: _value})
            with open('arquivos/data/lsa/feature_topicos.json', 'w', encoding='utf-8') as json_file:
                json.dump(self.feature_topicos, json_file, indent=4, ensure_ascii=False)
        
        def _aplica_regra_treino(identificador, tweet):
            print('\nTweet: %s'%tweet)
            print('O Tweet Apresenta Vulnerabilidade? [S/N] ', end='')
            chave = 'vulnerabilidade'
            if input(str()).upper() == 'S':
                valor = 1.0
            else:
                valor = 0.0
            _atualiza_feature_topicos_(identificador, chave, valor)
            clear()
        
        
        _retorna_tweet_topico()        
        treino = int(len(_tweet)*0.6) ## Treino 60% da Base ##
        tw = _tweet.copy()
        ident = _id.copy()
        pos = 0
        print('Deseja Continuar a Etiquetagem da Base? [S/N] ', end='')
        if input(str()).upper() == 'S':
            if len(tw) > 0:
                for item in tw:
                    print('%i de %i Tweets - tópico: \"%s\" Id: %s'%(pos+1, len(tw), _topic, ident[pos]))
                    _aplica_regra_treino(ident[pos], item)
                    pos += 1
                    self.Atualiza_arquivo_controle('topico_treinamento', int(_topic))
                pa.Atualiza_Recursos_Classificador()
            else:
                print('Etiquetagem atualizada! Não há mais tweets para etiquetar.\n')
        else:
            return True



