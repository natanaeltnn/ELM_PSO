from pyswarm import pso
from IO import *
import locale
import sys
sys.path.insert(0,"../CPSO")
from gaussian_pso import *
from CPSO import *
from CPSO.SolveSystemFitness import *
from CPSO.CPSO import *
import pyswarms as ps
import matplotlib.pyplot as plt
from pso_canon import *
#from func_auxiliares import *


def apply_fitness(x,*args):
	#ind1, ind2,ind3,ind4 = args
	values_elm = args
	#print("args: ",args[1])
	values = x
	calcVM1 = (values[1]+values[0])/(values[2]+values[3])
	calcVM2 = (values[2] + values[3] + values[1])/3
	calcVM3 = (values[2]*values[0])/(values[1]*values[3])
	calcVM4 = values[2]+values[3]
	#print(values_elm[0][1])
	
	err1 = abs(values_elm[0]-calcVM1)
	err2 = abs(values_elm[1]-calcVM2)
	err3 = abs(values_elm[2]-calcVM3)
	err4 = abs(values_elm[3]-calcVM4)
	return (err1+err2+err3+err4)/4


def feasible(x,*args):
	values = x
	OPEN = 0
	CLOSE = 1
	HIGH = 2
	LOW = 3

	if (values[HIGH] >= values[OPEN] and values[HIGH] >= values[CLOSE] and 
		values[HIGH] >= values[LOW] and values[LOW] <= values[OPEN] and 
		values[LOW] <= values[CLOSE] and MAPE(values[LOW],values[HIGH]) < 4):
		return 1
	else:
		return -1

'''def feasible(x):
	values = x
	OPEN = 0
	CLOSE = 1
	HIGH = 2
	LOW = 3

	return (values[HIGH] >= values[OPEN] and values[HIGH] >= values[CLOSE] and 
		values[HIGH] >= values[LOW] and values[LOW] <= values[OPEN] and 
		values[LOW] <= values[CLOSE] and MAPE(values[LOW],values[HIGH]) < 8):'''

def grafico(fit_a,nome_ativo):
	x = range(1,(len(fit_a)+1))
	plt.plot(x,fit_a)
	plt.title(nome_ativo)
	plt.savefig("graficos/"+nome_ativo)
	plt.close()

def func2_CPSO(nome_ativo,values,j,dia,opcao):
	medidas = ["open.txt","close.txt","high.txt","low.txt"]
	#a_open = ler_dados_arq("../Open/"+dia+"/open.txt")

	'''if opcao == 1:
		if len(a_open) > 3:
			a_open = a_open[5:8]
	elif opcao == 2:
		if len(a_open) > 12:
			a_open = a_open[0:5]+a_open[8:]'''

	path = '../limites/'+dia+'/'+nome_ativo+'/'
	lim_inf = list()
	lim_sup = list()
	tuple_values = list([values[0],values[1],values[2],values[3]])
	print(tuple_values)
	options = {'omega':0.729, 'phiP':1.49, 'phiG':1.49, 'maximumStagnation':5,'logisticA': 4,'jumpN': 20,'stagnationEps': 0.01}
	for aux in medidas:
		p = path+aux
		valor_min,valor_max = get_limites(p)

		if aux == "high.txt":
			lim_inf.append(valor_min)
			lim_sup.append(valor_max)
		elif aux == "low.txt":
			lim_inf.append(valor_min)
			lim_sup.append(valor_max)
		elif aux == "open.txt":
			lim_inf.append(valor_min)
			lim_sup.append(valor_max)
		else:
			lim_inf.append(valor_min)
			lim_sup.append(valor_max)

	fit = SolveSystemFitness2(tuple_values[0],tuple_values[1],tuple_values[2],tuple_values[3])
	cpso = CPSO((lim_inf,lim_sup),4,50,options,fit)
	p,xopt,vet_fit = cpso.run_until(0,1500)
	return (xopt[1:],p,xopt[0])

def func_CPSO(nome_ativo,values,j,dia,tipo = 0):
	medidas = ["close.txt","high.txt","low.txt"]
	a_open = list()
	path = ""
	if tipo == 2:
		path = '../limites/'+dia+'-semanal/'+nome_ativo+'/'
		a_open = ler_dados_arq("../Open/"+dia+"-semanal/"+nome_ativo+"/open.txt")
	elif tipo == 1:
		path = '../limites/'+dia+'-horario/'+nome_ativo+'/'
		#print(path)
		a_open = ler_dados_arq("../Open/"+dia+"-horario/"+nome_ativo+"/open.txt")		
	else:
		path = '../limites/'+dia+'/'+nome_ativo+'/'
		a_open = ler_dados_arq("../Open/"+dia+"/"+nome_ativo+"/open.txt")

	lim_inf = list()
	lim_sup = list()
	tuple_values = list([values[0],values[1],values[2],values[3]])
	print(tuple_values)
	options = {'omega':0.729, 'phiP':1.49, 'phiG':1.49, 'maximumStagnation':5,'logisticA': 4,'jumpN': 20,'stagnationEps': 0.01}
	for aux in medidas:
		p = path+aux
		valor_min,valor_max = get_limites(p)

		if aux == "high.txt":
			lim_inf.append(a_open[0])
			lim_sup.append(valor_max)
		elif aux == "low.txt":
			lim_inf.append(valor_min)
			lim_sup.append(a_open[0])
		else:
			lim_inf.append(valor_min)
			lim_sup.append(valor_max)

	fit = SolveSystemFitness(tuple_values[0],tuple_values[1],tuple_values[2],tuple_values[3],a_open[0])
	print(a_open[0],lim_inf,lim_sup)
	cpso = CPSO((lim_inf,lim_sup),3,50,options,fit)
	#cpso.particulas()
	p,xopt,vet_fit = cpso.run_until(0,1500)
	print('p ',p)
	#grafico(vet_fit,nome_ativo+"_logisticA_"+str(options['logisticA']))
	return (xopt,p,a_open[0])


def func_PSO(nome_ativo,values,j,dia):
	medidas = ["close.txt","high.txt","low.txt"]
	a_open = ler_dados_arq("../Open/"+dia+"/open.txt")
	#a_open = [18.79]
	path = '../limites/'+dia+'/'+nome_ativo+'/'
	lim_inf = list()
	lim_sup = list()
	tuple_values = list([values[0][0],100*values[1][0],values[2][0],100*values[3][0]])
	#options = {'omega':0.8, 'phiP':2, 'phiG':2, 'maximumStagnation':5,'logisticA': 4,'jumpN': 20,'stagnationEps': 0.0001}
	for aux in medidas:
		p = path+aux
		valor_min,valor_max = get_limites(p)
		lim_inf.append(valor_min)
		lim_sup.append(valor_max)
	fit = SolveSystemFitness(tuple_values[0],tuple_values[1],tuple_values[2],tuple_values[3],a_open[j])
	#cpso = CPSO((lim_inf,lim_sup),3,30,options,fit)
	#cpso.particulas()
	pso = PSO(fit.apply_fitness,None,(lim_inf,lim_sup),50,1000,fit.feasible)

	p,xopt = pso.resultado()
	#print('vet_fit ',vet_fit)
	#grafico(vet_fit,nome_ativo+"_logisticA_"+str(options['logisticA']))
	return (xopt,p,a_open[j])

def func_GPSO(nome_ativo,values):
	medidas = ["open.txt","close.txt","high.txt","low.txt"]
	path = '../limites/'+nome_ativo+'/'
	lim_inf = list()
	lim_sup = list()
	tuple_values = list([values[0][0],100*values[1][0],values[2][0],100*values[3][0]])
	#print(type(tuple_values))
	#print(tuple_values)
	
	for aux in medidas:
		p = path+aux
		#print(p)
		valor_min,valor_max = get_limites(p)
		lim_inf.append(valor_min)
		lim_sup.append(valor_max)
	#print(lim_inf)
	#print(lim_sup)
	options = {'c1':1, 'c2':1, 'w':0}
	'''optimizer = ps.single.GlobalBestPSO(n_particles=100, dimensions=4, options=options,bounds = (np.array(lim_inf),np.array(lim_sup)))
	cost, pos = optimizer.optimize(apply_fitness, iters=2000,verbose = 3, **{'ind1': tuple_values[0],
		'ind2': tuple_values[1],'ind3': tuple_values[2],'ind4': tuple_values[3]})'''
	print((np.array(lim_inf),np.array(lim_sup)))
	print(options)
	g_pso = Gausian_PSO(100,4,options,bounds=(np.transpose(np.array(lim_inf)),np.transpose(np.array(lim_sup))),ftol=0.02)

	xopt,p = g_pso.optimize(apply_fitness,f_ieqcons=feasible,args = tuple_values,maxiter=2000)

	#plot_cost_history(cost_history=optimizer.cost_history)
	#plt.show()
	#print(ps)
	return (xopt,p)