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
from nltk.chunk import *
from nltk.chunk.util import *
from nltk.chunk.regexp import *
from nltk import Tree
from nltk.probability import FreqDist
from nltk.classify import NaiveBayesClassifier, PositiveNaiveBayesClassifier
from nltk.metrics import ConfusionMatrix
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics, svm
from sklearn.metrics import classification_report, plot_confusion_matrix
from sklearn.model_selection import StratifiedShuffleSplit
import time
import json
import pymysql
import pprint
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from analyzer import *
from BOW import BagOfWords
from tfidf import TF_IDF
from WCloud import WCloud
from Manipulador_arquivos import Arquivo
from interface import interface_terminal as terminal
import programa_auxiliar as pa

class Arvore():
    def __init__(self, Lista_arvores):
        self._lista_tree = Lista_arvores

    def Buscar_Elemento(self, arvore, etiqueta):
        '''
        Retorna um lista de Árvores contendo os nós selecionados conforme a etiqueta.

        :param arvore: Obj Arvore
        :param etiqueta: Etiqueta (label) que um determinado nó da Árvore
        '''
        t = arvore
        etiqueta = etiqueta.upper()
        count = 0
        lista =[]
        for i in t.subtrees(lambda t: t.label()==etiqueta):
            count +=1
            print('%s: %s' % (count, i.__repr__()))
            lista.append(i.__repr__())
        return lista

    def Buscar_Arvore(self, etiqueta):
        '''
        Retorna um lista de Árvores contendo os nós selecionados conforme a etiqueta do Obj Arvore criado.

        :param etiqueta: Etiqueta (label) que um determinado nó da Árvore
        '''
        # t[1] Retorna o segundo filho[nó] da arvore na (posição 1.)
        # t.height() Retorna altura da arvore
        # len(t) REtorna o numero de filhos.
        # t.leaves() retorna folhas
        # t.label() REtorna o rotulos da arvore.
        # t.set_label('label')
        # t.flatten() retorna versão simples da arvore.
        # t.treepositions() Retorna posição dos nos e folhas na arvore.
        # t.pos() Retorna lista de tuplas ('dog', 'N')
        # t.leaf_treeposition(index) retorna a posição de uma folha na arvore.
        # t.draw() retorna arvore desenhada em outro display.
        lista = [self.Buscar_Elemento(t, etiqueta) for t in self._lista_tree]
        return lista
    
    def Buscar_Arvore_Por_Altura(self, altura):
        '''
        Retorna um lista de Árvores contendo os nós selecionados conforme a ALTURA no Obj Arvore.

        :param altura: Altura de uma Árvore
        '''
        arvore = [arvore.append(t) for t in self._lista_tree]
        count = 0
        lista =[]
        for i in t.subtrees(lambda t: t.height()==altura):
            count +=1
            print('%s: %s' % (count, i.__repr__()))
            lista.append(i.__repr__())
        if len(lista) == 0:
            print('Não há árvores na Lista com a Altura selecionada!')
        return lista
    
    def Imprime_Arvore_Desenho(self, arvore):
        '''
        Retorna um desenho de uma Árvores em nova janela.

        :param arvore: Obj Arvore
        '''
        return arvore.draw()


    def Imprime_SubArvores_filhos(self, uma_arvore):
        t = uma_arvore
        for i in t.subtrees(lambda t: t.height()>1):
            print(i.__repr__())

    def Imprime_Arvore(self, uma_arvore, formato):
        '''
        Imprime a Árvore formata no terminal e retorna uma string com o formato conforme parâmetro.

        :param uma_arvore: Obj Arvore
        :param formato: string opções { P - output de Produção | L - output LaTeX | S - String format}
        '''
        print(self.__String_Arvore(uma_arvore, formato))

    def Imprime_Arvore_Completa(self, formato):
        '''
        Retorna as Árvores impressas como string no formato passado por parâmetro.

        :param uma_arvore: Obj Arvore
        :param formato: string opções { P - output de Produção | L - output LaTeX | S - String format}
        '''
        [self.Imprime_Arvore(tree, formato) for tree in self._lista_tree]

    def __String_Arvore(self, uma_arvore, formato):
        '''
        Retorna uma string com o formato conforme parâmetro.

        :param uma_arvore: Obj Arvore
        :param formato: string opções { P - output de Produção | L - output LaTeX | S - String format}
        '''
        t = uma_arvore
        formato = formato.lower()

        if formato == 'p':
            return t.productions()
        elif formato == 'l':
            return t.pformat_latex_qtree()
        elif formato == 's':
            return t.pformat()
        else:
            return t.pformat()

class Avaliacao_classificacao:
    def __init__(self):
        self.Seletor_Classificador()

    def Seletor_Classificador(self):
        terminal.Mensagem('Iniciando em Avaliação > Classificação', 'd')
        # Variáveis
        base_tweet, vulnerabilidade, twt, loop = [], [], [], 0
        X_train, X_test, y_train, y_test = [], [], [], []
        X_treino_Holdout, X_teste_Holdout, y_treino_Holdout, y_teste_Holdout = [], [], [], []

        # Métodos
        def Seleciona_Base_tweets():
            dicts,teste = {}, {}
            with open( 'arquivos/data/lsa/feature_topicos.json' , 'r', encoding='utf8') as json_file:
                dicts = json.load(json_file)

            for topico in dicts.keys():
                for _id in dicts[topico].keys():
                    if dicts[topico][_id]['vulnerabilidade'] != None:
                        teste.update(dicts[topico])
            
            print('Tamanho  da base: %i'%len(teste))
            words, terms, wdictionary, topic, score, importancia = 0, 0, 0, 0, 0, 0

            for _id in teste.keys():
                if teste[_id]['vulnerabilidade'] != None:
                    words = (teste[_id]['words'])
                    terms = (teste[_id]['special_terms'])
                    wdictionary = (teste[_id]['words_dicionary'])
                    topic = (teste[_id]['topic'])
                    score = (teste[_id]['score'])
                    importancia = (teste[_id]['importancia'])
                    vulnerabilidade.append(teste[_id]['vulnerabilidade'])
                    twt.append([_id, teste[_id]['tweet']])
                    base_tweet.append([words, terms, wdictionary, topic, score, importancia])
                    # base_tweet.append([words, topic, score, wdictionary]) # teste 1

        Seleciona_Base_tweets()
        
        ''' Selecao_Amostragem_Holdout(80 - 20) '''
        parte = int(len(base_tweet)*0.8)
        x1, x2, y1, y2 = [], [], [], []
        [x1.append(item) for item in base_tweet[:parte]]
        [x2.append(item) for item in base_tweet[parte:]]
        [y1.append(item) for item in vulnerabilidade[:parte]]
        [y2.append(item) for item in vulnerabilidade[parte:]]
        
        X_treino_Holdout = np.array(x1)
        X_teste_Holdout = np.array(x2)
        y_treino_Holdout = np.array(y1)
        y_teste_Holdout = np.array(y2)
        
        ''' Selecao_Amostragem_Stratified_Cross_Validation (80 - 20)'''
        test_size=0.2
        train_size = 1.0 - test_size
        sss = StratifiedShuffleSplit(test_size=test_size, n_splits=12, random_state=0)
        loop = sss.get_n_splits(X_treino_Holdout, y_treino_Holdout)

        print('Parametros Stratified Cross Validation: ', sss)

        for train_index, test_index in sss.split(X_treino_Holdout, y_treino_Holdout):
            X_train.append(X_treino_Holdout[train_index])
            X_test.append(X_treino_Holdout[test_index])
            y_train.append(y_treino_Holdout[train_index])
            y_test.append(y_treino_Holdout[test_index])

        ''' NaiveBayes '''
        clf = GaussianNB()
        predicted_CV, predicted = [], []
        for item in range(loop):
            clf.fit(X_train[item], y_train[item])
            predicted_CV.append(clf.predict(X_test[item]))
        
        print('>>> Resultado Teste 1 (Stratified Cross-Validation):')
        target_names = [ 'Não', 'Sim']
        print(classification_report(y_test[0], predicted_CV[0], target_names=target_names))
        # print(predicted_CV)

        #teste
        predicted = clf.predict(X_teste_Holdout)
        print('>>> Resultados Teste 2 (HOLDOUT):')
        target_names = ['Não', 'Sim']
        print(classification_report(y_teste_Holdout, predicted, target_names=target_names))

        met = ['HOLDOUT', 'Stratified Cross-Validation']
        tam = [[len(X_treino_Holdout), len(X_teste_Holdout)], [len(X_treino_Holdout)*train_size, len(X_treino_Holdout)*test_size]]
        pa.Metodos_Amostragem(met,tam)

        ''' Impressão de Resultados '''
        count = parte
        contador = 0
        impressao = 10
        print('\n * * * PREDIÇÃO VULNERABILIDADE EM TWEETS * * * ')
        for item in predicted:
            if (contador < impressao) or (contador >= len(vulnerabilidade[parte:])-impressao):
                if vulnerabilidade[count] == item:
                    acerto = 'OK'
                else:
                    acerto = 'ERRO'
                print('id: {:<5} tweet: {:<30}... Vulnerabilidade: {:<2} - Class: {:<2} - {:<5}'.format(twt[count][0], twt[count][1][0:30], vulnerabilidade[count], item, acerto))
            elif contador == impressao:
                print('    {:<5}        {:<30}                     {:<2}          {:<2}   {:<5}'.format('...', '...', '...', '...', '...'))
            count += 1
            contador += 1
        print(' > > > Tamanho teste: ', len(vulnerabilidade[parte:]))
        
        print('\n\tMATRIZ DE PREDIÇÃO VULNERABILIDADE EM TWEETS ')
        print(predicted)
        print(' > > > Tamanho teste: ', len(predicted))

        print('\n --- MÉTRICAS ---')
        acuracia = metrics.accuracy_score(vulnerabilidade[parte:], predicted)
        precisao = metrics.precision_score(vulnerabilidade[parte:], predicted)
        recall = metrics.recall_score(vulnerabilidade[parte:], predicted)
        v_measure = metrics.v_measure_score(vulnerabilidade[parte:], predicted)
        f1 = metrics.f1_score(vulnerabilidade[parte:], predicted)
        print('acuracia:  {:<12.8f} precisao: {:<12.8f} recall: {:<12.8f}\nv_measure: {:<12.8f} f1_score: {:<12.8f}\n'.format(acuracia, precisao, recall, v_measure, f1))

        confusao = metrics.confusion_matrix(vulnerabilidade[parte:], predicted)
        print(confusao)
        ''' Plot Matriz de Confusão '''
        np.set_printoptions(precision=2)

        # Plot non-normalized confusion matrix
        titles_options = [("Matriz de Confusão", None),
                        ("Matriz de Confusão normalizada", 'true')]
        for title, normalize in titles_options:
            disp = plot_confusion_matrix(clf, X_teste_Holdout, y_teste_Holdout,
                                        display_labels=target_names,
                                        cmap=plt.cm.Blues,
                                        normalize=normalize)
            disp.ax_.set_title(title)

            print(title)
            print(disp.confusion_matrix)

        plt.show()

class Gerenciador_BagOfWords():
    def __init__(self):
        self.nome_arq_controle = 'arquivos/data/bow/arq_controle.json'
        self.arq_controle = None
        self.arq = Arquivo()
        self.bow = BagOfWords()
        self.vocabulario = None
        self.freq_vocabulario = None
        self.tweets = []
        self.tweets_limpos = []
        self.wc = WCloud()
        self.Run()
        
    def Inicializar_arq_controle(self):
        lista = ['atualizacao_data',
                'atualizacao_hora',
                'has_lista_vocabulario',
                'lista_vocabulario_nome',
                'has_dict_freq_vocabulario',
                'dict_freq_vocabulario_nome',
                'total_tweets',
                'total_vocabulos',
                'has_lista_tweets_limpos',
                'lista_tweets_limpos_nome']
        dicio = {}
        for i in lista:
            dicio.update({i:None})
        self.Gravar_arq_JSON(self.nome_arq_controle, dicio)

    def Gravar_arq_JSON(self,nome_arquivo, arquivo):
        with open(nome_arquivo, 'w') as json_file:
            json.dump(arquivo, json_file, indent=4, ensure_ascii=False)
            
    def Carregar_arq_JSON(self, nome_arquivo):
        with open(nome_arquivo, 'r', encoding='utf8') as json_file:
            dados = json.load(json_file)
        return dados
    
    def Atualiza_arq_JSON(self, key, value):
        self.arq_controle.update({key: value})
        self.Gravar_arq_JSON(self.nome_arq_controle,self.arq_controle)
    
    def Carregar_atualizacao(self):
        try:
            self.arq_controle = self.Carregar_arq_JSON(self.nome_arq_controle)
            terminal.Mensagem('arq_controle carregado com Sucesso!', 'ok')
        except Exception as identifier:
            terminal.Mensagem(str(identifier),'e')
        
        try:
            self.vocabulario = self.arq.Carregar_Arquivo_UTF8(self.arq_controle['lista_vocabulario_nome'])
            terminal.Mensagem('vocabulario carregado com Sucesso!', 'ok')
        except Exception as identifier:
            terminal.Mensagem(str(identifier),'e')
        
        try:
            self.freq_vocabulario = self.Carregar_arq_JSON(self.arq_controle['dict_freq_vocabulario_nome'])
            terminal.Mensagem('freq_vocabulario carregado com Sucesso!', 'ok')
        except Exception as identifier:
            terminal.Mensagem(str(identifier),'e')

        try:
            self.tweets_limpos = self.Carregar_PKL(self.arq_controle['lista_tweets_limpos_nome'])
            terminal.Mensagem('lista_tweets_limpos carregado com Sucesso!', 'ok')
        except Exception as identifier:
            terminal.Mensagem(str(identifier),'e')
   
    def __WordCloud(self):
        try:
            self.wc.Build_Nuvem_Palavras(self.tweets_limpos)
            terminal.Mensagem('WordClound Gerado com Sucesso!', 'ok')
        except Exception as identifier:
            terminal.Mensagem(str(identifier),'e')
    
    def Gravar_PKL(self, arquivo, nome_arquivo):
        output = open(nome_arquivo, 'wb')
        dump(arquivo, output, -1)
        output.close()
    
    def Carregar_PKL(self, nome_arquivo):
        Input = open(nome_arquivo, 'rb')
        dados = load(Input)
        Input.close()
        return dados

    def __BOW(self):
        if len(self.tweets) == 0:
            conn = pymysql.connect("localhost","root","", "tw")
            c = conn.cursor()
            query = "SELECT tweet FROM selecionados_notrt_tb"
            c.execute(query)

            while True:
                res = c.fetchall()
                if not res:
                    break
                for result in res:
                    self.tweets.append(result[0])
        
        tam = 1000
        x = int(len(self.tweets)/tam)+1
        for i in range(x):
            if i < x:
                self.tweets_limpos.append(self.bow.Construtor_Vocabulario(self.tweets[tam*i:tam*(i+1)]))
            else:
                self.tweets_limpos.append(self.bow.Construtor_Vocabulario(self.tweets[tam*i:]))
        
        def normalizar_lista(lista_tweets):
            i = 0
            aux = []
            for i in range(len(lista_tweets)):
                j = 0
                for t in lista_tweets[i][0][j]:
                    aux.append(t)
                    j +=1
            return aux
        
        self.tweets_limpos = normalizar_lista(self.tweets_limpos)

        self.Atualiza_arq_JSON('lista_tweets_limpos_nome', 'arquivos/data/bow/lista_tweets_limpos.pkl')
        self.Gravar_PKL(self.tweets_limpos, self.arq_controle['lista_tweets_limpos_nome'])
        self.Atualiza_arq_JSON('has_lista_tweets_limpos', True)
        self.Atualiza_arq_JSON('total_tweets', len(self.tweets))
        self.Atualiza_arq_JSON('total_vocabulos', len(self.vocabulario))
        
        self.Atualiza_arq_JSON('has_lista_vocabulario', True)
        self.Atualiza_arq_JSON('lista_vocabulario_nome', 'arquivos/data/bow/vocabulario.txt')
        self.arq.Gravar_Arquivo(self.bow.vocabulario, self.arq_controle['lista_vocabulario_nome'])
        
        for sent in self.tweets_limpos:
            vetor = self.bow.Vetor(sent)
            self.bow.Verifica_Freq_Vocabulario(vetor)
        
        self.Atualiza_arq_JSON('has_dict_freq_vocabulario', True)
        self.Atualiza_arq_JSON('dict_freq_vocabulario_nome', 'arquivos/data/bow/freq_vocabulario.json')
        self.Gravar_arq_JSON(self.arq_controle['dict_freq_vocabulario_nome'],self.bow.freq_vocabulario)

        fim = time.time()
        data = time.strftime("%d-%m-%Y", time.localtime(fim))
        hora = time.strftime("%H:%M:%S", time.localtime(fim))
        self.Atualiza_arq_JSON('atualizacao_data', data)
        self.Atualiza_arq_JSON('atualizacao_hora', hora)

        self.__WordCloud()

    def Run(self):
        resposta = ''
        self.Carregar_atualizacao()
        if self.arq_controle == None:
            self.Inicializar_arq_controle()
        else:
            terminal.Mensagem('Arquivos Atualizados em %s às %s:\nTotal de Tweets: %i\nTotal de Vocábulos: %i\nDeseja atualizar o Bag Of Words?[S/N]'
                                %(self.arq_controle['atualizacao_data'], self.arq_controle['atualizacao_hora'], 
                                self.arq_controle['total_tweets'], self.arq_controle['total_vocabulos']),'w')
            resposta = str(input()).upper()

        if resposta == 'S':
            self.tweets_limpos.clear()
            self.__BOW()
        elif resposta == 'N':
            terminal.Mensagem('Deseja gerar WordCloud com o arquivo existente?[S/N]','w')
            option = str(input()).upper()
            if option == 'S':
                self.__WordCloud()
            else:
                return False
        else:
            terminal.Mensagem('Resposta Inválida! Informe [S/N].', 'w')
            return False

class Gerenciador_TF_IDF():
    def __init__(self):
        self.tfidf = TF_IDF()
        self.arq = Arquivo()
        self.tweets = []
        self.nome_arq_controle = 'arquivos/data/tf-idf/arq_controle.json'
        self.arq_controle = None
        self.vetor_tfidf = None
        self.feature_names = None
        self.Run()

    def Inicializar_arq_controle(self):
        lista = ['atualizacao_data',
                'atualizacao_hora',
                'has_vetor_tfidf',
                'vetor_tfidf_nome',
                'has_feature_names',
                'feature_names_nome']
        dicio = {}
        for i in lista:
            dicio.update({i:None})
        self.Gravar_arq_JSON(self.nome_arq_controle, dicio)

    def Gravar_arq_JSON(self,nome_arquivo, arquivo):
        with open(nome_arquivo, 'w') as json_file:
            json.dump(arquivo, json_file, indent=4, ensure_ascii=False)
            
    def Carregar_arq_JSON(self, nome_arquivo):
        with open(nome_arquivo, 'r', encoding='utf8') as json_file:
            dados = json.load(json_file)
        return dados
    
    def Atualiza_arq_JSON(self, key, value):
        self.arq_controle.update({key: value})
        self.Gravar_arq_JSON(self.nome_arq_controle,self.arq_controle)

    def Carregar_PKL(self, nome_arquivo):
        Input = open(nome_arquivo, 'rb')
        dados = load(Input)
        Input.close()
        return dados

    def __agregarlistas(self, lista):
        result = []
        aux = []
        if type(lista) == list:
            for item in lista:
                if type(item) == list:
                    aux = self.__agregarlistas(item)
                    result = result + aux
                else:
                    result.append(item)
        return result

    def Carregar_atualizacao(self):
        try:
            self.arq_controle = self.Carregar_arq_JSON(self.nome_arq_controle)
            terminal.Mensagem('arq_controle carregado com Sucesso!', 'ok')
        except Exception as identifier:
            terminal.Mensagem(str(identifier),'e')
        
        try:
            self.vetor_tfidf = self.Carregar_PKL(self.arq_controle['vetor_tfidf_nome'])
            terminal.Mensagem('vetor_tfidf carregado com Sucesso!', 'ok')
        except Exception as identifier:
            terminal.Mensagem(str(identifier),'e')
        
        try:
            self.feature_names = self.arq.Carregar_Arquivo_UTF8(self.arq_controle['feature_names_nome'])
            terminal.Mensagem('feature_names carregado com Sucesso!', 'ok')
        except Exception as identifier:
            terminal.Mensagem(str(identifier),'e')

    def Run(self):

        def Executar_tfidf():
            aux = []
            aux = self.Carregar_PKL('arquivos/data/bow/lista_tweets_limpos.pkl')
            self.tweets = self.__agregarlistas(aux)
            self.tfidf.Gerar_Dados(self.tweets)

            self.Atualiza_arq_JSON('has_vetor_tfidf', True)
            self.Atualiza_arq_JSON('vetor_tfidf_nome', 'arquivos/data/tf-idf/vetor_tfidf.pkl')
            self.Atualiza_arq_JSON('has_feature_names', True)
            self.Atualiza_arq_JSON('feature_names_nome', 'arquivos/data/tf-idf/feature_names.txt')

            fim = time.time()
            data = time.strftime("%d-%m-%Y", time.localtime(fim))
            hora = time.strftime("%H:%M:%S", time.localtime(fim))
            self.Atualiza_arq_JSON('atualizacao_data', data)
            self.Atualiza_arq_JSON('atualizacao_hora', hora)

        resposta = ''
        res = ''
        self.Carregar_atualizacao()
        if self.arq_controle == None:
            self.Inicializar_arq_controle()
        elif not self.arq_controle['has_vetor_tfidf'] and not self.arq_controle['has_feature_names']:
            Executar_tfidf()
        else:
            terminal.Mensagem('Arquivos Atualizados em %s às %s:\nDeseja atualizar o TF-IDF?[S/N]'
                                %(self.arq_controle['atualizacao_data'], self.arq_controle['atualizacao_hora']),'w')
            resposta = str(input()).upper()
        if resposta == 'S':
            Executar_tfidf()
        elif resposta == 'N':
            terminal.Mensagem('Deseja Visualizar o arquivo existente?[S/N]','w')
            res = str(input()).upper()
            if res == 'S':
                if self.arq_controle['has_vetor_tfidf'] and self.arq_controle['has_feature_names']:
                    row_label = ['Tweet %i'% i for i in range(len(self.tweets))]
                    col_label = self.feature_names
                    self.tfidf.Gerar_tabela(45,5,8,row_label, col_label, self.vetor_tfidf)
                else:
                    Executar_tfidf()
            else:
                return False
        else:
            return False
