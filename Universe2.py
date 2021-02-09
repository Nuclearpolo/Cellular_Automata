import numpy as np 
from numpy import random
from numpy.random import seed
from numpy.random import rand
import matplotlib.pyplot as plt
from matplotlib import colors
import statistics

# Rule 1, define flux vector
for i in range(0,Ysize):
    for j in range(0,Xsize):
        # look at a cell and make it relative
        
        



#All zero array
# X = input("X size (Global)")
# Y = input("Y size (Global)") 
Xsize = 9
Ysize = 9
space = np.zeros(9,9)
# Cell is vector containing all values [E, F_x1, F_y1, Fp_x, Fp_y]

for i in range(0,Ysize):
    for j in range(0,Xsize):
        space[i,j] = [np.random(), np.random(), np.random(), 0, 0]

# x(1 skip 2,0 skip 2) 01010101


# x(0 skip 2,1 skip 2) 10101010
# space[:,:] = random.randint(-1000, 1000, 1)
space[6][6] = 1000 
space[2][2] = 500

X = space.shape[0] - 1
Y = space.shape[1] - 1



# No. of time steps
time = 10

# Loop over all possible time
t = 0
while t < time:
    t += 1
    if t <= X:  
        for i in range(-t, t):
            for j in range(t, t):    
                
                LocalSpaceSetup(space)
                LocalSpacelimits(n,m,X,Y)
               
                

image = space
plt.imshow(image, cmap=plt.cm.hot_r)
plt.colorbar()
plt.show()
print(space)
