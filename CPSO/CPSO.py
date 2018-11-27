import numpy as np
import random
from CPSO.Particula import *
from CPSO.SolveSystemFitness import *
from copy import deepcopy
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.animation as animation

def grafico_3d(a,b,c):
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	x = a
	y = b
	z = c
	
	ax.clear()
	ax.scatter(x, y, z)
	plt.draw()
	plt.pause(0.0001)
	plt.clf()
	#plt.show()

def split(pop):
	close = list()
	high = list()
	low = list()

	for i in range(len(pop)):
		close.append(pop[i].position[0])
		high.append(pop[i].position[1])
		low.append(pop[i].position[2])
	return (close,high,low)

class CPSO(object):
	"""docstring for CPSO"""
	def __init__(self, bounds,num_dimensions, numParticles, options,Fit_solver):
		self.population = list()
		self.num_dimensions = num_dimensions
		self.numParticles = numParticles
		self.bounds = deepcopy(bounds)
		self.options = deepcopy(options)
		self.Fit_solver = Fit_solver
		self.bestGlobalPosition = np.zeros(num_dimensions)
		self.bestGlobalFitness = 99999999999.9
		self. best_fit_arry = list()
		random.seed()
		i = 0
		for i in range(numParticles):
			p = Particula(num_dimensions)
			
			while True:
				i = i+1
				#print(i)
				aux_particula = inicializar_Particula(bounds)
				if Fit_solver.feasible(aux_particula.position):
					#print('feasible')
					i = 0
					p.copy(aux_particula)
					del aux_particula
					break

				del aux_particula
			p.inserir_best_position(p.position)

			initialFitness = Fit_solver.apply_fitness(p.position)
			p.best_fitness = initialFitness

			if(initialFitness < self.bestGlobalFitness):
				self.bestGlobalFitness = initialFitness
				self.bestGlobalPosition =  np.copy(p.position)
				#self.best_fit_arry.append(initialFitness)
			p.stagnationCounter = 0
			#print(p.velocity)
			self.population.append(p)
			#print('particula vel: ',self.population[i].velocity)
	
	def logistic(self, a,y):
		return a*y*(1-y)

	def randomLogisticDouble(self):
		cj = random.random()
		while (cj==0) or (cj==0.25) or (cj==0.5) or (cj==0.75) or (cj==1.0):
			cj=random.random()

		result = self.logistic(self.options['logisticA'], cj)*2-1
		return result

	def run(self):
		for i in range(self.numParticles):
			for j in range(self.num_dimensions):
				eta  = (self.options['jumpN']/100.0) * (self.bounds[1][j] - self.bounds[0][j])
				if self.population[i].stagnationCounter < self.options['maximumStagnation']:
					rp = random.random()
					rg = random.random()

					t = self.options['omega']*self.population[i].velocity[j]+self.options['phiP']*rp*(self.population[i].best_position[j]-self.population[i].position[j])+self.options['phiG']*rg*(self.bestGlobalPosition[j]-self.population[i].position[j])

					#print(i,' omega e vel: ', self.options['omega']*self.population[i].velocity[j],
					#' segunda parte: ',self.options['phiP']*rp*(self.population[i].best_position[j]-self.population[i].position[j])+ self.options['phiG']*rg*(self.bestGlobalPosition[j]-self.population[i].position[j])
					#,' t: ',t)
                    #self.options['omega']*self.population[i].velocity[j]
					self.population[i].velocity[j] =  self.options['omega']*self.population[i].velocity[j]+self.options['phiP']*rp*(self.population[i].best_position[j]-self.population[i].position[j])+self.options['phiG']*rg*(self.bestGlobalPosition[j]-self.population[i].position[j])

					#if i == 0:
					
					#print('vel: ', self.population[i].velocity)
					self.population[i].position[j] += self.population[i].velocity[j]
				else:
					#print('valor stag: ',self.population[i].stagnationCounter)
					self.population[i].position[j] = self.population[i].best_position[j]*(1+eta*self.randomLogisticDouble())
				
				if(self.population[i].position[j] < self.bounds[0][j] or self.population[i].position[j] > self.bounds[1][j]):
					self.population[i].position[j] = np.copy(self.population[i].best_position[j])
					#self.population[i].best_fitness = self.Fit_solver.apply_fitness(self.population[i])
				
				if (self.population[i].velocity[j] > self.population[i].vel_rest[j][1]):
					self.population[i].velocity[j] = self.population[i].vel_rest[j][1]

				if (self.population[i].velocity[j] < self.population[i].vel_rest[j][0]):
					self.population[i].velocity[j] = self.population[i].vel_rest[j][0]

				if self.population[i].stagnationCounter > self.options['maximumStagnation']:
					self.population[i].stagnationCounter = 0
					
			#print('velocity: ',self.population[i].velocity)
			particleFitness = self.Fit_solver.apply_fitness(self.population[i].position)
			
			'''if(abs(particleFitness - self.population[i].best_fitness) < self.options['stagnationEps']):
				self.population[i].stagnationCounter += 1
				#print(self.population[i].stagnationCounter)
			else:
				self.population[i].stagnationCounter = 0'''

			if particleFitness < self.population[i].best_fitness and self.Fit_solver.feasible(self.population[i].position):
				self.population[i].best_fitness = particleFitness
				self.population[i].inserir_best_position(self.population[i].position)
				self.population[i].stagnationCounter = 0
				if(particleFitness < self.bestGlobalFitness):
					self.bestGlobalFitness = particleFitness
					self.bestGlobalPosition =  np.copy(self.population[i].position)
			else:
				self.population[i].stagnationCounter += 1

		return (self.bestGlobalFitness,self.bestGlobalPosition)

	def run_until(self,target,num_iter):
		best_fit = 9999999.9
		best_pos = np.zeros(self.num_dimensions)
		it = 0
		print('fitness inicial: ',best_fit)
		'''plt.ion()
		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')'''
		while (best_fit > target) and (it < num_iter):
			best_fit,best_pos = self.run()
			#print(self.population[0].velocity, self.population[0].vel_rest)
			#print('i: ',it,' best_fit: ',best_fit)
			'''c,h,l = split(self.population)
			ax.scatter(c, h, l)
			plt.draw()
			plt.pause(0.1)
			ax.clear()
			ax.cla()'''
			self.best_fit_arry.append(best_fit)
			it +=1

		'''x = range(len(self.best_fit_arry))
		plt.plot(x,self.best_fit_arry)
		plt.show()'''

		#c,h,l = split(self.population)
		#print('best_pos',best_pos)
		#self.particulas()
		#grafico_3d(c,h,l)

		return (best_fit,best_pos,self.best_fit_arry)

	def particulas(self):
		for p in self.population:
			print('pos: ',p.return_pos(),' best_pos: ',p.best_position,' velocity: ',p.velocity,'best-fitness: ',p.best_fitness)

	#def stagnation():









		
		