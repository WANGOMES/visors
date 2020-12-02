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

from time import sleep

class interface_terminal():
    
    def Mensagem(mensagem, tipo):
        """
        :parametro: mensagem: texto que será exibido na mensagem no terminal
        :parametro: tipo: tipo de mensagem sendo 'D'-Destaque | 'S'-Simples | 'OK'-Success | 'W'-Warning | 'E'-Error | 'T'-Title
        """
        tipo = tipo.lower()
        t = ' * '
        cor = {'s': '\033[37m',
                'd': '\033[33m',
                'ok': '\033[32m',
                't': '\033[32m',
                'w': '\033[33m',
                'e': '\033[31m',
                'dd': '\033[1;30;47m'}
        AUX = cor['s']
        interno = ''
        quant = 3
        for color in cor.keys():
            if tipo == color:
                AUX = cor[color]
                interno = cor[color]
                if color == 'd':
                    interno = cor['dd']
                    quant = 5
                    t = ' x '
                if color == 't':
                    t = ''

        print(AUX + (t * quant) + '\033[0;0m' + interno + ' ' + mensagem + ' ' + '\033[0;0m' + AUX + (t * quant) + '\033[0;0m')

    def printProgressBar (iteration, total, prefix = 'Progresso:', suffix = 'Completo', decimals = 1, length = 100, fill = '█'):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        color = '\033[32m'
        color_reset = '\033[0;0m'
        sleep(0.05)
        print('\r%s%s |%s| %s%% %s %s' % (color, prefix, bar, percent, suffix, color_reset), end = '\r')
        # Print New Line on Complete
        if iteration == total: 
            print()

    def printProgressBarII(contador, prefix = 'Progresso:'):
        index = int(contador % 4)
        # if index > 3:
        #     index = 0
        bar = [' ▷  ◐ ',' ▶  ◓ ',' ▷  ◑ ',' ▶  ◒ ']
        color = '\033[32m'
        color_reset = '\033[0;0m'
        sleep(0.05)
        print('\r%s%s  %s  %s %s' % (color, prefix, contador, bar[index], color_reset), end = '\r')

    def TelaInicial(titulo, lista_menu, solicita_input=None):
        fill = ':'
        size=70
        if solicita_input == '' or solicita_input == None:
            solicita_input = '  > Escolha uma opção: '

        tamanho_titulo = len(titulo)
        mult = int((size - tamanho_titulo)/2)
        interface_terminal.Mensagem(fill*mult+titulo+fill*mult , 'T')
        print()
        pos = 1
        for item in lista_menu:
            if pos == len(lista_menu):
                print('\t%i - %s\n\t%s'%(pos, item, solicita_input), end='')
                opcao = str(input())
            else:
                print('\t%i - %s'%(pos, item))
            pos += 1
        return opcao

