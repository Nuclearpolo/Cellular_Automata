import numpy as np 
from numpy import random
from numpy.random import seed
from numpy.random import rand
import matplotlib.pyplot as plt
from matplotlib import colors
import statistics

# define a function that translates primitive variables to conserved quantities Q
def getConserved( rho, vx, vy, P, gamma, vol):
    Mass = rho*vol
    Momx = rho * vx * vol
    Momy = rho * vy * vol
    Energy = (P/(gamma-1) + 0.5*rho*(vx**2+vy**2))*vol
    
    return Mass, Momx, Momy, Energy 
# define a function that translates conserved quantaties to primative variables Q
def getPrimative(Mass, Momx, Momy, Energy, gamme, vol):
    rho = Mass / vol 
    vx = Momx / rho / vol
    vy = Momy / rho/ vol
    P = (Energy/vol - 0.5*rho*(vx**2+vy**2)) * (gamma-1)
    
    return rho, vx, vy, P

#function that calculates the gradient on a periodic domain in a vectorized fashion 
def getGradient(f,dx):
    #np.roll() directions
    R = -1
    L = 1 
    f_dx = ( np.roll(f,R,axis=0) - np.roll(f,L,axis=0) ) / (2*dx)
    f_dy = ( np.roll(f,R,axis=1) - np.roll(f,L,axis=1) ) / (2*dx)
    
    return f_dx, f_dy

# Spactially interpolate on faces 
def extrapolateInSpaceToFace(f, f_dx, f_dy,dx):
    R = -1 
    L = 1
    
    f_XL = f - f_dx * dx/2
    f_XL= np.roll(f_XL, R, axis=0)
    f_XR = f + f_dx * dx/2
    
    f_YL = f - f_dy * dx/2
    f_YL= np.roll(f_YL, R, axis=0)
    f_Y1R = f + f_dy * dx/2
    
    return f_XL, f_XR, f_YL, f_YR
# Rusanov Flux
def getFlux(rho_L, rho_R, vx_L, vx_R,, vy_L, vy_R, P_L, P_R, gamma):
    
    # cell wall energies
    e_L = P_L/(gamma - 1) +0.5*rho_L*(vx_L**2 + vy_L**2)
    e_R = P_R/(gamma - 1) +0.5*rho_R*(vx_R**2 + vy_R**2)
    
    # get conserved avg states
    rho_avg = 0.5(rho_L + rho_R)
    momx_avg = 0.5(rho_L * vx_L + rho_R * vx_r)
    momy_avg = 0.5(rho_L * vy_L + rho_R * vy_r)
    eng_avg = 0.5(en_L + en_R)
    P_avg = (gamma-1)*(eng_avg - 0.5* (momx_avg**2 + momy_avg**2)/rho_avg)) # rho on bottom here because momentum = rho*v so momentum 2 =rho2*v2
    
    # compute flux, not really sure why certain equations are used. Best to understand this
    flux_Mass = momx_avg
    flux_Momx = momx_avg**2/rho_avg + P_avg
    flux_Momy = momy_avg**2/rho_avg + P_avg
    # flux_Momy = momx_avg*momy_avg/rho_avg    THis is given in tutorial but I don't understand why its different. 
    flux_Eng = (eng_avg + P_avg) * momx_avg/rho_avg
    
    # find wavespeeds
    c_L = np.sprt(gamma*(P_L / rho_L))
    c_R = np.sprt(gamma*(P_R / rho_R))
    c = np.maximum( c_L, c_R)
    
    # Add diffusion term
    flux_Mass -= c*0.5*(rho_L - rho_R)
    flux_Momx -= c*0.5*(rho_L*vx_L - rho_R*vx_R)
    flux_Momy -= c*0.5*(rho_L*vy_L - rho_R*vy_R)
    flux_Eng -= c*0.5*(en_L - eng_R)
    
    return flux_Mass, flux_Momx, flux_Momy, flux_Eng