from elm import ELM
from func_auxiliares import *
from sistema_ativos import Ativo
from func_aux_pso import *
import os

if __name__ == '__main__':
	num_rodadas = 5
	num_ativos = 12
	caminhos = [os.path.join('../historico2', nome) for nome in os.listdir('../historico2')]
	print(caminhos)
	indicador = ["Variacao_relativa_valores.txt","Preco_Tipico_valores.txt","Kni_Indicator_valores.txt","Variacao_valores.txt"]
	tam = len(caminhos)

	arquivos = files_path09('../parametros/')
	delay,params_janela,params_neurons = ler_params(arquivos,tam)
	el = definir_mat_elm(delay,params_neurons)

	at = Ativo(num_rodadas)
	
	for j in range(num_rodadas):
		for i in range(num_ativos):
			lista_dados = list()
			for ind in indicador:
				aux = caminhos[i]+"/"+ind
				print(aux)
				x = ler_dados_arq(aux)
				lista_dados.append(x)
				del x

			nome_ativo = pegar_nome_ativo(caminhos[i])
			#print("lista de dados",lista_dados)
			dados = [lista_dados[0],lista_dados[1],lista_dados[2],lista_dados[3]]
			predicoes = list()

			for k in range(4):
				in_train,out_train,test_dados = dividir_dados(dados[k],delay[i][k])
				el[i][k].train(in_train,out_train)
				result  = el[i][k].test(test_dados)
				predicoes.append(result)
				del in_train
				del out_train
				del test_dados
			print('ja foi feita predicao')
			x_sol,ps,op = func_CPSO(nome_ativo,lista_dados,i)
			#print('x_sol: ',x_sol,' ps: ',ps)
			cand = candle(op,x_sol[0],x_sol[1],x_sol[2],predicoes[0],predicoes[1],predicoes[2],predicoes[3],ps)
			#print(cand.retornar_valores())
			at.inserir_teste_ativo(nome_ativo,cand)

	#registrar_resultados(at)