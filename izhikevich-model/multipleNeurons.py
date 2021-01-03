import numpy as np
from numpy import random
import pylab as pl
import matplotlib.pyplot as plt

#Electronic version of the figure and reproduction permissions are freely available at www.izhikevich.com

runtime = 2000

#Number of excitatory Neurons
excitatoryN = 800

#Number of inhibitory Neurons
inhibitoryN = 200

#random Excitatory Neurons
rEx = random.rand(excitatoryN)

#random of Inhibitory Neurons
rIn = random.rand(inhibitoryN)

#definition of a after Izhikevich
aEx = 0.02 * np.ones(excitatoryN)
aIn = 0.02 + 0.08 * rIn
a = np.concatenate((aEx, aIn), axis=None)

#definition of b after Izhikevich
bEx = 0.2 * np.ones(excitatoryN)
bIn = 0.25 - 0.05 * rIn
b = np.concatenate((bEx, bIn), axis=None)

#definition of c after Izhikevich
cEx = -65 + 15 * np.square(rEx)
cIn = -65 * np.ones(inhibitoryN)
c = np.concatenate((cEx, cIn), axis=None)

#definition of d after Izhikevich
dEx = 8 - 6 * np.square(rEx)
dIn = 2 * np.ones(inhibitoryN)
d = np.concatenate((dEx, dIn), axis=None)

#The matrix models the synaptic connections between neurons
SEx = 0.5 * random.rand(excitatoryN + inhibitoryN, excitatoryN)
SIn = -random.rand(excitatoryN + inhibitoryN, inhibitoryN)
S = np.concatenate((SEx, SIn), axis=1)

# The initial values of v
v = -65 * np.ones(excitatoryN + inhibitoryN, dtype=float)
u = b * v

firings = np.empty((runtime,excitatoryN + inhibitoryN),dtype=float)


for t in range(runtime): 
    
    #Thalamic input, uses normal distribution
    Iex = random.randn(excitatoryN)
    Iex *= 5  
    Iin = random.randn(inhibitoryN)
    Iin *= 2
    I = np.concatenate((Iex, Iin), axis=None)
    
    fired = (v >= 30)# indices of spikes, returns an array of zeros with ones at the spiking indices
    firings[t,:]=fired
    v[fired] = c[fired]
    u[fired] = u[fired] + d[fired]
    I = I + S[:,fired].sum(1)

    #The Izhikevich model
    v = v + 0.5 * (0.04 * v**2 + 5 * v + 140 - u + I)
    v = v + 0.5 * (0.04 * v**2 + 5 * v + 140 - u + I)
    u = u + a*(b*v - u)


ids=np.arange(1, excitatoryN + inhibitoryN +1)
numNfired = []
timefired = []

#prepares plot
for t,fired in zip(range(runtime),firings):
    res=ids[fired==1]
    for fi in res:
        numNfired.append(fi)
        timefired.append(t)


numNfired = np.array(numNfired)
timefired = np.array(timefired)


plt.scatter(timefired ,numNfired, c = "steelblue", s=1)
plt.xlabel("t(ms)")
plt.ylabel("Number of spiking neuron")
plt.show()


    
        
    
