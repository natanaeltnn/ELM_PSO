from func_auxiliares import *
from IO import *

class candle:
	"""docstring for Candle"""
	def __init__(self, o = None,c = None,h = None,l = None,pred_ind1 = None,pred_ind2 = None,
		pred_ind3 = None,pred_ind4 = None,xopt = None,cand = None):
		if cand == None:
			self.pred_elm = list()
			self.pred_elm.append(pred_ind1)
			self.pred_elm.append(pred_ind2)
			self.pred_elm.append(pred_ind3)
			self.pred_elm.append(pred_ind4)
			self.open = o
			self.close = c
			self.high = h
			self.low = l
			self.mape_h_l = MAPE(self.low,self.high)
			self.xopt = xopt
		else:
			self.open = cand.open
			self.close = cand.close
			self.high = cand.high
			self.low = cand.low
			self.mape_h_l = cand.mape_h_l
			self.pred_elm = cand.pred_elm.copy()

	def calcular_erro_pred(self,real):
		self.erro_pred = MAPE(real,self.open)

	def retornar_valores(self):
		return [self.open,self.close,self.high,self.low,self.xopt]

	def retornar_valor_elm(self):
		return [self.pred_elm[0],self.pred_elm[1],self.pred_elm[2],self.pred_elm[3]]

		

		
		
		