import numpy as np 
from numpy import random
from numpy.random import seed
from numpy.random import rand
import matplotlib.pyplot as plt
from matplotlib import colors
import statistics

def average(MArray, LocalSpace):
    
    for i in range(-MArray[0], MArray[1]): 
            for j in range(-MArray[2], MArray[3]):
                if i != 0 and j != 0:   
                    A[1+i][1+j] = (LocalSpace[1][1] + LocalSpace[1+i][1+j])/2  #Average between z.cell and n.cell
                    
                    
                    
                    if LocalSpace[1][1] >=  LocalSpace[1+i][1+j]:      # Difference in Energy between z.cell and n.cell
                        Diff[1+i][1+j] = abs(abs(LocalSpace[1][1]) - abs(LocalSpace[1+i][1+j]))
                    else: 
                        Diff[1+i][1+j] = abs(abs(LocalSpace[1+i][1+j]) - abs(LocalSpace[1][1]))
                    
                    
                    
                    FluxCell = np.zeros((2,1))
                    FluxCell[0][0] = (LocalSpace[1+i][1+j] / Diff[1+i][1+j]) * A[1+i][1+j]     # Flux for z.cell
                    FluxCell[1][0] = (LocalSpace[1][1] / Diff[1+i][1+j]) * A[1+i][1+j]      # Flux for n.cell
                    print(FluxCell)
                    Flux[1+i][1+j] = FluxCell[1][0] # Put this flux vector into array
                    Flux[1][1] += (1/8)*FluxCell[0][0]               
    print(Flux)
    return Diff 
    return Flux 
    return A 

def Localupdate(MArray, LocalSpace, Flux):
    LocalSpace = LocalSpace + Flux           
    return LocalSpace 
    
                
                # FluxCell = np.zeros(1,2)
                # Flux = Diff[1+i][1+j]
def GlobalUpdate(MArray, LocalSpace): #put into local space
    for i in range(-MArray[0], MArray[1]): 
        for j in range(-MArray[2], MArray[3]):
            space[n+i][m+j] = LocalSpace[1+i][1+j]
    return space

def Rule(MArray, LocalSpace): #the rule for this update
    average(MArray, LocalSpace)
    Localupdate(MArray, LocalSpace, Flux)
    GlobalUpdate(MArray, LocalSpace)

def LocalSpacelimits(n,m,X,Y):   #Limits local space for boundedness
    if (n >= 1 and m >= 1) and (n != X and m != Y):
        #Array of possible movement directions
        #[-i,+i,-j,+j] yes/no
        MArray = [1,1,1,1]
        Rule(MArray, LocalSpace)
    ## Edges w/o corners
    # left edge no -j
    if n == 0 and m >= 1 and m != Y:
        MArray = [1,1,0,1]
        Rule(MArray, LocalSpace)
        
    # top edge no -i
    elif n >= 1 and m == 0 and n != X:
        MArray = [0,1,1,1]
        Rule(MArray, LocalSpace)
        
    # right edge no +j
    elif n == X and m >= 1 and m != Y:
        MArray = [1,1,1,0]
        Rule(MArray, LocalSpace)

    # bottom edge no +i
    elif n >= X and m == Y and n != X:
        MArray = [1,0,1,1]
        Rule(MArray, LocalSpace)
    ## corners
    # Top left
    elif n == 0 and m == 0:
        MArray = [0,1,0,1]
        Rule(MArray, LocalSpace)
        
    # Top right
    elif n == X  and m == 0:
        MArray = [0,1,1,0]
        Rule(MArray, LocalSpace)
        
    elif n == X and m == Y:
        MArray = [1,0,1,0]
        Rule(MArray, LocalSpace)
        
    # Bottom left
    else:
        MArray = [1,0,0,1]
        Rule(MArray, LocalSpace)

def LocalSpaceSetup(space, i, j):

    n = random.randint(X)
    
    m = random.randint(Y)
    
    
    # zeroth cell (z.vec), cell of interest 
    O = space[33+i][33+j]
    
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

    Diff = np.zeros_like(LocalSpace)
    A = np.zeros_like(LocalSpace)
    Flux = np.zeros_like(LocalSpace)

#May be better to average this!
# Void draws from surrounding
# def Entropy(i, j, LocalSpace):
#     if i == j and i == 1:
#         LocalSpace[1][1] -= 0.01*(LocalSpace.shape[0]*LocalSpace.shape[1] - 1)
#     else:
#         LocalSpace[1+i][1+j] += 0.01
#     return LocalSpace
# # # Thing gives to surrounding      
# def Gravity(i, j, LocalSpace):
#     if i == j and i == 1:
#         LocalSpace[1][1] += 0.01*(LocalSpace.shape[0]*LocalSpace.shape[1] - 1)
#     else:
#         LocalSpace[1+i][1+j] -= 0.01
#     return LocalSpace

# # More gives to less
# def GraEntQ(i, j, LocalSpace):
#     if LocalSpace[1][1] < LocalSpace[1+i][1+j]: # if z.cell is less than n.cell: 1 bit to z.cell from n.cell
#         LocalSpace[1][1] += 0.01
#         LocalSpace[1+i][1+j] -= 0.01
#     elif LocalSpace[1][1] > LocalSpace[1+i][1+j]: # if z.cell is more than n.cell: 1 bit from z.cell to n.cell. LocalSpace[1][1]
#         LocalSpace[1][1] -= 0.01
#         LocalSpace[1+i][1+j] += 0.01
#     return LocalSpace # if equal, ignore. hopefully this takes care of the 

# # True/False in terms of directions in bounds [negative_i, positive_i, negative_j, positive_j]
# def LocalUpdate(MArray, LocalSpace):
#     if LocalSpace[1][1] >= float(1):    #select surrounding cells
#         for i in range(-MArray[0], MArray[1]): 
#             for j in range(-MArray[2], MArray[3]):
#                 Entropy(i, j, LocalSpace)
                
                          
#         # elif 0 is min, draw from all 
#     elif LocalSpace[1][1] <= float(0):   #select surrounding cells
#         for i in range(-MArray[0], MArray[1]): 
#             for j in range(-MArray[2], MArray[3]):
#                    Gravity(i, j, LocalSpace)
#     else: 
#         for i in range(-MArray[0], MArray[0]): 
#             for j in range(-MArray[2], MArray[0]):
#                 GraEntQ(i, j, LocalSpace) 
#     return LocalSpace   




#All zero array
# X = input("X size (Global)")
# Y = input("Y size (Global)") 
Xsize = 65
Ysize = 65
space = np.random.uniform(-1, 1, (Xsize, Ysize))

# x(1 skip 2,0 skip 2) 01010101


# x(0 skip 2,1 skip 2) 10101010
# space[:,:] = random.randint(-1000, 1000, 1)
space[33][33] = 1000 
space[31][31] = 1000

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


# print(space)