import numpy as np
import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.nn.functional as F
import shelve



class policy():
    def __init__(self, network):
        self.network = network
    def initialize(self):
        torch.nn.init.xavier_uniform(self.network.weight)
    def inference(self, state):
        torch.no_grad()
        a, p = self.network(state.cuda()).cuda()
        a1 = a.numpy()
        p1 = p.numpy()
        result = np.where(a1 == np.amax(a1))
        temp = np.array([0,0,0])
        if len(result[0]) == 1:
            temp[result[0][0]] = 1
            a1 = a1*temp
        elif len(result[0]) == 2:
            dice = np.random.uniform(1)
            if dice > 0.5:
                temp[result[0][0]] = 1
                a1 = a1 * temp
            else:
                temp[result[0][1]] = 1
                a1 = a1 * temp
        elif len(result[0]) == 2:
            dice = np.random.uniform(1)
            if dice < 0.33:
                temp[result[0][0]] = 1
                a1 = a1 * temp
            elif 0.67 >= dice >= 0.33:
                temp[result[0][1]] = 1
                a1 = a1 * temp
            else:
                temp[result[0][1]] = 1
                a1 = a1 * temp
        vec = np.concatenate([a1, p1])

        return vec