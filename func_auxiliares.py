import numpy as np
from elm import ELM
from Candle import candle
from func_aux_pso import *
from sistema_ativos import Ativo
#from IO import *
import os
import matplotlib.pyplot as plt
from kelm import KELM
from datetime import datetime, timedelta
import copy		

def dividir_dados(dados,delay):
	train_data = np.empty(shape = [0, delay])
	test_data = np.empty(shape = [0,delay])
	train_saida = np.empty(shape = [0, 1])
	num_instacias = len(dados)-delay

	for i in range(num_instacias):
		aux = np.copy(dados[i:(i+delay)])
		train_data = np.append(train_data, [aux], axis=0)
		train_saida = np.append(train_saida,dados[i+delay])
	#print(delay)
	#print(dados)
	#print(dados[num_instacias:len(dados)])
	test_data = np.append(test_data,[dados[num_instacias:len(dados)]],axis=0)
	
	return (train_data,train_saida,test_data)

def definir_mat_elm(a_delay,a_neurons):
	a_elm = list()
	num_ativos = len(a_delay)
	num_ind = len(a_delay[0])
	for i in range(num_ativos):
		aux = list()
		for j in range(num_ind):
			#print(a_delay[i][j],a_neurons[i][j])
			el = ELM(int(a_delay[i][j]),int(a_neurons[i][j]))
			#el = ELM(3,50)
			aux.append(el)
		a_elm.append(aux)
		del aux
	return a_elm

def definir_mat_kelm(array_c,num_ativos,param = None,tipo = None):
	a_elm = list()
	num_ind = 4
	for i in range(num_ativos):
		aux = list()
		for j in range(num_ind):
			if tipo == None:
				el = KELM(array_c[j])
				aux.append(el)
			else:
				el = KELM(array_c[j],'R',tipo,param[j])
				aux.append(el)
		a_elm.append(aux)
		del aux
	return a_elm

def criar_candle(dados1,dados2,dados3,dados4,delay,el,nome_ativo,j):
	dados = [dados1,dados2,dados3,dados4]
	predicoes = list()

	for i in range(4):
		in_train,out_train,test_dados = dividir_dados(dados[i],delay[i])
		el[i].train(in_train,out_train)
		result  = el[i].test(test_dados)
		predicoes.append(result)
		del in_train
		del out_train
		del test_dados

	x_sol,ps = func_CPSO(nome_ativo,predicoes,j)

	cand = candle(x_sol[0],x_sol[1],x_sol[2],x_sol[3],predicoes[0],predicoes[1],predicoes[2],predicoes[3],ps)
	return cand

def processamento(caminho,indicadores,delay,elm_instancias,num_rodadas):
	num_ativos = len(caminho)

	at = Ativo(num_rodadas)
	
	for j in range(num_rodadas):
		for i in range(num_ativos):
			lista_dados = list()
			for ind in indicadores:
				aux = caminho[i]+"/"+ind
				x = ler_dados_arq(aux)
				lista_dados.append(x)
				del x
			nome_ativo = pegar_nome_ativo(caminho[i])
			cand = criar_candle(lista_dados[0],lista_dados[1],lista_dados[2],lista_dados[3],delay[i],elm_instancias[i],nome_ativo,j)
			at.inserir_teste_ativo(nome_ativo,cand)

	return at

def predicao(num_rodadas=5):
	caminhos = [os.path.join('../historico', nome) for nome in os.listdir('../historico')]
	arquivos = files_path09('../parametros/')
	indicador = ["Variacao_relativa_valores.txt","Preco_Tipico_valores.txt","Kni_Indicator_valores.txt","Variacao_valores.txt"]
	tam = len(caminhos)

	params_delay,params_janela,params_neurons = ler_params(arquivos,tam)
	a_elm = definir_mat_elm(params_delay,params_neurons)
	at = processamento(caminhos,indicador,params_delay,a_elm,num_rodadas)

	registrar_resultados(at)
	#registrar_resultados_elm(at)

	for i in range(at.num_rodadas):
		#writer.writerow('rodada '+str(i))
		for keys,values in at.conj_ativo.items():
			list_aux = [keys]
			#print(list_aux+values[i].retornar_valor_elm())
			print(list_aux+values[i].retornar_valores())
		i = i+1


def grafico(fit_a,nome_ativo):
	x = range(1,(len(fit_a)+1))
	plt.plot(x,fit_a)
	plt.set_title(nome_ativo)
	plt.savefig('graficos/'+nome_ativo)
	#plt.show()

def norm(serie):
	max_valor = np.amax(serie)
	min_valor = np.amin(serie)

	for i in range(len(serie)):
		v = (serie[i]-min_valor)/(max_valor-min_valor)

		serie[i] = np.copy(v)

	return (serie,min_valor,max_valor)

def norm_mean_std(serie):
	media = np.mean(serie)
	std = np.std(serie)
	for i in range(len(serie)):
		v = (serie[i]-media)/std

		serie[i] = np.copy(v)

	return (serie,media,std)

def des_norm(min_v,max_v,x):
	return ((max_v-min_v)*x)+min_v


