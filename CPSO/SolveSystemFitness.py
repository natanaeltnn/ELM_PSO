from func_auxiliares import *
from IO import *
import math

class SolveSystemFitness(object):
	"""docstring for SolveSystemFitness"""
	def __init__(self, v1,v2,v3,v4,op):
		self.v1 = v1
		self.v2 = v2
		self.v3 = v3
		self.v4 = v4
		self.op = op

	def feasible(self,x):
		values = x
		OPEN = 0
		CLOSE = 1-1
		HIGH = 2-1
		LOW = 3-1

		return (values[HIGH] >= self.op and values[HIGH] >= values[CLOSE] and 
		values[HIGH] >= values[LOW] and values[LOW] <= self.op and 
		values[LOW] <= values[CLOSE] and MAPE(values[LOW],values[HIGH]) < 4)
	
	def apply_fitness(self,x):
		values = x
		calcVM1 = (values[1-1]+self.op )/(values[2-1]+values[3-1])
		#calcVM2 = (values[2-1] + values[3-1] + values[1-1])/3
		calcVM2 = (values[1-1]/(values[1-1]+values[2-1]+values[3-1]))
		calcVM3 = (values[2-1]*self.op )/(values[1-1]*values[3-1])
		#calcVM4 = values[2-1]+values[3-1]
		calcVM4 = (self.op /(self.op+values[1-1]+values[2-1]))
		#print(values_elm[0][1])
	
		err1 = abs(self.v1-calcVM1)*0.3
		err2 = abs(self.v2-calcVM2)
		err3 = abs(self.v3-calcVM3)*0.3
		err4 = abs(self.v4-calcVM4)

		return (err1+err2+err3+err4)/4

class SolveSystemFitness2(object):
	"""docstring for SolveSystemFitness"""
	def __init__(self, v1,v2,v3,v4):
		self.v1 = v1
		self.v2 = v2
		self.v3 = v3
		self.v4 = v4

	def feasible(self,x):
		values = x
		OPEN = 0
		CLOSE = 1
		HIGH = 2
		LOW = 3

		return (values[HIGH] >= values[OPEN] and values[HIGH] >= values[CLOSE] and 
		values[HIGH] >= values[LOW] and values[LOW] <= values[OPEN]  and 
		values[LOW] <= values[CLOSE] and MAPE(values[LOW],values[HIGH]) < 4)

	def apply_fitness(self,x):
		values = x
		calcVM1 = (values[1]+values[0] )/(values[2]+values[3])
		#calcVM2 = (values[2-1] + values[3-1] + values[1-1])/3
		calcVM2 = (values[1]/(values[1]+values[2]+values[3]))
		calcVM3 = (values[2]*values[0] )/(values[1]*values[3])
		#calcVM4 = values[2-1]+values[3-1]
		calcVM4 = (values[0] /(values[0]+values[1]+values[2]))
		#print(values_elm[0][1])
	
		err1 = abs(self.v1-calcVM1)*0.3
		err2 = abs(self.v2-calcVM2)
		err3 = abs(self.v3-calcVM3)*0.3
		err4 = abs(self.v4-calcVM4)

		return (err1+err2+err3+err4)/4

def rosenbrock(x):
	soma = 0
	tam  = len(x)-1
	for i in range(tam):
		soma= soma + 100*math.pow((x[i+1]-math.pow(x[i],2)),2) + math.pow((x[i]-1),2)
	return soma

def schaffer(a):
	x = a[0]
	y = a[1]
	b = math.pow(x,2)+math.pow(y,2)
	num = math.pow(math.sin(math.sqrt(b)),2) - 0.5
	den= math.pow((1.0+0.001*b),2)

	out = 0.5 + num/den

	return out

def sphere(x):
	s = 0

	for i in range(len(x)):
		#print(x[i])
		s = s + x[i]*x[i]
	return s

def rastrigin(x):
	s = 0
	n = len(x)
	for i in range(n):
		s = s + (math.pow(x[i],2) - 10*math.cos(2*math.pi*x[i]))
	
	return (10*n+s)

def schwefel(x):
	s = 0
	n = len(x)
	for i in range(n):
		s = s + (x[i]*math.sin(math.sqrt(abs(x[i]))))
	
	return (418.9829*n - s)

class SolveSystemFitness_Test(object):
	"""docstring for SolveSystemFitness"""
	def __init__(self,indice):
		self.ind  = indice

	def apply_fitness(self,x):
		if self.ind == 0:
			return rosenbrock(x)
		else:
			if self.ind == 1:
				return schaffer(x)
			elif self.ind == 2:
				return sphere(x)
			elif self.ind == 3:
				return rastrigin(x)
			elif self.ind == 4:
				return schwefel(x)

	def feasible(self,x):
		return True