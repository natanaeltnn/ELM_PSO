import numpy as np 
import math
from sklearn.metrics.pairwise import polynomial_kernel

class KELM:

    def __init__(self,C,type_uso = 'R',kernel_type = 'lin_kernel',kernel_para = None):
        self.reg = C
        self.type = kernel_type
        self.tipo = type_uso
        self.kernel_param = kernel_para


    def train(self,in_train,out_train):
        omega_train = self.kernel_matrix(in_train)
        identidade = np.eye(len(in_train))
        identidade_c = identidade*(1/self.reg)
        x = omega_train+identidade_c
        self.out_weight = np.linalg.solve(x,out_train)
        self.out_weight = np.reshape(self.out_weight,(len(in_train),1))
        self.out_weight = np.squeeze(np.asarray(self.out_weight))

    def test(self,in_train,in_test):
        omega_test = self.kernel_matrix(in_train,in_test)
        omega_test = np.squeeze(np.asarray(omega_test))
        return np.dot(omega_test,self.out_weight)


    def kernel_matrix(self,Train,test = None):
        if self.type == 'lin_kernel':
            if test is None:
                return np.dot(Train,np.transpose(Train))
            else:
                return np.dot(Train,np.transpose(test))
        elif self.type == 'poly_kernel':
            if test is None:
                return np.power((np.dot(Train,np.transpose(Train))+self.kernel_param[0]),self.kernel_param[1])
            else:
                return np.power((np.dot(Train,np.transpose(test))+self.kernel_param[0]),self.kernel_param[1])

