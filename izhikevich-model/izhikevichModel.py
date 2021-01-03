import numpy as np
from numpy import *
from numpy.random import *
import pylab as pl
import matplotlib as plt


#Electronic version of the figure and reproduction permissions are freely available at www.izhikevich.com
#
#
def izhikevichModel (a , b, c , d , I, v0, u0, dt):
    spikeValue = 40     # [mV] the maximum of the spike
    threshold = 30      #threshold for spiking activity

    #The parameter v is the voltage membran
    v = np.zeros(len(I))

    #The parameter u is a membrane recovery variable
    u = np.zeros(len(I))

    v[0] = v0 #in mV
    u[0] = u0 #in mV

    for i in range(1, len(I)):

        if v[i - 1] < threshold:
            dv =  0.04 * pow(v[i - 1], 2) + 5 * v[i - 1] + 140 - u[i - 1] + I[i -1]
            v[i] = v[i - 1] + (dv * dt)

            du = a * (b * v[i - 1] - u[i - 1])
            u[i] = u[i - 1] + (du * dt)
        else:
            v[i-1] = spikeValue
            v[i] = c                #reset the membrane voltage
            u[i] = u[i - 1] + d     #reset the recovery variable
    return v

