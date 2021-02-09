import numpy as np 
from numpy import random
from numpy.random import seed
from numpy.random import rand
import matplotlib.pyplot as plt
from matplotlib import colors
import statistics
# for some reason its pumping out a "pull to vacuum"
# struggles with signs too, all positive Edotdot values. 
# all values too big and getting inf.
Dspace = np.array([10.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 5.0, 0.0, 0.0], dtype=np.float64)
print(len(Dspace))
tstep=1
t=0
while t < tstep:
    t += 1
    
    Edotdot = np.zeros((len(Dspace), len(Dspace)))
    
    for i in range(0, len(Dspace)-1):
        for j in range(0, len(Dspace)-1):
            if Dspace[j] == 0:
                Edotdot[j][i] = 0.0
            
            else:
                if i == j:
                    Edotdot[j][i] = 0.0
                    #print(Edotdot[j][i])
                elif i < j:
                    Edotdot[j][i] = Dspace[j]/((j-i)^2) 
                    #print(Edotdot[j][i])
                else:
                    Edotdot[j][i] = Dspace[j]/((i-j)^2)
                   
                    #print(Edotdot[j][i])
            # if i == 'inf':
            #     print(i)
            #     print(j)
            #     print(Dspace[j])
            #     print(Dspace[i])
 
print(Edotdot)       
         