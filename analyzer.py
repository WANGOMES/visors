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

# -*- coding: utf-8 -*-
from Manipulador_arquivos import Arquivo
import pymysql
from nltk.text import Text
from nltk.tokenize import word_tokenize
import re # re(Regular Expressions) Biblioteca em Python que manipula Expressões Regulares
import nltk
from pickle import dump
from pickle import load
from nltk.corpus import mac_morpho #Importa a biblioteca para etiquetas de classes gramaticais - tagging
from nltk.metrics import accuracy
from interface import interface_terminal as terminal

class Tokenizacao():
    def Token(self, texto):
        if type(texto) == list:
            token = [word_tokenize(t, language='portuguese') for t in texto]
        elif type(texto) == str:
            token = word_tokenize(texto, language='portuguese')
        return token

    def Expressoes_Regulares(self, stem, texto):
        resultado = re.findall(r''+ stem +'\w*', texto)
        return resultado

    def Posicao_palavra(self, palavra, texto):
        resultado = re.search(r''+palavra, texto)
        if resultado != None:
            print('palavra: ' + resultado.group(0) + '\nposição: ' + str(resultado.span()))
            res = str(resultado.span())
        else:
            print('palavra ' + palavra + ' não foi encontrada!')
            res = None
        return res

class AnaliseLexica():
    def Remocao_Stopword(self, texto):

        def __verifica_Type(texto):
            t = Tokenizacao()
            if type(texto)== str:
                token = t.Token(texto.lower()) #Tokenizado
            elif type(texto) == list:
                for text in texto:
                    if type(text) == list:
                        token = __verifica_Type(text)
                        break
                    elif type(text) == str:
                        token = []
                        token.append(t.Token(text.lower())) #Tokenizado
            else:
                token = t.Token(texto.lower())
            return token

        lista = []

        def __remocao_stopwords(palavra):
            stopword = nltk.corpus.stopwords.words('portuguese')
            stw = set(['vc','voce', 'todos', 'cara', 'onde', 'b', 'fala', 'inteira', 'so', 'sabado', 'caiu', 'domingo','mim', 'ter', 'amg', 'ja', 'toda', 'hoje', 'conta', 'dar', 'sempre', 'ai','h', 'menos','via', 'at', 'ontem', 'assim', 'modo', 'noite', 'olha', 'tarde', 'vou', 'vai', 'to', 'tao', 'tava', 'ta', 'tamo', 'tanta', 'tanto', 'q', 'sei', 'ser', 'pra', 'pq', 'porque', 'quanto', 'ne', 'muitos', 'muitas', 'muito', 'muita', 'nao', 'nada', 'n', 'mesmo', 'mesma', 'live', 'fazer', 'fica', 'ficar', 'ficava', 'fiz', 'enquanto', 'diria', 'diriam', 'dessa', 'desse', 'desses', 'dessas', 'desde', 'cmg', 'acha', 'acho'])
            resposta = ''
            count = 0
            cont = 0
            for sw in stopword:
                if palavra == sw:
                    count +=1
                    break
            if count == 0:
                for word in stw:
                    if palavra == word:
                        cont +=1
                        break
            if (count == 0 and cont == 0):
                resposta = palavra
            return resposta
        
        token = __verifica_Type(texto)

        for palavra in token:
            if type(palavra) == list:
                for word in palavra:
                    t = __remocao_stopwords(word)
                    if len(t) != 0:
                        lista.append(t)
            else:
                lista.append(__remocao_stopwords(palavra))
        return lista
    
    def Stemmers(self, termo):
        stemmer = nltk.stem.RSLPStemmer() # Em portugues
        resultado = stemmer.stem(termo)
        return resultado
    
    def Stemmers_lista (self, lista):
        resultado = []
        for word in lista:
            resultado.append(self.Stemmers(word))
        return resultado
    
    def Remocao_Pontuacao(self, token):
        lista = []
        def __remove_pontuacao(word):
            Sinais = ['.',',','?','!','-',':',';','...','(',')','[',']','{','}', '&', '\*','``','\“', "\'\'",'…']
            lista = []
            pos = []
            count = 0
            for s in Sinais:
                if word == s:
                    pos.append(count)
                    break
            lista.append(word)
            count +=1
            if len(pos) !=0:
                pos.reverse()
                for posicao in pos:
                    lista.pop(posicao)
            return lista

        for word in token:
            if type(word)==list:
                for _word in word:
                    lista.append(__remove_pontuacao(_word))
            else:
                lista.append(__remove_pontuacao(word))
        return lista
            
    def Remocao_acentuacao(self, termo):
        lista = []

        def __remove_acentuacao(termo):
            lista = []
            Normal = {'á': 'a',
                    'â': 'a',
                    'ã': 'a',
                    'à': 'a',
                    'é': 'e',
                    'ê': 'e',
                    'í': 'i',
                    'ó': 'o',
                    'ô': 'o',
                    'ú': 'u',
                    'ç': 'c'}
            for k in termo:
                try:
                    lista.append(Normal[k])
                except KeyError as identifier:
                    lista.append(k)
            return ''.join(lista)

        if type(termo)==list:
            for term in termo:
                term = term.lower()
                lista.append(__remove_acentuacao(term))
        elif type(termo) == str:
            term = termo.lower()
            lista.append(__remove_acentuacao(term))
        return lista 
    
    def Remocao_acentuacao_lista(self, lista):
        res = [self.Remocao_acentuacao(termo) for termo in lista]
        return res

    def __Remocao_caracteres_Tweets(self, tweet):
        user = re.compile(r'@\w+')
        site = re.compile(r'\bhttps://\w+[./#]\w+\b')
        site1 = re.compile(r'\bhttps//t.co\/\w+\b') #https//t.co/iKPoA75HUB
        site2 = re.compile(r'https//t.\w+\b')
        rt = re.compile(r'\bRT\b')
        linha = re.compile(r'\n')
        tab = re.compile(r'\t')
        tags = re.compile(r'#\w+')
        space = re.compile(r'\s\s+')
        space2 = re.compile(r'\B\s')
        space3 = re.compile(r'\s+\B')
        number = re.compile(r'\d')
        reticencias = re.compile(r'\…')
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
                            r'\B\¯', r'\›', r'\b\›',r'\B\›']
        
        kkk = re.compile(r'\b[k|K]{3,100}')
        tag_especiais = [r'\&lt;',r'\&le;' ,r'\&ge;',r'\&amp;',r'\&current;',r'\&trade;',r'\&gt;']
        emoticons = [r"\bO:\)\b", r"=D",r":-D", r"=\]", r":-X", r"=^.^=", r":'\(", r":-\)'", r"}:\(", r":-7", r":*",
                        r":-#", r":-\{", r"@\}-;-'--", r":\(", r"=O", r":\)", r"8-\)", r":-\)", r":-\|", 
                        r"=p", r":-\\", r";\)", r":-*",r"=B", r"^^", r"D:", r"--'", r"d\(-_-\)b", r"o.O",
                        r"T_T", r"U_U", r"$_$", r"\{\{\{\(>_<\)\}\}\}", r"\/\/.*\)", r"X-\(", r"~:@", r"o\-<\]:",
                        r"\(_8^\(\|\)", r"B^\)"]

        lista_remocao = [kkk, user, site, site1, site2, rt, number, tab, tags, reticencias]
        lista_remocao_espacos = [space2, space3]

        result = tweet

        for tesp in tag_especiais:
            t = re.compile(tesp)
            result = re.sub(t, ' ', result)
        
        for emot in emoticons:
            e = re.compile(emot)
            result = re.sub(e, '', result)
        
        result = re.sub(linha, ' ', result)

        for er in lista_remocao:
            result = re.sub(er, '', result)
        
        for item in caract:
            e = re.compile(item)
            result = re.sub(e, ' ', result)

        result = re.sub(space, ' ', result)
        
        for a in lista_remocao_espacos:
            result = re.sub(a, '', result)

        return result

    def Remocao_caracteres_Tweets(self, tweet):
        
        if type(tweet) == list:
            resultado = []
            resultado.append([self.__Remocao_caracteres_Tweets(t) for t in tweet])
        else:
            resultado = ''
            resultado = self.__Remocao_caracteres_Tweets(tweet)
        return resultado
   
    def Remove_Caracteres_Chunk(self, lista_chunks):
        re0 = re.compile(r'\bTree\(\'A1\',\s\[\(')
        re1 = re.compile(r'[,]\s\'\w+\'\)\]\)')
        re2 = re.compile(r'\s{1,3}')
        lista = [re0, re1, re2]
        result = []
        for item in lista_chunks:
            for j in lista:
                item = re.sub(j , '', item)
            result.append(item)
        return result

class AnaliseSintatica_Semantica():
    def __init__(self):
        #Carrega as sentença rotuladas do Corpus
        self.sentencas_etiquetadas = mac_morpho.tagged_sents()
        # # tags = [tag for (word, tag) in mac_morpho.tagged_words()]
        self.padrao = 'N' # nltk.FreqDist(tags).max() # Retorna N - substantivo
    
    def Aplicar_Tagging_Padrao(self, sentenca): #Aplica tag padrão para uma sentença
        etiqPadrao =  nltk.tag.DefaultTagger(self.padrao)
        return etiqPadrao.tag(sentenca)

    def Aplicar_Tagging_treinamento(self, sentenca):#Aplica tag treinada para uma sentença
        tagger = self.Carregar_tag()
        result = tagger.tag(sentenca)
        
        return result

    def Tagging_treinamento(self): #treina a base de Corpus do Mac_morpho
        tagpadrao = nltk.DefaultTagger(self.padrao)
        tag1 = nltk.UnigramTagger(self.sentencas_etiquetadas, backoff=tagpadrao)
        print(tag1.evaluate(tagpadrao))
        tag2 = nltk.BigramTagger(self.sentencas_etiquetadas, backoff=tag1)
        print(tag2.evaluate(tag1))
        tag3 = nltk.TrigramTagger(self.sentencas_etiquetadas, backoff=tag2)
        print(tag3.evaluate(tag2))
        self.Salvar_tag(tag3)
    
    def Salvar_tag(self, tag):
        output = open('arquivos/mac_morpho.pkl', 'wb')
        dump(tag, output, -1)
        output.close()
        print('* * * tags salvas...')
    
    def Carregar_tag(self):
        Input = open('arquivos/mac_morpho.pkl', 'rb')
        tag = load(Input)
        Input.close()
        return tag
    
class Extracao_Informacao():
    def __init__(self):
        self.tk = Tokenizacao()
        self.ass = AnaliseSintatica_Semantica()

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

    def Segmentador(self, texto):
        """
        Retorna uma sentença tokenizada, segmentada e etiquetada.
        Em lingua portuguesa Brasil - pt-br

        :parametro texto: texto para tokenização
        :parametro Obj Tokenização: Obj do Analyzer
        :parametro Obj AnaliseSintatica_Semantica: Obj do Analyzer
        """
        if ((type(texto) == list) | (type(texto) == set)):
            sent = [nltk.sent_tokenize(t,language='portuguese') for t in texto]
            sent = self.__agregarlistas(sent)
        elif type(texto) == str:
            sent = nltk.sent_tokenize(texto,language='portuguese')
        sent = [self.tk.Token(s) for s in sent]
        sent = [self.ass.Aplicar_Tagging_treinamento(s) for s in sent]
        return sent
    
    def Chunking(self, regra_gramatical, texto):
        """
        Retorna uma lista de árvores semanticas analisadas conforme a regra gramatical inserida nos parametros.
        Em lingua portuguesa Brasil - pt-br

        :parametro regra_gramatical: uma regra definida para aplicação no texto
        :parametro texto: texto para tokenização
        :parametro Obj Tokenização: Obj do Analyzer
        :parametro Obj AnaliseSintatica_Semantica: Obj do Analyzer
        """
        sent_etiq = self.Segmentador(texto)       
        analise_gramatical = nltk.RegexpParser(regra_gramatical) 
        chunked = []
        for s in sent_etiq:
        #     if type(s) == list:
        #         chunked.append(analise_gramatical.parse(ss) for ss in s)
        #     else:
            chunked.append(analise_gramatical.parse(s))
        return chunked

    def NER(self, texto):
        """
        NER (Named Entity Recognition)

        Retorna um Chunking com a identificação de Entidades Nomeadas (Named Entity) conforme a regra gramatical já definida.
        Em lingua portuguesa Brasil - pt-br

        :parametro texto: texto para tokenização
        :parametro Obj Tokenização: Obj do Analyzer
        :parametro Obj AnaliseSintatica_Semantica: Obj do Analyzer
        """
        NE = r"""NE: {<NPROP>+}"""
        return self.Chunking(NE, texto)
    
    def Relacionamento_Entidades_Nomeadas(self, texto):
        gramatica = r""" NE: {<NPROP>+}
                    REL: {<NE> <.*>* <PREP.*> <.*>* <NE>} """
        return self.Chunking(gramatica, texto)

class AnaliseLocalização():
    '''
    Retorna lista de cidades validadas para aplicação de geolocalização

    :parametro tweets_selecionados: lista de tweets selecionados
    '''
    def __init__(self):
        self.arq = Arquivo()
        self.analise = AnaliseLexica()
        self.arquivo = self.arq.Carregar_Arquivo('arquivos/arq_controle_mun_bra_ibge.csv')
        self.cidades = self.arq.Carregar_Arquivo('arquivos/municipios_brasileiros_ibge.csv')
        self._ids_tweets_localizacao = self.arq.Carregar_Arquivo('arquivos/data/lsa/_ids_tweets_localizacao.txt')
        self.arq_controle_cidades = {}
        self.cidades_validadas = []
        self.Carregar_arq_controle_cidades()
        self.Localizacoes()
    
    def AgregarListas(self, lista):
        result = []
        aux = []
        if type(lista) == list:
            for item in lista:
                if type(item) == list:
                    aux = self.AgregarListas(item)
                    result = result + aux
                else:
                    result.append(item)
        else:
            result.append(lista)
        return result

    def _Selecionar_localizacao_tweets_banco_(self, lista_ids_tweets):
        aux = ''
        for item in lista_ids_tweets:
            if item != lista_ids_tweets[-1]:
                aux += 'id=%i OR '%(int(item) + 610) #foram desprezados 609 tweets
            else:
                aux += 'id=%i'%(int(item) + 610)
        
        conn = pymysql.connect("localhost","root","", "tw")
        c = conn.cursor()
        query = "SELECT user_local, geo, coordinates, place, tweet FROM `selecionados_notrt_tb` WHERE %s"%aux
        c.execute(query)
        lista = []
        while True:
            res = c.fetchall()
            if not res:
                break
            for result in res:
                lista.append(str(result[0]))
                lista.append(str(result[1]))
                lista.append(str(result[2]))
                lista.append(str(result[3]))
        c.close()
        return lista

    def Localizacoes(self):
        terminal.Mensagem('Iniciando em Análise Localização', 'd')
        lista = self._Selecionar_localizacao_tweets_banco_(self._ids_tweets_localizacao)
        point = []
        cidades_validadas = []
        # Verificação do user_local
        for i in lista:
            if i!= None:
                point.append(i)

        teste = self.Validacao_cidades(point)

        for item in teste:
            self.EhCidade(item)
                # cidades_validadas.append(item)
        self.arq.Gravar_Arquivo(self.cidades_validadas, 'arquivos/data/localizacao/arquivo_localizacao.txt')
        print('Arquivo \'arquivo_localizacao.txt\' tamanho: ', len(self.cidades_validadas))
        count, encontrou, cids = 0, False, []
        cids.append(self.cidades_validadas[0])
        for item in self.cidades_validadas:
            for cidade in cids:
                if cidade == item:
                    encontrou = True
            if not encontrou:
                cids.append(item)
            encontrou = False
        print('%i Cidades Brasileiras encontradas.'%len(cids))
        cids.sort()
        print(cids)

    def Carregar_arq_controle_cidades(self):
        for linha in self.arquivo:
            linhas = linha.split(',')
            self.arq_controle_cidades.update({linhas[0]:[int(linhas[1]),int(linhas[2])]})

    def Validacao_cidades(self, lista):
        aux = []
        sinais = ['.',',','?','!','-',':',';','...','(',')','[',']','{','}', '&', '*','``','“', "''",'…']
        numeros = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        count_num = 0
        count_pont = 0
        sinal = ''
        for local in lista:
            # contem numeros - para coordenadas
            for caract in local:
                for num in numeros:
                    if caract == num:
                        count_num +=1
                for pontuacao in sinais:
                    if caract == pontuacao:
                        sinal = pontuacao
                        count_pont +=1
            if (count_pont == 0 & count_num == 0):
                aux.append(local)
                count_num = 0
            if count_pont > 0:
                locais = local.split(sinal)
                for l in locais:
                    aux.append(l)
                count_pont = 0
        return aux

    def EhCidade(self, localidade):
        result = False
        loc = self.analise.Remocao_acentuacao(localidade)
        loc = self.analise.Remocao_caracteres_Tweets(loc)
        if type(loc) == list:
            loc = self.AgregarListas(loc)
            if loc[0] == '':
                return False
            local = loc[0]
        else:
            local = local.upper()

        space2 = re.compile(r'\B\s+')
        local = re.sub(space2, '', local)
        # local = loc[0]
        local = local.upper()
        letra = local[0]        
        inicio = self.arq_controle_cidades[letra][0]
        fim = self.arq_controle_cidades[letra][1]
        i= inicio
        while i < fim:
            city = self.cidades[i-1].split(',')
            cidade = city[0]
            if local == cidade:
                self.cidades_validadas.append(cidade)
                result = True
                break
            i +=1
        return result