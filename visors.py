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
from selector import Selector
from extractor import Extractor
from interface import interface_terminal as terminal
from analyzer import AnaliseLocalização
from evaluation import Avaliacao_classificacao
from lsa import Latent_Semantic_Analysis
import os
import time
import winsound


clear = lambda: os.system('cls')

def Sinal():
    frequency = 2500  # Set Frequency To 2500 Hertz
    duration = 3000  # Set Duration To 1000 ms == 1 second
    return winsound.Beep(frequency, duration)

''' MOD I - EXTRAÇÃO '''
def Extrair():
    print('Informe o Tempo de Processamento (em segudos): ', end='')
    tempo = float(input())
    extracao = Extractor(tempo) # Faz conexão com a API do Twitter e extrai dados para banco de dados local.
    
''' MOD II - SELEÇÃO '''
def Selecionar():
    print('Informe o tipo de Consulta: C - COMPLETA | A - ATUALIZAÇÃO: ', end='')
    tipo = str(input())
    print('Informe a Data INICIAL para a Consulta [YYYY-MM-DD]: ', end='')
    data_inicio = str(input())
    print('Informe a Data FINAL para a Consulta [YYYY-MM-DD]: ', end='')
    data_final = str(input())
    selecao = Selector() #Faz a seleção do conteudo dos tweets e insere em Banco de dados.
    selecao.select(tipo, data_inicio, data_final)

''' MOD III - ANALISE '''
def Analisar():
    _lsa = Latent_Semantic_Analysis()
    analise = AnaliseLocalização()

''' MOD IV - AVALIAÇÃO '''
def Avaliar():
    avaliacao = Avaliacao_classificacao()

def Run():
    Extrair()
    Selecionar()
    Analisar()
    Avaliar()

def Continuar():
    Sinal()
    terminal.Mensagem('Deseja continuar? (S/N) ', 's')
    term = input()
    term = term.upper()
    if term != 'S':
        clear()
        return False
    else:
        clear()
        return True

opcao = ''
title = 'VISORS - VIGILANCIA SOCIOASSISTENCIAL EM REDES SOCIAIS'
lista = ['Extração de Dados','Seleção de Dados','Análise de dados','Avaliação dos Dados','AUTO-Iniciar Processo Automático','Sair']

while opcao != 'S':
    opcao = terminal.TelaInicial(title, lista)
    opcao = opcao.upper()
    if opcao == 'AUTO':
        clear()
        Run()
        if not Continuar():
            opcao = 'S'
    elif opcao == '1':
        clear()
        Extrair()
        if not Continuar():
            opcao = 'S'
    elif opcao == '2':
        clear()
        Selecionar()
        if not Continuar():
            opcao = 'S'
    elif opcao == '3':
        clear()
        Analisar()
        if not Continuar():
            opcao = 'S'
    elif opcao == '4':
        clear()
        Avaliar()
        if not Continuar():
            opcao = 'S'


terminal.Mensagem(' . . . Desconectando o VISOR . . . ', 'd')
time.sleep(4)
clear()