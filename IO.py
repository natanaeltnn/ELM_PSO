import numpy as np
from sistema_ativos import Ativo
#from func_auxiliares import *
import csv
import os
import locale
import codecs
import copy
from datetime import datetime,timedelta


def create_folder(directory):
	if not os.path.exists(directory):
		os.makedirs(directory)

def ler_dados_arq(caminho):
	arq = open(caminho,"r")
	l = list()
	linha = arq.readline()

	while linha:
		l.append(float(linha))
		linha = arq.readline()
	arq.close()
	return l


def pegar_nome_ativo(caminho):
	tam  = len(caminho)-1

	while caminho[tam] != '\\':
		tam = tam-1
	return caminho[tam+1:]


def get_limites(caminho):
	arq  = ler_dados_arq(caminho)

	maximo = max(arq)
	minimo = min(arq)
	minimo -= 0.2*minimo
	maximo += 0.2*maximo
	
	return (minimo,maximo)

def csv_to_list(arq):
	l = list()
	csvReader = csv.reader(codecs.open(arq+'.csv', 'rU', 'utf-8'),delimiter=';')

	for row in csvReader:
		l.append(row)
	return l

def search(nome_ativo,l):
	for aux in l:
		if aux[0] == nome_ativo:
			return aux[1:]
	return NULL


def lendo_bloco(num_linha,x):
	num_linha+=1
	d = x[num_linha]
	#print(d)
	num_linha+=1
	n = x[num_linha]
	num_linha+=1
	num_linha+=1
	j = x[num_linha]
	num_linha+=3

	return (d,n,j,num_linha)

def ler_params(args,num_ativos):
	params_delay = np.zeros((num_ativos,4), dtype=int)
	params_neurons =  np.zeros((num_ativos,4), dtype=int)
	params_janela = np.zeros((num_ativos,4), dtype=int)
	path = '../parametros/'
	cont = 0
	
	for arg in args:
		print(arg)
		arq = open(path+arg,"r")
		l = list()
		x = arq.read().splitlines()
		#print(x)
		arq.close()
		linha = 0
		for i in range(num_ativos):
			d,n,j,linha = lendo_bloco(linha,x)
			params_delay[i][cont] = d
			params_janela[i][cont] = j
			params_neurons[i][cont] = n
		cont+=1

	return (params_delay,params_janela,params_neurons)

def ler_params_with_lag(args,num_ativos,lag):
	params_delay = np.zeros((num_ativos,4), dtype=int)
	params_neurons =  np.zeros((num_ativos,4), dtype=int)
	params_janela = np.zeros((num_ativos,4), dtype=int)
	path = '../parametros/'
	cont = 0
	for arg in args:
		print(arg)
		arq = open(path+arg,"r")
		l = list()
		x = arq.read().splitlines()
		#print(x)
		arq.close()
		linha = 0
		for i in range(num_ativos):
			d,n,j,linha = lendo_bloco(linha,x)
			params_delay[i][cont] = lag[i][cont]
			params_janela[i][cont] = j
			params_neurons[i][cont] = n
		cont+=1

	return (params_delay,params_janela,params_neurons)

def MAPE(real,pred):
	return (abs((real - pred))/(real+0.000001))*100

def MAPE_completo(predito, real):
	erro = list()

	for i in range(len(predito)):
		aux = list()

		for j in range(1,5):
			valor = float(predito[i][j].replace(',','.'))
			valor_real = float(real[i][j-1])

			aux.append(str(MAPE(valor_real,valor)).replace('.',',')[0:7])
		erro.append(aux)
		del aux
	return erro

def files_path09(path):
	'''return list of tuple(path, file)'''
	return [file for p, _, files in os.walk(os.path.abspath(path)) for file in files]

def registrar_resultados(at,nome_arq,dia):
	#f = open('resultados.csv','w')
	#writer = csv.Writer(f, delimiter=';')
	#reais = csv_to_list('../min_max/'+dia)
	locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
	csv.register_dialect('myDialect',delimiter = ';',quoting=csv.QUOTE_NONE,skipinitialspace=True)
   
	with open(nome_arq+'-com_pesos_elm.csv', 'w') as csvFile:
		writer = csv.writer(csvFile,dialect='myDialect')
		for i in range(at.num_rodadas):
			writer.writerow(["rodada "+str(i)])
			for keys,values in at.conj_ativo.items():
				list_aux = [keys]
				#l = search(keys,reais)
				aux = values[i].retornar_valores()
				res = list()
				'''res.append(aux[0])
				res.append(aux[1])
				res.append(aux[2])
				res.append(aux[3])'''
				res.append(locale.currency(aux[0], grouping=True, symbol=None))
				res.append(locale.currency(aux[1], grouping=True, symbol=None))
				res.append(locale.currency(aux[2], grouping=True, symbol=None))
				res.append(locale.currency(aux[3], grouping=True, symbol=None))
				res.append(aux[4])
				'''res.append(" ")
				res.append(locale.currency(float(l[0]), grouping=True, symbol=None))
				res.append(locale.currency(float(l[1]), grouping=True, symbol=None))
				res.append(locale.currency(float(l[2]), grouping=True, symbol=None))
				res.append(locale.currency(float(l[3]), grouping=True, symbol=None))'''

				writer.writerow(list_aux+res)
	csvFile.close()


def registrar_resultados_elm(at,nome_arq,dia):
	#f = open('resultados.csv','w')
	#writer = csv.Writer(f, delimiter=';')
	reais = csv_to_list('../real/'+dia)
	locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
	csv.register_dialect('myDialect',delimiter = ';',quoting=csv.QUOTE_NONE,skipinitialspace=True)

	with open(nome_arq+'.csv', 'w') as csvFile:
		writer = csv.writer(csvFile,dialect='myDialect')
		for i in range(1):
			writer.writerow(["rodada "+str(i)])
			j = 0
			for keys,values in at.conj_ativo.items():
				list_aux = [keys]
				aux = values[i].retornar_valor_elm()
				res = list()
				res.append(aux[0][0])
				res.append(aux[1][0])
				res.append(aux[2][0])
				res.append(aux[3][0])
				res.append(" ")
				res.append(reais[j][0])
				res.append(reais[j][1])
				res.append(reais[j][2])
				res.append(reais[j][3])
				res.append(" ")
				res.append(locale.currency(MAPE(float(reais[j][0]),float(aux[0][0])), grouping=True, symbol=None))
				res.append(locale.currency(MAPE(float(reais[j][1]),float(aux[1][0])), grouping=True, symbol=None))
				res.append(locale.currency(MAPE(float(reais[j][2]),float(aux[2][0])), grouping=True, symbol=None))
				res.append(locale.currency(MAPE(float(reais[j][3]),float(aux[3][0])), grouping=True, symbol=None))

				j +=1
				writer.writerow(list_aux+res)
	csvFile.close()

def split_date(dat):
	print(dat)
	d = copy.copy(dat[0:2])

	if d[1] == '-':
		d = '0'+d[0]
	m = copy.copy(dat[2:])

	return (d,m)

def lista_dias(N,data):
	historico = [nome for nome in os.listdir('../historico3')]
	l = list()
	ctd = 0
	ano = str(datetime.today().year)
	day,month = split_date(data)

	if month[0] == '-':
		month = month[1:]

	d_completa = ano+'-'+month+'-'+day
	print(ano)
	print(month)
	print(day)

	#print(d_completa)
	data_pred = datetime.strptime(d_completa, '%Y-%m-%d')

	print(type(day))

	while(len(l) < N):
		ctd = ctd+1
		date_N_days_ago = data_pred - timedelta(days=ctd)

		if not date_N_days_ago.weekday() == 5 and not date_N_days_ago.weekday() == 6:
			dia = str(date_N_days_ago.day)
			mes = str(date_N_days_ago.month)

			data = dia+'-'+mes

			if data in historico:
				l.append(data)

	return l

def delete_vazio(estimado):
	lista = list()

	for aux in estimado:
		if not aux == [] and not aux[0] == 'Ativo':
			lista.append(copy.copy(aux))
	return lista

def mean_N_dias(dia,n,tam,nome_arq,opcao):
	l_dias  = lista_dias(tam,dia)
	m_mape = np.zeros((n,3))
	for d in l_dias:
		print(d)
		real = csv_to_list('../real/'+d)
		predito = csv_to_list(nome_arq+d)
		predito = delete_vazio(predito)

		if opcao == 1:
			predito = predito[5:8]

			if len(real) > 3:
				real = real[5:8]
			else:
				real = real
		elif opcao == 2:
			predito = predito[0:5]+predito[8:]
			real = real[0:5]+real[8:]
		
		for i in range(len(predito)):

			fechamento = predito[i][2].replace(',','.',1)
			maximo = predito[i][3].replace(',','.',1)
			minimo = predito[i][4].replace(',','.',1)

			m_mape[i][1] = m_mape[i][0] + MAPE(float(real[i][0]),float(fechamento))
			m_mape[i][2] = m_mape[i][1] + MAPE(float(real[i][1]),float(maximo))
			m_mape[i][3] = m_mape[i][2] + MAPE(float(real[i][2]),float(minimo))

	m_mape = m_mape/tam

	return m_mape

def registrar_best(X,nome_arq,dia,num_rodadas,opcao,media= True):
	locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
	csv.register_dialect('myDialect',delimiter = ';',quoting=csv.QUOTE_NONE,skipinitialspace=True)
	tam = len(X)
	medias = 0
	ultimo = 0

	if media:
		medias  = mean_N_dias(dia,tam,num_rodadas,'Predicoes/completo_',opcao)
		ultimo = mean_N_dias(dia,tam,1,'Predicoes/completo_',opcao)
   
	with open(nome_arq+'.csv', 'w') as csvFile:
		writer = csv.writer(csvFile,dialect='myDialect')
		for i in range(1):
			for j in range(tam):
				list_aux = [X[j][0]]
				
				aux = X[j][1].retornar_valores()
				res = list()

				res.append(str(aux[0]).replace('.',',')[0:5])
				res.append(str(aux[1]).replace('.',',')[0:5])
				res.append(str(aux[2]).replace('.',',')[0:5])
				res.append(str(aux[3]).replace('.',',')[0:5])
				res.append(" ")
				res.append(aux[4])

				res.append(" ")
				
				if media:
					for k in range(3):
						res.append(str(medias[j][k]).replace('.',',')[0:5])
					res.append(" ")
					for k in range(3):
						res.append(str(ultimo[j][k]).replace('.',',')[0:5])


				writer.writerow(list_aux+res)
	csvFile.close()

def unir_best(X,dia,num_rodadas,opcao,media = True):
	csv.register_dialect('myDialect',delimiter = ';',quoting=csv.QUOTE_NONE,skipinitialspace=True)
	tam = len(X)
	medias = 0
	ultimo = 0

	if media:
		medias  = mean_N_dias(dia,tam,num_rodadas,'Predicoes/completo_',opcao)
		ultimo = mean_N_dias(dia,tam,1,'Predicoes/completo_',opcao)

	dol_ind = csv_to_list('Predicoes/dol_ind_'+dia)
	completo = list()
	with open('Predicoes/completo_'+dia+'.csv', 'w') as csvFile:
		writer = csv.writer(csvFile,dialect='myDialect')
		writer.writerow(['Ativo','Open','Close','High','Low',' ','Fit',' ','Close err medio',
		'High err medio','Low err medio',' ','Close err','High err','Low err'])
		for i in range(1):
			for j in range(tam):

				list_aux = [X[j][0]]

				aux = X[j][1].retornar_valores()
				res = list()

				res.append(str(aux[0]).replace('.',','))
				res.append(str(aux[1]).replace('.',',')[0:5])
				res.append(str(aux[2]).replace('.',',')[0:5])
				res.append(str(aux[3]).replace('.',',')[0:5])
				res.append(" ")
				res.append(aux[4])

				if media:

					res.append(" ")
					
					for k in range(3):
						res.append(str(medias[j][k]).replace('.',',')[0:5])
					
					res.append(" ")
					
					for k in range(3):
						res.append(str(ultimo[j][k]).replace('.',',')[0:5])

				completo.append(list_aux+res)
		dol_ind = delete_vazio(dol_ind)
		completo = completo[0:5] + dol_ind + completo[5:]

		for i in range(len(completo)):
			writer.writerow(completo[i])
	csvFile.close()

def registrar_elm(X,nome_arq,dia,opcao):
	locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
	csv.register_dialect('myDialect',delimiter = ';',quoting=csv.QUOTE_NONE,skipinitialspace=True)
	tam = len(X)
   
	with open(nome_arq+'.csv', 'w') as csvFile:
		writer = csv.writer(csvFile,dialect='myDialect')
		for i in range(1):
			for j in range(tam):
				list_aux = [X[j][0]]
				
				aux = X[j][1].retornar_valor_elm()
				res = list()

				res.append(str(aux[0]).replace('.',',')[0:7])
				res.append(str(aux[1]).replace('.',',')[0:7])
				res.append(str(aux[2]).replace('.',',')[0:7])
				res.append(str(aux[3]).replace('.',',')[0:7])

				writer.writerow(list_aux+res)
	csvFile.close()


def unir_elm(X,dia,opcao):
	csv.register_dialect('myDialect',delimiter = ';',quoting=csv.QUOTE_NONE,skipinitialspace=True)
	tam = len(X)
	dol_ind = csv_to_list('Predicoes/dol_ind_elm_'+dia)
	ind_real = csv_to_list('../real/IND_'+dia)
	completo = list()
	with open('Predicoes/completo_elm2_'+dia+'.csv', 'w') as csvFile:
		writer = csv.writer(csvFile,dialect='myDialect')

		for i in range(1):
			for j in range(tam):

				list_aux = [X[j][0]]

				aux = X[j][1].retornar_valor_elm()
				res = list()

				res.append(str(aux[0]).replace('.',','))
				res.append(str(aux[1]).replace('.',',')[0:5])
				res.append(str(aux[2]).replace('.',',')[0:5])
				res.append(str(aux[3]).replace('.',',')[0:5])

				res.append(" ")
				

				completo.append(list_aux+res)
		dol_ind = delete_vazio(dol_ind)
		completo = completo[0:5] + dol_ind + completo[5:]

		erro = MAPE_completo(completo,ind_real)

		for i in range(len(completo)):
			linha = completo[i]+erro[i]
			writer.writerow(linha)
	csvFile.close()
