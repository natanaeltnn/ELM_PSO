import numpy as np
import random
import copy

def posicao_inicial(bounds):
	tam = len(bounds[0])
	a_posicoes = list()

	for i in range(tam):
		x = randomFloat(bounds[0][i],bounds[1][i])
		#x = randomFloat(0,50)
		a_posicoes.append(x)

	return a_posicoes

def velocidade_inicial(bounds):
	tam = len(bounds[0])
	a_velocity = list()
	limites_vel = list()

	for i in range(tam):
		#vel_max = float(abs(bounds[1][i]-bounds[0][i]))
		vel_max = 6 
		vel_min = (-1)*vel_max
		#v = randomFloat(vel_min,vel_max)
		v = 0
		limites_vel.append([vel_min,vel_max])
		a_velocity.append(v)
	#print(limites_vel[3][1])
	return a_velocity,limites_vel

def randomFloat(minimo,maximo):
	return random.random()*(maximo-minimo)+minimo

def inicializar_Particula(bounds):
	p = Particula(len(bounds[0]))
	
	p.inserir_posicao(posicao_inicial(bounds))
	
	a_velocity,limites_vel = velocidade_inicial(bounds)
	
	p.inserir_vel(a_velocity,limites_vel)

	return p

class Particula(object):
	"""docstring for Particula"""
	def __init__(self,dim=4):
		self.position = np.zeros(dim)
		self.velocity = np.zeros(dim)
		self.best_position = np.zeros(dim)
		self.best_fitness = 999999999.9
		self.stagnationCounter = 0
		self.vel_rest = np.zeros((dim,2))

	def inserir_posicao(self,v):
		self.position = np.copy(v)

	def inserir_vel(self,v,x):
		self.velocity = np.copy(v)
		self.vel_rest = np.copy(x)

		#print('inicial: ',self.vel_rest,' vel: ',self.velocity)

	def inserir_best_position(self,v):
		self.best_position = np.copy(v)

	def return_pos(self):
		return self.position

	def get_vel_rest(self):
		#print('dfff')
		#print(len(self.vel_rest))
		return self.vel_rest

	def copy(self,p):
		self.position = np.copy(p.position)
		self.velocity = np.copy(p.velocity)
		#print('velocity: ',self.velocity)
		self.best_position = np.copy(p.best_position)
		self.best_fitness = copy.copy(p.best_fitness)
		self.stagnationCounter =copy.copy(p.stagnationCounter)
		self.vel_rest = np.copy(p.vel_rest)