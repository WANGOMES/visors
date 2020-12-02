import pymysql
from Manipulador_arquivos import Arquivo
from evaluation import Avaliacao, Arvore
from analyzer import Extracao_Informacao, AnaliseLexica
import re
from interface import interface_terminal as terminal
import numpy
import threading
import time
import json

class Conexao():
    conn = pymysql.connect("localhost","root","", "tw")
    c = conn.cursor()
    Verificacao_dados = []
    

    def query(self, word, query):
        word = word.split(',')
        query = query.format(word[0], word[1])
        return query
    
    def consulta_base(self, lista_palavras, query, nome_arquivo):
        lista = []
        arq = Arquivo()
        mes = {'2020-01-01,2020-01-31':'janeiro',
                    '2020-02-01,2020-02-28':'fevereiro',
                    '2020-03-01,2020-03-31':'março',
                    '2020-04-01,2020-04-30':'abril',
                    '2020-05-01,2020-05-31':'maio',
                    '2020-06-01,2020-06-30':'junho',
                    '2020-07-01,2020-07-31':'julho',
                    '2020-08-01,2020-08-31':'agosto',
                    '2020-09-01,2020-09-30':'setembro',
                    '2020-10-01,2020-10-31':'outubro',
                    '2020-11-01,2020-11-30':'novembro',
                    '2020-12-01,2020-12-31':'dezembro'}
        
        for w in lista_palavras:
            self.c.execute(self.query(w, query))
            label = mes[w]
            while True:
                res = self.c.fetchall()
                if not res:
                    break
                for result in res:
                    if (self.Verifica_Dados(label, nome_arquivo)):
                        lista.append(label + ';' + str(result[0]))
                        print(label + ';'+ str(result[0]))
        arq.Gravar_Arquivo(lista, (nome_arquivo))
    
    def consulta_base_geral(self, lista_palavras, query):
        lista = []
        if type(lista_palavras) == list:
            for w in lista_palavras:
                self.c.execute(self.query(w, query))
                # label = self.mes[w]
                # if len(lista) == 0:
                #     lista.append(label)
                while True:
                    res = self.c.fetchall()
                    if not res:
                        break
                    for result in res:
                            lista.append(str(result[0]))
        elif type(lista_palavras) == str:
            w = lista_palavras
            self.c.execute(self.query(w, query))
            while True:
                    res = self.c.fetchall()
                    if not res:
                        break
                    for result in res:
                            lista.append(str(result[0]))
        return lista

    def Fechar_Conexao(self):
        self.conn.close()
    
    def Verifica_Dados(self, id_table, nome_arquivo):
        if(len(self.Verificacao_dados)==0):
            arq = Arquivo()
            try:
                lista = arq.Carregar_Arquivo(nome_arquivo)
                self.Verificacao_dados = lista
            except Exception as identifier:
                print(identifier)
                return True
        else:
            lista = self.Verificacao_dados
        count = 0
        for item in lista:
            item = item.rstrip()
            item = item.split(';')
            item = item[0]
            if (item == id_table):
                count += 1
        
        if count == 0:
            return True
        else:
            return False

class Estatistica():
    def __init__(self):
        self.conex = Conexao()
        self.arq = Arquivo()
        # self.avaliacao = Avaliacao()
        # self.analise = AnaliseLexica()
        # self.ext = Extracao_Informacao()
        # self.FRACAO = 10
        # self.status = self.CarregarStatus()
        # self.dicio_arquivo_pkl = dict()
        # self.Num_Processo = 1
        # self.Total_Processos = self.FRACAO
        self.Run('arquivos/consulta.txt')
        

    def CarregarDicioPKL(self, lista):
        for item in lista:
            self.dicio_arquivo_pkl.update({item: False})
    
    def AtualizarDicioPKL(self, chave):
        self.dicio_arquivo_pkl.update({chave: True})
        self.GravaDicioPKL()

    def GravaDicioPKL(self):
        try:
            with open('arquivos/estatistica/pkl/dicio_arquivo_pkl.json', 'w') as json_file:
                json.dump(self.dicio_arquivo_pkl, json_file, indent=4)
        except FileNotFoundError as identifier:
            terminal.Mensagem('%s - Arquivo não encontrado!' % identifier, 'e')
 
    def CarregarStatus(self):
        dados = ''
        try:
            with open('arquivos/estatistica/status.json', 'r') as json_file:
                dados = json.load(json_file)
        except FileNotFoundError as identifier:
            dados = {'BancoDados': False, #Base de dados Consultada
            'Remove_Caract_Esp': False, #Caracteres Especiais Removidos
            'Remove_Stopwords': False, #Stopwords Removidos
            'Remove_Pontuacao': False, #Pontuação Removida
            'Concat': False, #Concatenado
            'SplitLista': False, #Split dados
            'Dir_Arq_pkl': 'arquivos/estatistica/pkl', #Diretório PLK
            'Arq_pkl_Lista': [], #Lista arq. plk
            'Chunking': False, #Chunking
            'Remove_Caract_Chunk': False, #Caract Removidos
            'Freq_Palavras': False, #Freqeuncia Palavras
            'Arq_Final_Lista': [], #Lista de arquivos finais
            'Data_Atualizacao': None}
        return dados

    def AtualizaStatus(self, chave, valor):
        self.status.update({chave: valor})
        self.GravaStatus()

    def GravaStatus(self):
        try:
            with open('arquivos/estatistica/status.json', 'w') as json_file:
                json.dump(self.status, json_file, indent=4)
        except FileNotFoundError as identifier:
            terminal.Mensagem('%s - Arquivo não encontrado!' % identifier, 'e')

    def Concatenate(self):
        lista1 = self.arq.Carregar_Arquivo('arquivos/result.txt') # total
        lista2 = self.arq.Carregar_Arquivo('arquivos/result2RT.txt') # somente RT
        lista3 = self.arq.Carregar_Arquivo('arquivos/result3GEO.txt') # geo
        try:
            Lista_estatistica = self.arq.Carregar_Arquivo('arquivos/result_Estatistica.txt')
        except expression as identifier:
            Lista_estatistica = []
        result = []
        cont = 0
        repete = False
        for i in lista1:
            label = i.split(';')
            label = label[0]
            if(len(Lista_estatistica)!=0):
                for item in Lista_estatistica:
                    label_item = item.split(';')
                    label_item = label_item[0]
                    if(label == label_item):
                        repete = True
                    if(not repete):
                        a1 = lista2[cont].split(';')
                        a1 = a1[1]
                        a2 = lista3[cont].split(';')
                        a2 = a2[1]
                        result.append(i + ';' + a1 + ';' + a2)
                        print(i + ';' + a1 + ';' + a2)
                        cont += 1
                        repete = False
                    else:
                        cont += 1

        self.arq.Gravar_Arquivo(result, 'arquivos/result_Estatistica.txt')
    
    def Consulta_Todos_Tweets_Mes(self, mes):
        '''
        Retorna um arquivo com as 50 palavras mais utilizadas em um determinado mês.

        :parametro mes: Mês que deseja fazer a pesquisa
        '''
        terminal.Mensagem('MÓDULO Estatísticas Iniciado com Sucesso...', 'ok')
        
        meses = {'janeiro':'2020-01-01,2020-01-31',
                'fevereiro':'2020-02-01,2020-02-28',
                'março':'2020-03-01,2020-03-31',
                'abril':'2020-04-01,2020-04-30',
                'maio':'2020-05-01,2020-05-31',
                'junho':'2020-06-01,2020-06-30',
                'julho':'2020-07-01,2020-07-31',
                'agosto':'2020-08-01,2020-08-31',
                'setembro':'2020-09-01,2020-09-30',
                'outubro':'2020-10-01,2020-10-31',
                'novembro':'2020-11-01,2020-11-30',
                'dezembro':'2020-12-01,2020-12-31',
                'jan':'2020-01-01,2020-01-31',
                'fev':'2020-02-01,2020-02-28',
                'mar':'2020-03-01,2020-03-31',
                'abr':'2020-04-01,2020-04-30',
                'mai':'2020-05-01,2020-05-31',
                'jun':'2020-06-01,2020-06-30',
                'jul':'2020-07-01,2020-07-31',
                'ago':'2020-08-01,2020-08-31',
                'set':'2020-09-01,2020-09-30',
                'out':'2020-10-01,2020-10-31',
                'nov':'2020-11-01,2020-11-30',
                'dez':'2020-12-01,2020-12-31',
                '1':'2020-01-01,2020-01-31',
                '2':'2020-02-01,2020-02-28',
                '3':'2020-03-01,2020-03-31',
                '4':'2020-04-01,2020-04-30',
                '5':'2020-05-01,2020-05-31',
                '6':'2020-06-01,2020-06-30',
                '7':'2020-07-01,2020-07-31',
                '8':'2020-08-01,2020-08-31',
                '9':'2020-09-01,2020-09-30',
                '10':'2020-10-01,2020-10-31',
                '11':'2020-11-01,2020-11-30',
                '12':'2020-12-01,2020-12-31',
                '01':'2020-01-01,2020-01-31',
                '02':'2020-02-01,2020-02-28',
                '03':'2020-03-01,2020-03-31',
                '04':'2020-04-01,2020-04-30',
                '05':'2020-05-01,2020-05-31',
                '06':'2020-06-01,2020-06-30',
                '07':'2020-07-01,2020-07-31',
                '08':'2020-08-01,2020-08-31',
                '09':'2020-09-01,2020-09-30',
                '10':'2020-10-01,2020-10-31',
                '11':'2020-11-01,2020-11-30',
                '12':'2020-12-01,2020-12-31'}
        
        _mes = {'2020-01-01,2020-01-31':'janeiro',
                    '2020-02-01,2020-02-28':'fevereiro',
                    '2020-03-01,2020-03-31':'março',
                    '2020-04-01,2020-04-30':'abril',
                    '2020-05-01,2020-05-31':'maio',
                    '2020-06-01,2020-06-30':'junho',
                    '2020-07-01,2020-07-31':'julho',
                    '2020-08-01,2020-08-31':'agosto',
                    '2020-09-01,2020-09-30':'setembro',
                    '2020-10-01,2020-10-31':'outubro',
                    '2020-11-01,2020-11-30':'novembro',
                    '2020-12-01,2020-12-31':'dezembro'}
        
        query = "SELECT tweet FROM `tweet_tb` WHERE `datetime` BETWEEN '{} 00:00:00.000000' AND '{} 23:59:59.999999' AND `tweet` NOT like 'RT%'"

        ### Consulta Base de Dados ###
        terminal.Mensagem('Iniciando Consulta Base de Dados...', 'w')
        ini_consulta = time.time()
        result = self.conex.consulta_base_geral(meses[mes], query)
        self.conex.Fechar_Conexao()
        self.AtualizaStatus('BancoDados', True)
        fim_consulta = time.time()
        terminal.Mensagem('Concluído com Sucesso em %3f seg!' % ((fim_consulta - ini_consulta)), 'ok')
        nome_arquivo_mes = str(_mes[meses[mes]])

        ### Removendo Caracteres Especiais ###
        terminal.Mensagem('Removendo Caracteres Especiais...', 'w')
        result = [self.analise.Remocao_caracteres_Tweets(r) for r in result]
        self.AtualizaStatus('Remove_Caract_Esp', True)
        terminal.Mensagem('Concluído com Sucesso!', 'ok')
        
        ### Removendo Stopwords ###
        terminal.Mensagem('Removendo Stopwords...', 'w')
        resultado = [self.analise.Remocao_Stopword(r) for r in result]
        self.AtualizaStatus('Remove_Stopwords', True)
        terminal.Mensagem('Concluído com Sucesso!', 'ok')

        ### Removendo Pontuação ###
        terminal.Mensagem('Removendo Pontuação...', 'w')
        resultado = [self.analise.Remocao_Pontuacao(r) for r in resultado]
        self.AtualizaStatus('Remove_Pontuacao', True)
        terminal.Mensagem('Concluído com Sucesso!', 'ok')

        ### Concatenando ###
        terminal.Mensagem('Concatenando...', 'w')
        resultado = [self.avaliacao.Concatenar_Texto(c) for c in resultado]
        self.AtualizaStatus('Concat', True)
        terminal.Mensagem('Concluído com Sucesso!', 'ok')

        ### Faz a separação da lista e grava em arquivos ###
        self.SplitLista(resultado, nome_arquivo_mes)

        terminal.Mensagem('Deseja iniciar o processo de Nuvem de Palavras? (S/N) ', 's')
        opcao = input()
        while opcao.upper() != 'N':
            self.ProduzirNuvemPalavras(nome_arquivo_mes)
            terminal.Mensagem('Processo %i/%i: Deseja Continuar? (S/N) '% (self.Num_Processo, self.Total_Processos), 's')
            opcao = input()
        terminal.Mensagem('Status: %i Processos Executados\t%i Processos Restantes'% (self.Num_Processo, self.Total_Processos - self.Num_Processo), 'w')

    def SplitLista(self, lista, nome_arquivo_mes):
        T = len(lista)
        quant = int(T/self.FRACAO)
        j = 0
        i = self.FRACAO
        while j < i:
            inicio = quant*j
            fim = quant * (j+1)

            if(j+1) < 10:
                nome_arquivo_pkl = '%s/%s/00%i%s' % (self.status['Dir_Arq_pkl'], nome_arquivo_mes, j+1,'.pkl')
            else:
                nome_arquivo_pkl = '%s/%s/0%i%s' % (self.status['Dir_Arq_pkl'], nome_arquivo_mes, j+1,'.pkl')
            
            if j == i-1:
                self.Serializar(inicio, T, lista, nome_arquivo_pkl)
            else:
                self.Serializar(inicio, fim, lista, nome_arquivo_pkl)
            
            j +=1
        self.AtualizaStatus('SplitLista', True)
        terminal.Mensagem('Serialização Concluída com Sucesso!', 's')

    def Serializar(self, inicio, fim, lista, nome_arquivo_pkl):
        new = lista[inicio : fim]
        
        output = open(nome_arquivo_pkl, 'wb')
        dump(new, output, -1)
        output.close()
        
        self.status['Arq_pkl_Lista'].append(nome_arquivo_pkl)

    def ProduzirNuvemPalavras(self, nome_arquivo_mes):
        if self.status['SplitLista']:
            self.CarregarDicioPKL(self.status['Arq_pkl_Lista'])

        nome_pkl = ''
        contador = 0
        j = 0
        n_proc = 0
        for k in self.dicio_arquivo_pkl.keys():
            n_proc +=1
            if not self.dicio_arquivo_pkl[k]:
                j += 1
                nome_arquivo = 'arquivos/estatistica/%s/0%i.txt' % (nome_arquivo_mes, j)
                nome_pkl = k
                contador += 1
                break
        if contador > 0:
            try:
                Input = open( nome_pkl, 'rb')
                dados = load(Input)
                Input.close()

                # T = len(dados)
                # quant = int(T/self.FRACAO)
                
                # cont = 0
                # i = self.FRACAO
                # while cont < i:
                #     inicio = quant*cont
                #     fim = quant * (cont+1)

                #     if cont == i-1:
                # #     Dados_Fracao = self.__DadosLista(inicio, T, dados)
                #     th001 = threading.Timer(3.0,self.__Producao_Nuvem_Palavras(Dados_Fracao, nome_arquivo))
                #     th001.start()
                #     print('%s iniciando... ' % th001.getName())
                
                # # th001 = threading.Timer(3.0,self.Serializar(inicio, T, lista, nome_arquivo_pkl))
                # # print('%s iniciando... Tarefa: %i' % (th001.getName(),j+1))
                # # th001.start()
                # else:
                #     Dados_Fracao = self.__DadosLista(inicio, fim, dados)
                #     th001 = threading.Timer(3.0,self.__Producao_Nuvem_Palavras(Dados_Fracao, nome_arquivo))
                #     th001.start()
                #     print('%s iniciando... ' % th001.getName())
                # '''PAREI AQUI'''

                th001 = threading.Timer(3.0,self.__Producao_Nuvem_Palavras(dados, nome_arquivo))
                th001.start()
                print('%s iniciando... ' % th001.getName())
                th001.cancel()
                print('%s Terminando... ' % (th001.getName()))
                self.AtualizarDicioPKL(nome_pkl)
                self.Num_Processo = n_proc
            except Exception as identifier:
                self.Num_Processo = n_proc
                terminal.Mensagem('%s' % identifier, 'e')
                
        else:
            self.Num_Processo = n_proc
            terminal.Mensagem('Não há arquivos para carregar!','w')
            
    def __DadosLista(self, inicio, fim, lista):
        res = lista[inicio : fim]
        return res  

    def __Producao_Nuvem_Palavras(self, dados, nome_arquivo):
            ### Chunking ###
            regra = r'''A1: {(<N+\w+ | N>)}'''
            terminal.Mensagem('Iniciando Chunking...', 'w')
            count = 0
            tam = len(dados)
            chunk = []
            arvore_busca = []

            for texto in dados:
                count += 1
                chunk += self.ext.Chunking(regra, texto)
                terminal.printProgressBar(count,tam,length=50)
            terminal.Mensagem('Concluído com Sucesso!', 'ok')
            self.AtualizaStatus('Chunking', True)
            
            ### Buscando elementos ###
            arvore = Arvore(chunk)
            terminal.Mensagem('Buscando Elementos no Chunk...', 'w')
            for c in chunk:
                arvore_busca += arvore.Buscar_Elemento(c,'A1')
                terminal.printProgressBar(count,tam,length=50)
            terminal.Mensagem('Concluído com Sucesso!', 'ok')
            
            ### Removendo Caracteres no Chunk ###
            terminal.Mensagem('Removendo Caracteres no Chunk...', 'w')
            arvore_busca = self.analise.Remove_Caracteres_Chunk(arvore_busca)
            self.AtualizaStatus('Remove_Caract_Chunk', True)
            terminal.Mensagem('Concluído com Sucesso!', 'ok')

            ### Verificando Frequencia das Palavras ###
            terminal.Mensagem('Verificando Frequencia das Palavras...', 'w')
            avaliado = self.avaliacao.NuvemDePalavras(arvore_busca)
            self.AtualizaStatus('Freq_Palavras', True)
            terminal.Mensagem('Concluído com Sucesso!', 'ok')

            self.arq.Gravar_Arquivo(avaliado, nome_arquivo)
            now = time.time()
            self.AtualizaStatus('Data_Atualizacao', time.strftime('%d/%b/%Y %H:%M:%S', time.localtime(now)))

    def Run(self, nome_arquivo):
        # terminal.Mensagem('MÓDULO Estatísticas Iniciado com Sucesso...', 'ok')

        # keywords = self.arq.Carregar_Arquivo(nome_arquivo)

        # geo = "SELECT COUNT(id) FROM `tweet_tb` WHERE `datetime` BETWEEN '{} 00:00:00.000000' AND '{} 23:59:59.999999' AND (user_local IS NOT NULL OR geo IS NOT NULL OR coordinates IS NOT NULL OR place IS NOT NULL) AND `tweet` NOT LIKE 'RT%'"
        # total = "SELECT COUNT(id) FROM `tweet_tb` WHERE `datetime` BETWEEN '{} 00:00:00.000000' AND '{} 23:59:59.999999'"
        # rt = "SELECT COUNT(id) FROM `tweet_tb` WHERE `datetime` BETWEEN '{} 00:00:00.000000' AND '{} 23:59:59.999999' AND `tweet` like 'RT%'"

        # nome_arq_rt = 'arquivos/result2RT.txt'
        # nome_arq_total = 'arquivos/result.txt'
        # nome_arq_geo = 'arquivos/result3GEO.txt'

        # self.conex.consulta_base(keywords, total, nome_arq_total)
        # self.conex.consulta_base(keywords, rt, nome_arq_rt)
        # self.conex.consulta_base(keywords, geo, nome_arq_geo)
        # self.conex.Fechar_Conexao()

        self.Concatenate()

est = Estatistica()
# est.Concatenate()
# # est.Consulta_Todos_Tweets_Mes('04')
# # est.Concatenate()
# print(est.Consulta_Todos_Tweets_Mes('04'))





# query = "SELECT COUNT(id) FROM `tweet_tb` WHERE `datetime` BETWEEN '{} 00:00:00.000000' AND '{} 23:59:59.999999' AND (user_local IS NOT NULL OR geo IS NOT NULL OR coordinates IS NOT NULL OR place IS NOT NULL)"
# # query = "SELECT COUNT(id) FROM `tweet_tb` WHERE `datetime` BETWEEN '{} 00:00:00.000000' AND '{} 23:59:59.999999'"
# # query = "SELECT COUNT(id) FROM `tweet_tb` WHERE `datetime` BETWEEN '{} 00:00:00.000000' AND '{} 23:59:59.999999' AND `tweet` like 'RT%'"

# # nome_arquivo = 'result2RT.txt'
# # nome_arquivo = 'result.txt'
# nome_arquivo = 'result3GEO.txt'

# keywords = arq.Carregar_Arquivo('consulta.txt')
# essa.consulta_base(keywords, query, nome_arquivo)
# est = Estatistica('-1')

# print(est.status)
# # est.AtualizaStatus('BancoDados', 2000)
# # print(est.status)