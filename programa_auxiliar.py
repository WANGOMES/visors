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
from analyzer import AnaliseLexica
import json

def Base_teste_treino():
    '''
    Importante código para separar teste e treinamento de bases
    '''
    conn = pymysql.connect("localhost","root","", "tw")
    c = conn.cursor()
    arq = Arquivo()
    al = AnaliseLexica()
    nome_arquivo = 'arquivos/treinamento.csv'
    nome_arquivo1 = 'arquivos/teste.csv'

    query = "SELECT id, id_tweet, tweet FROM selecionados_notrt_tb WHERE id=4216 OR id=7319 OR id=11542 OR id=11571 OR id=11764 OR id=14300 OR id=16303 OR id=19407 OR id=19439 OR id=21363 OR id=21577 OR id=22099"
    c.execute(query)

    lista = []
    while True:
        res = c.fetchall()
        if not res:
            break
        for result in res:
            tweet = al.Remocao_caracteres_Tweets(str(result[2]))
            lista.append(str(result[0]) + ';' + str(result[1]) + ';' + str(tweet))

    # treino = int(len(lista)*0.7)

    [print(i) for i in lista]

    arq.Gravar_Arquivo(lista[:treino], nome_arquivo)
    arq.Gravar_Arquivo(lista[treino:], nome_arquivo1)

def Corrigir_Base_Dicionario(palavras):
    if type(palavras)==str:
        palavras = palavras.split()
    arq = Arquivo()
    arq.Gravar_Arquivo(palavras, 'arquivos/data/lsa/limpeza_feature_names.txt')
    print('>> Método: Corrigir_Base_Dicionario <<\nType: %s Tamanho: %i Primeira Palavra: %s Ultima Palavra: %s'%(type(palavras), len(palavras), palavras[0], palavras[-1]))

def AgregarListas(lista):
    result = []
    aux = []
    if type(lista) == list:
        for item in lista:
            if type(item) == list:
                aux = AgregarListas(item)
                result = result + aux
            else:
                result.append(item)
    else:
        result.append(lista)
    return result

def Atualiza_Dict_Termos_especiais(inicializar=False):
    '''
    Atualiza o Dicionario de Termos Especiais.
    :parametro inicializar: inicializa o Dicionário de Termos Especiais, False como Padrão.
    '''
    arq = Arquivo()
    termos_especiais = {}
    def __Inicializa_Dict():
        aux = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        for i in aux:
            termos_especiais.update({i: None})
    
    if inicializar:
        __Inicializa_Dict()

    t = arq.Carregar_Arquivo_UTF8('arquivos/data/lsa/termos_vulnerabilidade_risco_social.txt')
    lista, count = [], 0
    for key in termos_especiais.keys():
        for item in t:
            inicial = item[0]
            if inicial == key:
                count += 1
                lista.append(item)
        if len(lista)==0:
            termos_especiais[key] = None
        else:
            termos_especiais[key] = lista.copy()
        lista.clear()
    
    with open('arquivos/data/lsa/termos_especiais.json', 'w', encoding='utf-8') as json_file:
        json.dump(termos_especiais, json_file, indent=4, ensure_ascii=False)
    print('>> Método: Atualiza_Dict_Termos_especiais <<\nType: %s Arquivo: \'%s\' Tamanho: %i'%(type(termos_especiais), 'arquivos/data/lsa/termos_especiais.json', count))

def List_ToString(inicial, final):
    resp = ''
    for item in range(inicial, final):
        if item == (final - 1):
            resp += '%i'%item
        else:
            resp += '%i, '%item
    return resp

def Levantamento_Score_Vulnerabilidade():
    dicts = {}
    with open( 'arquivos/data/lsa/feature_topicos.json' , 'r', encoding='utf8') as json_file:
        dicts = json.load(json_file)

    maior_75_1, menor_75_1, maior_75_0, menor_75_0 = 0,0,0,0
    maior_75_none, menor_75_none = 0,0
    for topico in dicts.keys():
        for _id in dicts[topico].keys():
            if dicts[topico][_id]['score']>= 0.75 and dicts[topico][_id]['vulnerabilidade'] != None:
                if dicts[topico][_id]['vulnerabilidade'] > 0.0:
                    maior_75_1 += 1
                elif dicts[topico][_id]['vulnerabilidade'] == 0.0:
                    maior_75_0 += 1
            elif dicts[topico][_id]['score']>= 0.75 and dicts[topico][_id]['vulnerabilidade'] == None:
                maior_75_none += 1
            elif dicts[topico][_id]['score']< 0.75 and dicts[topico][_id]['vulnerabilidade'] != None:
                if dicts[topico][_id]['vulnerabilidade'] > 0.0:
                    menor_75_1 += 1
                elif dicts[topico][_id]['vulnerabilidade'] == 0.0:
                    menor_75_0 += 1
            else:
                menor_75_none += 1
    soma = __Somatorio__(maior_75_1, maior_75_0, menor_75_1, menor_75_0, maior_75_none, menor_75_none)
    soma_maior = __Somatorio__(maior_75_none, maior_75_1, maior_75_0)
    soma_menor = __Somatorio__(menor_75_none, menor_75_1, menor_75_0)
    perc_treino_maior = maior_75_1/__Somatorio__(maior_75_1, maior_75_0)
    perc_treino_menor = menor_75_1 / __Somatorio__(menor_75_1, menor_75_0)
    
    somatorio_true = __Somatorio__(maior_75_1, menor_75_1)
    somatorio_false = __Somatorio__(maior_75_0, menor_75_0)
    p_true = (somatorio_true/soma)*100
    p_false = (somatorio_false/soma)*100

    print('Score > 0.75 e Vulnerabilidade = 1.0: {:<5} Score > 0.75 e Vulnerabilidade = 0.0: {:<5} Score > 0.75 e Vulnerabilidade = None: {:<5}Estimativa Vulnerabilidade TRUE: {:<5.2f}\nScore < 0.75 e Vulnerabilidade = 1.0: {:<5} Score < 0.75 e Vulnerabilidade = 0.0: {:<5} Score < 0.75 e Vulnerabilidade = None: {:<5}Estimativa Vulnerabilidade TRUE: {:<5.2f}\n\tSoma: {:<5}'
            .format(maior_75_1,maior_75_0, maior_75_none, (soma_maior* perc_treino_maior), menor_75_1, menor_75_0, menor_75_none,(soma_menor*perc_treino_menor) ,soma))
    print('\n * * * * BASE DE DADOS TWEETS ETIQUETADOS COMO VULNERABILIDADE OU RISCO SOCIAL * * * * \n Vulnerabilidade Social = 1.0: {:<5} | {:<10} ({:<5.2f}%)\n Vulnerabilidade Social = 0.0: {:<5} | {:<10} ({:<5.2f}%)\n Total de tweets: {:<7}'
            .format(somatorio_true, int(p_true)*'█',p_true, somatorio_false, int(p_false*0.4)*'█', p_false, soma))

def Atualiza_Recursos_Classificador():
    dicts, teste = {}, {}
    with open( 'arquivos/data/lsa/feature_topicos.json' , 'r', encoding='utf8') as json_file:
        dicts = json.load(json_file)
    
    for topico in dicts.keys():
        teste.update(dicts[topico])
    
    with open('arquivos/data/lsa/feature_teste.json', 'w', encoding='utf-8') as json_file:
        json.dump(teste, json_file, indent=4, ensure_ascii=False)

def __Somatorio__(*args):
    soma = 0
    for item in args:
        soma += item
    return soma

def Metodos_Amostragem(metodos_nome=list, tamanho_X_y=list):
    posicao = 0
    for metodo in metodos_nome:
        soma = __Somatorio__(int(tamanho_X_y[posicao][0]), int(tamanho_X_y[posicao][1]))
        treinamento = int(tamanho_X_y[posicao][0])
        teste = int(tamanho_X_y[posicao][1])
        p_treinamento = (treinamento/soma)*100
        p_teste = (teste/soma)*100
        print('\n \n\tMÉTODO DE AMOSTRAGEM: {:<5}\n Detalhamento das Amostras:\n  Treinamento: {:<5} | {:<10} ({:<5.2f}%)\n  Teste: {:<11} | {:<10} ({:<5.2f}%)\n  Total de tweets: {:<7}'
                    .format(metodo, treinamento, int(p_treinamento*0.4)*'█',p_treinamento, teste, int(p_teste)*'█', p_teste, soma))
        posicao +=1