#from elm import ELM
from func_auxiliares import *
from sistema_ativos import Ativo
from func_aux_pso import *
from statsmodels.tsa.stattools import acf
from IO import *
import os
import sys
import datetime
import glob
import time
from predicao_ind import do_prediction,param_ret

def split_path(op,caminhos):
	if op == 1:

		if len(caminhos) > 3:
			return caminhos[5:8]
		else:
			return caminhos
	elif op == 2:
		return caminhos[0:5]+caminhos[8:]
	elif op == 3:
		return caminhos

def transform(X):
	X = delete_vazio(X)
	Y = copy.copy(X)

	for i  in range(len(X)):
		for j in range(1,5):
			Y[i][j] = float(X[i][j].replace(',','.'))

	return Y

def Diff(li1, li2): 
    return (list(set(li1) - set(li2))) 

def search_ativo(matrix,ativo):
	for i in range(len(matrix)):
		if matrix[i][0] == ativo:
			return i
	return -1


def unir(X,dia,num_rodadas,media):
	csv.register_dialect('myDialect',delimiter = ';',quoting=csv.QUOTE_NONE,skipinitialspace=True)
	tam = len(X)

	dol_ind = csv_to_list('Predicoes/dol_ind_'+dia)
	completo = list()
	with open('Predicoes/completo_'+dia+'.csv', 'w') as csvFile:
		writer = csv.writer(csvFile,dialect='myDialect')

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

				completo.append(list_aux+res)
		dol_ind = delete_vazio(dol_ind)
		completo = completo[0:5] + dol_ind + completo[5:]

		for i in range(len(completo)):
			writer.writerow(completo[i])
	csvFile.close()


if __name__ == '__main__':
	num_rodadas = 5
	datass = [nome for nome in os.listdir('../historico3')]
	num_ativos  = 15
	nome_ativo = ""
	num_alcancado = 0
	print(datass)
	print(len(datass))
	datas = [sys.argv[1]]
	matrix_pred = csv_to_list('Predicoes/elm_'+datas[0])

	matrix_pred = transform(matrix_pred)

	print(datas)
	indicador = ["Variacao_relativa_valores.txt","Preco_Tipico_valores.txt","Kni_Indicator_valores.txt","Variacao_valores.txt"]

	for dia in datas:

		at = Ativo(num_rodadas)
		print(dia)
		#old = []

		#while(old == []):
		old = [nome for nome in os.listdir('../Open/'+dia)] 
		
		original = copy.copy(old)
		new = []
		while num_alcancado < num_ativos:

			for nova_acao in old:
				print(nova_acao)

				nome = nova_acao

				i = search_ativo(matrix_pred,nome)

				nome_ativo = matrix_pred[i][0]
				print(nome_ativo)
				predicoes = copy.copy(matrix_pred[i][1:])

				for i in range(num_rodadas):
					x_sol,ps,op = func_CPSO(nome_ativo,predicoes,i,dia)
					cand = candle(op,x_sol[0],x_sol[1],x_sol[2],predicoes[0],predicoes[1],predicoes[2],predicoes[3],ps)
					at.inserir_teste_ativo(nome_ativo,cand)
				num_alcancado = num_alcancado+1
				print('num_alcancado: ',num_alcancado)

			if not old == []:

				print('calcula o best')
				best_pred = at.best()
				print('escreve o best')
				registrar_best(best_pred,'Predicoes/completo_'+dia,dia,num_rodadas,-1,media=False)

			original = original+new
			new = [nome for nome in os.listdir('../Open/'+dia)]
			new = Diff(new,original)
			old = copy.copy(Diff(new,old))	
			time.sleep(5)
