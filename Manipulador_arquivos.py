# -*- coding: utf-8 -*-
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
import unicodedata
from interface import interface_terminal as terminal

class Arquivo():
    def Carregar_Arquivo(self, nome_arquivo):
        """
        Cria um manipulador de arquivo no modo leitura ('r') e retorna uma string do arquivo lido.

        :parametro nome_arquivo: nome do arquivo de a ser lido.
        """
        texto = []
        # ler arquivo
        arq = open(nome_arquivo, 'r')
        # Carrega no vetor
        for i in arq:
            i = i.rstrip()
            texto.append(i)
        # fechar arquivo
        arq.close()
        return texto
    
    def Gravar_Arquivo(self, lista, nome_arquivo):
        """
        Cria um manipulador de arquivo no modo escrita ('a') e salva um arquivo com o nome escolhido no parametro com os dados da lista.
        Este modo de escrita verifica se há o arquivo no diretório: 
        Se verdadeiro sobregrava, se falso cria o arquivo.

        :parametro lista: dados em formato de lista para gravar no arquivo.
        :parametro nome_arquivo: nome do arquivo de a ser gravado / escrito.
        """
        try:
            arq = open(nome_arquivo, 'a', encoding="utf-8")
            for linha in lista:
                if type(linha) == tuple:
                    arq.write(str(linha[0]) + ',' + str(linha[1]) + ';\n')
                else:
                    arq.write(linha + '\n')
            arq.close()
            terminal.Mensagem('Arquivo Gravado com Sucesso!', 'ok')
        except Exception as identifier:
            terminal.Mensagem('Erro (' + str(identifier) + ') ao tentar gravar o Arquivo!','e')

    def Carregar_Arquivo_UTF8(self, nome_arquivo):
        """
        Cria um manipulador de arquivo no modo leitura ('r') e retorna uma string do arquivo lido.

        :parametro nome_arquivo: nome do arquivo de a ser lido.
        """
        texto = []
        # ler arquivo
        arq = open(nome_arquivo, 'r', encoding='utf-8')
        # Carrega no vetor
        for i in arq:
            i = i.rstrip()
            texto += [i]
        # fechar arquivo
        arq.close()
        return texto

    