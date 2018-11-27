#from elm import ELM
from func_auxiliares import *
from sistema_ativos import Ativo
from func_aux_pso import *
from statsmodels.tsa.stattools import acf
from IO import *
import os
import sys
import datetime
import time
from predicao_ind import do_prediction,param_ret
from predicao_ind import do_prediction
from predicao_ind import registrar
from predicao_ind import param_ret
from nova_main import transform
from nova_main import search_ativo


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

def Diff(li1, li2): 
	return (list(set(li1) - set(li2))) 

if __name__ == '__main__':
	num_rodadas = 5
	#datass = [nome for nome in os.listdir('../historico_horario')]
	num_ativos  = 12
	nome_ativo = ""
	num_alcancado = 0
	datas = [sys.argv[1]]
	matrix_pred = csv_to_list('Predicoes/elm_semanal_'+datas[0])

	matrix_pred = transform(matrix_pred)
	print(datas)
	indicador = ["Variacao_relativa_valores.txt","Preco_Tipico_valores.txt","Kni_Indicator_valores.txt","Variacao_valores.txt"]

	for dia in datas:

		at = Ativo(num_rodadas)
		print(dia)
		old = [nome for nome in os.listdir('../Open/'+dia+"-semanal")]
		original = copy.copy(old)
		new = []
		while num_alcancado < num_ativos:

			for nova_acao in old:
				pred_values = do_prediction('../historico_semanal/',2)
				print(nova_acao)
				nome = nova_acao

				i = search_ativo(matrix_pred,nome)

				nome_ativo = matrix_pred[i][0]
				print(nome_ativo)
				predicoes = copy.copy(matrix_pred[i][1:])

				print(nome_ativo)
				predicoes = copy.copy(pred_values[0][1:])

				for i in range(num_rodadas):
					x_sol,ps,op = func_CPSO(nome_ativo,predicoes,i,dia,2)
					cand = candle(op,x_sol[0],x_sol[1],x_sol[2],predicoes[0],predicoes[1],predicoes[2],predicoes[3],ps)
					at.inserir_teste_ativo(nova_acao,cand)
				num_alcancado = num_alcancado+1
				print('num_alcancado: ',num_alcancado)

			if not old == []:

				print('calcula o best')
				best_pred = at.best()
				print('escreve o best')
				registrar_best(best_pred,'Predicoes/pred_semanal_'+dia,dia,num_rodadas,-1,media=False)

			original = original+new
			new = [nome for nome in os.listdir('../Open/'+dia+"-semanal")]
			new = Diff(new,original)
			old = copy.copy(Diff(new,old))	
			time.sleep(5)
