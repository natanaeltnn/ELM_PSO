#from elm import ELM
from func_auxiliares import *
from sistema_ativos import Ativo
from func_aux_pso import *
from statsmodels.tsa.stattools import acf
from IO import *
import os
import sys

def param_ret(op,arquivos):
	if op == 1:
		delay,_,_ = ler_params(arquivos[0:4],3)
		return (3,delay)
	elif op == 2:
		delay,_,_ = ler_params(arquivos[4:8],12)
		return (12,delay)
	elif op == 3:
		delay2,_,_ = ler_params(arquivos[0:4],3)
		delay,_,_ = ler_params(arquivos[4:8],12)
		aux = np.copy(delay[5:])
		delay =  np.concatenate((delay[0:5],delay2))
		delay = np.concatenate((delay,aux))
		return (15,delay)
	elif op == 4:
		delay,_,_ = ler_params(arquivos[8:],1)
		return (1,delay)



def registrar(X,nome_arq,dia):
	locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
	csv.register_dialect('myDialect',delimiter = ';',quoting=csv.QUOTE_NONE,skipinitialspace=True)
	tam = len(X)
   
	with open(nome_arq+'.csv', 'w') as csvFile:
		writer = csv.writer(csvFile,dialect='myDialect')
		for i in range(1):
			for aux in X:
				#list_aux = [X[j][0]]
				
				#aux = X[j][1].retornar_valor_elm()
				res = list()

				res.append(str(aux[0]).replace('.',',')[0:7])
				res.append(str(aux[1]).replace('.',',')[0:7])
				res.append(str(aux[2]).replace('.',',')[0:7])
				res.append(str(aux[3]).replace('.',',')[0:7])
				res.append(str(aux[4]).replace('.',',')[0:7])

				writer.writerow(res)
	csvFile.close()

def do_prediction(path,op):
	datass = [nome for nome in os.listdir(path)]

	print(datass)
	print(len(datass))
	datas = [sys.argv[1]]

	print(datas)
	indicador = ["Variacao_relativa_valores.txt","Preco_Tipico_valores.txt","Kni_Indicator_valores.txt","Variacao_valores.txt"]

	arquivos = files_path09('../parametros/')
	num_ativos,delay = param_ret(op,arquivos)
	pred_completo = list()

	for dia in datas:
		fold = path+dia
		caminhos = [os.path.join(fold, nome) for nome in os.listdir(fold)]

		print(len(caminhos))
		print(caminhos)
		c = [10,100,0.4,1]
		poly_kernel_param = ((1,0.8),(1,0.8),(1,0.8),(1,0.8))
		el = definir_mat_kelm(c,num_ativos,poly_kernel_param)


		for i in range(num_ativos):
			lista_dados = list()
			for ind in indicador:
				aux = caminhos[i]+"/"+ind
				print(aux)
				x = ler_dados_arq(aux)
				lista_dados.append(x)
				del x

			nome_ativo = pegar_nome_ativo(caminhos[i])
			print(nome_ativo)
			dados = [lista_dados[0],lista_dados[1],lista_dados[2],lista_dados[3]]
			predicoes = list()

			for k in range(4):
				in_train,out_train,test_dados = dividir_dados(dados[k],delay[i][k])
				el[i][k].train(in_train,out_train)
				result  = el[i][k].test(in_train,test_dados)
				predicoes.append(result)
				del in_train
				del out_train
				del test_dados
			pred_completo.append([nome_ativo]+predicoes)
	return pred_completo

if __name__ == '__main__':
	datas = [sys.argv[1]]
	op = int(sys.argv[2])

	if op == 1:
		pred_completo = do_prediction('../historico3/',3)
		registrar(pred_completo,'Predicoes/elm_'+datas[0],datas[0])
	elif op == 2:
		pred_completo = do_prediction('../historico_semanal/',2)
		registrar(pred_completo,'Predicoes/elm_semanal_'+datas[0],datas[0])