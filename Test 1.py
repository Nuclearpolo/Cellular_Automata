import numpy as np 
from numpy import random
import matplotlib.pyplot as plt
from matplotlib import colors

#May be better to average this!
# Void draws from surrounding
def Entropy(i, j, LocalSpace):
    if i == j and i == 1:
        LocalSpace[1][1] -= 0.01*(LocalSpace.shape[0]*LocalSpace.shape[1] - 1)
    else:
        LocalSpace[1+i][1+j] += 0.01
    return LocalSpace
# # Thing gives to surrounding      
def Gravity(i, j, LocalSpace):
    if i == j and i == 1:
        LocalSpace[1][1] += 0.01*(LocalSpace.shape[0]*LocalSpace.shape[1] - 1)
    else:
        LocalSpace[1+i][1+j] -= 0.01
    return LocalSpace

# More gives to less
def GraEntQ(i, j, LocalSpace):
    if LocalSpace[1][1] < LocalSpace[1+i][1+j]: # if z.cell is less than n.cell: 1 bit to z.cell from n.cell
        LocalSpace[1][1] += 0.01
        LocalSpace[1+i][1+j] -= 0.01
    elif LocalSpace[1][1] > LocalSpace[1+i][1+j]: # if z.cell is more than n.cell: 1 bit from z.cell to n.cell. LocalSpace[1][1]
        LocalSpace[1][1] -= 0.01
        LocalSpace[1+i][1+j] += 0.01
    return LocalSpace # if equal, ignore. hopefully this takes care of the 

# True/False in terms of directions in bounds [negative_i, positive_i, negative_j, positive_j]
def LocalUpdate(MArray, LocalSpace):
    if LocalSpace[1][1] >= float(1):    #select surrounding cells
        for i in range(-MArray[0], MArray[1]): 
            for j in range(-MArray[2], MArray[3]):
                Entropy(i, j, LocalSpace)
                
                          
        # elif 0 is min, draw from all 
    elif LocalSpace[1][1] <= float(0):   #select surrounding cells
        for i in range(-MArray[0], MArray[1]): 
            for j in range(-MArray[2], MArray[3]):
                   Gravity(i, j, LocalSpace)
    else: 
        for i in range(-MArray[0], MArray[0]): 
            for j in range(-MArray[2], MArray[0]):
                GraEntQ(i, j, LocalSpace) 
    return LocalSpace   

def GlobalUpdate(MArray, LocalSpace):
    for i in range(-MArray[0], MArray[1]): 
        for j in range(-MArray[2], MArray[3]):
            space[n+i][m+j] = LocalSpace[1+i][1+j]
    return space


#All zero array
# X = input("X size (Global)")
# Y = input("Y size (Global)") 
Xsize = 65
Ysize = 65
space = np.zeros((Xsize, Ysize), dtype=float)

# # x(1 skip 2,0 skip 2) 01010101
# space[1::2,::2] = 1

# # x(0 skip 2,1 skip 2) 10101010
# space[::2,1::2] = 1
space[33][33] = 1 


X = space.shape[0] - 1
Y = space.shape[1] - 1

# No. of time steps
time = 1000000

# Loop over all possible time
t = 0
while t < time:
    t += 1
    # Take a random selection on grid. 
    n = random.randint(X)
    
    m = random.randint(Y)
    
    
    # zeroth cell (z.vec), cell of interest 
    O = space[n][m]
    
    #[0101;0100;1100]
    #[0001;0000;1001]
    #[0011;0001;]   
    #
    #[0101;0100;1100]
    #[0001;0000;1001]
    #[0011;0001;1001]
    #
    # [1010]
    # [RIGHT/UP/LEFT/DOWN]
    #
    # Define neighbour cells (n.cells) 
    OIIO = space[n-1][m-1] 
    OIOO = space[n-1][m]
    IIOO = space[n-1][m+1]
    IOOI = space[n][m+1]
    IOOI = space[n+1][m+1]
    OOOI = space[n+1][m]
    OOII = space[n+1][m-1]
    OOIO = space[n][m-1]   
    
    LocalSpace = np.array([[OIIO, OIOO, IIOO],[OOIO, O, IOOI],[OOII, OOOI, IOOI]])
   
    # function too
    #temp fix before I can figure out back prop algorithm, if its more or less than max, it will consider max or min
    
    ## centre away from edges
    if (n >= 1 and m >= 1) and (n != X and m != Y):
        #Array of possible movement directions
        #[-i,+i,-j,+j] yes/no
        MArray = [1,1,1,1]
        LocalUpdate(MArray, LocalSpace)
        GlobalUpdate(MArray, LocalSpace)
    ## Edges w/o corners
    # left edge no -j
    if n == 0 and m >= 1 and m != Y:
        MArray = [1,1,0,1]
        LocalUpdate(MArray, LocalSpace)
        GlobalUpdate(MArray, LocalSpace)
        
    # top edge no -i
    elif n >= 1 and m == 0 and n != X:
        MArray = [0,1,1,1]
        LocalUpdate(MArray, LocalSpace)
        GlobalUpdate(MArray, LocalSpace)
        
    # right edge no +j
    elif n == X and m >= 1 and m != Y:
        MArray = [1,1,1,0]
        LocalUpdate(MArray, LocalSpace)
        GlobalUpdate(MArray, LocalSpace)
    
    # bottom edge no +i
    elif n >= X and m == Y and n != X:
        MArray = [1,0,1,1]
        LocalUpdate(MArray, LocalSpace)
        GlobalUpdate(MArray, LocalSpace)
    ## corners
    # Top left
    elif n == 0 and m == 0:
        MArray = [0,1,0,1]
        LocalUpdate(MArray, LocalSpace)
        GlobalUpdate(MArray, LocalSpace)
        
    # Top right
    elif n == X  and m == 0:
        MArray = [0,1,1,0]
        LocalUpdate(MArray, LocalSpace)
        GlobalUpdate(MArray, LocalSpace)
        
    elif n == X and m == Y:
        MArray = [1,0,1,0]
        LocalUpdate(MArray, LocalSpace)
        GlobalUpdate(MArray, LocalSpace)
          
    # Bottom left
    else:
        MArray = [1,0,0,1]
        LocalUpdate(MArray, LocalSpace)
        GlobalUpdate(MArray, LocalSpace)


image = space
plt.imshow(image, cmap=plt.cm.hot_r)
plt.colorbar()
plt.show()

# print(space)



