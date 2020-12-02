# import programa_auxiliar as pa
# from Manipulador_arquivos import Arquivo
# import json

# arq = Arquivo()
# termos_especiais = {}
# aux = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
# for i in aux:
#     termos_especiais.update({i: None})
# t = arq.Carregar_Arquivo_UTF8('arquivos/stem_termos.txt')
# lista = []
# for key in termos_especiais.keys():
#     for item in t:
#         inicial = item[0]
#         if inicial == key:
#             lista.append(item)
#     if len(lista)==0:
#         termos_especiais[key] = None
#     else:
#         termos_especiais[key] = lista.copy()
#     lista.clear()
# lista_ids_tweets = [0, 15, 25, 250, 252, 253, 255, 256, 2000, 2558, 2559, 25589]
# aux = ''

# for item in lista_ids_tweets:
#     if item != lista_ids_tweets[-1]:
#         aux += 'id=%i OR '%(item +609)
#     else:
#         aux += 'id=%i'%(item +609)
# query = "SELECT user_local, geo, coordinates, place, tweet FROM `selecionados_notrt_tb` WHERE %s"%aux

# print(query)
# print(lista_ids_tweets[2:])
'''
USAR ESTE
'''
# import psutil
# # Processos
# procs = {p.pid: p.info for p in psutil.process_iter(['name', 'username'])}
# # Sensores
# # # Temperatura
# psutil.sensors_temperatures()
# # # Bateria
# def secs2hours(secs):
#     mm, ss = divmod(secs, 60)
#     hh, mm = divmod(mm, 60)
#     return "%d:%02d:%02d" % (hh, mm, ss)

# battery = psutil.sensors_battery()
# print("charge = %s%%, time left = %s" % (battery.percent, secs2hours(battery.secsleft)))

# # # Velocidade dos ventiladores
# psutil.sensors_fans()
# # Disco
# psutil.disk_io_counters(perdisk=True) # Disco: Gravações e leituras
# psutil.disk_usage('/') # Disco em uso
# # Memoria
# mem = psutil.virtual_memory()
# THRESHOLD = 100 * 1024 * 1024  # 100MB
# if mem.available <= THRESHOLD:
#     print("warning")

# # CPU
# psutil.cpu_count()
# psutil.cpu_stats()
# psutil.cpu_percent(interval=None)
# psutil.cpu_times()
# psutil.cpu_freq()
# [x / psutil.cpu_count() * 100 for x in psutil.getloadavg()] # a carga média do sistema

# # Processos
# for proc in psutil.process_iter(['pid', 'name', 'username']):
#     print(proc.info)
# psutil.pids()
# p = psutil.Process()
# p.io_counters() # Contadores
# p.cpu_times()
# sum(p.cpu_times()[:2])  # cumulative, excluding children and iowait
# p.cpu_percent(interval=None) 
# p.cpu_affinity()
# p.memory_info()
# p.memory_full_info()
'''
USAR ESTE
'''
# from lsa import Latent_Semantic_Analysis as lsa

# print(lsa)

# import re
# teste = ['o tal apetite da minha mente vai acabar matando a fome do meu bolso',
#         'deu meia noite e ela chegou a fome',
#         'pensando tanto em comer que perdi a fome',
#         'q fome do crl porem preguica d ir na cozinha',
#         'ai como to com fome', 'estou com uma fome', 'sempre com muita fome']

# fome_lista = [r'to com fome', r'estou com fome', r'muita fome', r'chegou a fome', r'perdi a fome']
# pos = 0
# posicao = []
# for item in teste:
#     for ter in fome_lista:
#         e = re.compile(ter)
#         tweets = re.findall(e, item)
#         if len(tweets) != 0:
#             posicao.append(pos)
#             break
#     pos+=1
# print(posicao)
# for p in posicao:
#     print(teste[p])

# teste = {}
# for i in range(100):
#     teste.update({i: i})

# [print(teste[t]) for t in teste.keys() if t < 20 ]
# [print(teste[t]) for t in teste.keys() if t > len(teste)-20 ]
# # print(teste[:-20])
'''
esse
'''

# import json

# dicts, teste = {}, {}
# with open( 'arquivos/data/lsa/feature_topicos.json' , 'r', encoding='utf8') as json_file:
#     dicts = json.load(json_file)

# # pos = 0
# # for item in dicts.keys():
# #     pos +=1
# #     if pos == 1594:
# #         print(item, dicts[item])

# # for item in dicts.keys():
# #     for i in dicts[item].keys():
# #         # try:
#         #     x = dicts[item][i]['vulnerabilidade']
#         # except KeyError as identifier:
#         # dicts[item][i].update({'vulnerabilidade': None})

# # lista = dicts['0'].keys()
# # [print(l) for l in lista]

# # maior_75_1, menor_75_1, maior_75_0, menor_75_0 = 0,0,0,0
# # maior_75_none, menor_75_none = 0,0
# for topico in dicts.keys():
#     teste.update(dicts[topico])
# #     for _id in dicts[topico].keys():
# #         if dicts[topico][_id]['score']>= 0.75 and dicts[topico][_id]['vulnerabilidade'] != None:
# #             if dicts[topico][_id]['vulnerabilidade'] > 0.0:
# #                 maior_75_1 += 1
# #             elif dicts[topico][_id]['vulnerabilidade'] == 0.0:
# #                 maior_75_0 += 1
# #         elif dicts[topico][_id]['score']>= 0.75 and dicts[topico][_id]['vulnerabilidade'] == None:
# #             maior_75_none += 1
# #         elif dicts[topico][_id]['score']< 0.75 and dicts[topico][_id]['vulnerabilidade'] != None:
# #             if dicts[topico][_id]['vulnerabilidade'] > 0.0:
# #                 menor_75_1 += 1
# #             elif dicts[topico][_id]['vulnerabilidade'] == 0.0:
# #                 menor_75_0 += 1
# #         else:
# #             menor_75_none += 1
# # soma = maior_75_1 + maior_75_0 + menor_75_1 + menor_75_0 + maior_75_none + menor_75_none
# # soma_maior = maior_75_none + maior_75_1 + maior_75_0
# # soma_menor = menor_75_none + menor_75_1 + menor_75_0
# # perc_treino_maior = maior_75_1/(maior_75_1 + maior_75_0)
# # perc_treino_menor = menor_75_1 / (menor_75_1 + menor_75_0)
# # print('Score > 0.75 e Vulnerabilidade = 1.0: {:<5} Score > 0.75 e Vulnerabilidade = 0.0: {:<5} Score > 0.75 e Vulnerabilidade = None: {:<5}Estimativa Vulnerabilidade TRUE: {:<5.2f}\nScore < 0.75 e Vulnerabilidade = 1.0: {:<5} Score < 0.75 e Vulnerabilidade = 0.0: {:<5} Score < 0.75 e Vulnerabilidade = None: {:<5}Estimativa Vulnerabilidade TRUE: {:<5.2f}\n\tSoma: {:<5}'
# #         .format(maior_75_1,maior_75_0, maior_75_none, (soma_maior* perc_treino_maior), menor_75_1, menor_75_0, menor_75_none,(soma_menor*perc_treino_menor) ,soma))

# with open('arquivos/data/lsa/feature_teste.json', 'w', encoding='utf-8') as json_file:
#     json.dump(teste, json_file, indent=4, ensure_ascii=False)
'''
esse
'''
# with open('arquivos/data/lsa/feature_topicos.json', 'w', encoding='utf-8') as json_file:
    # json.dump(teste, json_file, indent=4, ensure_ascii=False)

# words = ['1 - o tal apetite da minha mente vai acabar matando a fome do meu bolso',
#         '2- deu meia noite e ela chegou a fome',
#         '3 - pensando tanto em comer que perdi a fome',
#         '4 - q fome do crl porem preguica d ir na cozinha',
#         '5 - ai como to com fome', '6 - estou com uma fome', '7 - sempre com muita fome']

# treino = int(len(words)*0.6)
# print(len(words))
# print(words[:treino], len(words[:treino]))
# print(words[treino:], len(words[treino:]))

def __Somatorio__(*args):
    soma = 0
    for item in args:
        soma += item
    return soma


# soma = __Somatorio__(2,2,5,5,125,5)
# print(soma)

# print('\n *** BASE DE DADOS TWEETS ETIQUETADOS COMO VULNERABILIDADE OU RISCO SOCIAL *** \n  Vulnerabilidade Social = 1.0: {:<5} | {:<10} ({:<5.2f}%)\n  Vulnerabilidade Social = 0.0: {:<5} | {:<10} ({:<5.2f}%)\n  Total de tweets: {:<7}'
#             .format(271, int(p_true)*'█',p_true, somatorio_false, int(p_false)*'█', p_false, soma))

'''
TESTAR ESSE CÓDIGO
'''
# import numpy as np
# import matplotlib.pyplot as plt

# from sklearn import svm, datasets
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import plot_confusion_matrix

# # import some data to play with
# iris = datasets.load_iris()
# X = iris.data
# y = iris.target
# class_names = iris.target_names

# # Split the data into a training set and a test set
# X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

# # Run classifier, using a model that is too regularized (C too low) to see
# # the impact on the results
# classifier = svm.SVC(kernel='linear', C=0.01).fit(X_train, y_train)

# np.set_printoptions(precision=2)

# # Plot non-normalized confusion matrix
# titles_options = [("Confusion matrix, without normalization", None),
#                   ("Normalized confusion matrix", 'true')]
# for title, normalize in titles_options:
#     disp = plot_confusion_matrix(classifier, X_test, y_test,
#                                  display_labels=class_names,
#                                  cmap=plt.cm.Blues,
#                                  normalize=normalize)
#     disp.ax_.set_title(title)

#     print(title)
#     print(disp.confusion_matrix)

# plt.show()
'''
AQUI
'''
# from sklearn.model_selection import StratifiedShuffleSplit
# import numpy as np
# def Selecao_Amostragem_Stratified_Cross_Validation(X, y, test_size=0.3, n_splits=10):
#     sss = StratifiedShuffleSplit(n_splits=n_splits, test_size=test_size, random_state=0)
#     print(sss.get_n_splits(X, y))

#     print(sss)
#     X_train, X_test, y_train, y_test = [], [], [], []

#     for train_index, test_index in sss.split(X, y):
#         print("TRAIN:", train_index, "TEST:", test_index)
#         # X_train, X_test = X[train_index], X[test_index]
#         y_train, y_test = y[train_index], y[test_index]
#         X_train.append(X[train_index])
#         X_test.append(X[test_index])
    
#     # for item in X_train:
#     print('X_train: ', X_train)

# lista = [0, 0, 0, 1, 1, 1]
# X = np.array([[1, 2], [3, 4], [1, 2], [3, 4], [1, 2], [3, 4]])
# y = np.array(lista)
# Selecao_Amostragem_Stratified_Cross_Validation(X, y,0.3, 4)
def Metodos_Amostragem(metodos_nome=list, tamanho_X_y=list):
    posicao = 0
    
    for metodo in metodos_nome:
        soma = __Somatorio__(tamanho_X_y[posicao][0], tamanho_X_y[posicao][1])
        treinamento = tamanho_X_y[posicao][0]
        teste = tamanho_X_y[posicao][1]
        p_treinamento = (treinamento/soma)*100
        p_teste = (teste/soma)*100
        print('\n \n\tMÉTODO DE AMOSTRAGEM: {:<5}\n Detalhamento das Amostras:\n  Treinamento: {:<5} | {:<10} ({:<5.2f}%)\n  Teste: {:<5} | {:<10} ({:<5.2f}%)\n  Total de tweets: {:<7}'
                    .format(metodo, treinamento, int(p_treinamento*0.4)*'█',p_treinamento, teste, int(p_teste)*'█', p_teste, soma))
        posicao +=1
met = ['HOLDOUT', 'Stratified Cross-Validation']
tam = [[2107, 527], [1685, 422]]
Metodos_Amostragem(met, tam)