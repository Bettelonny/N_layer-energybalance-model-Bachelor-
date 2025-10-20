import numpy as np
import math

def fluxes_N_layer(Q, eps):
    sigma = 5.670374419e-8
    t=1-eps #transmissivity
    #t[0]=1 

    N=len(Q)

    Flux_up_layer = []
    flux_self=eps*Q #flux from each layer itself, vector.
    trans=0
    
    for i in range(N): #Calculate layer flux
        flux=flux_self[i]
        
        for k in range(i):#Add flux from other flux components from transmission below. range(0), dont it run
            trans=math.prod(t[k+1:i+1]) #transmission from layers above 
            flux+=trans*flux_self[k]
        
        Flux_up_layer.append(flux)
    
    
    Flux_down_layer= [] #invert layers
    flux_self_down=flux_self[::-1]
    t_down=t[::-1]
    
    for i in range(N): #Calculate layer flux
        flux=flux_self_down[i]
        
        
        for k in range(i):#Add flux from other flux components from transmission below. range(0), dont it run
            trans=math.prod(t_down[k+1:i+1]) #transmission from layers above 
            flux+=trans*flux_self_down[k]
        
        Flux_down_layer.append(flux)
    Flux_down_layer[-1]=0
    Flux_down_layer=Flux_down_layer[::-1]
        
    return flux_self, Flux_up_layer, Flux_down_layer

def fluxes_N_layer_tilted(Te4, eps,ratio_up):
    sigma = 5.670374419e-8
    t=1-eps #transmissivity
    t[0]=1 
    eps_up=eps*ratio_up*2
    eps_up[0]=1
    eps_down=eps*(1-ratio_up)*2
    
    N=len(Te4)#vector from 0,1,2,3..len(Te4)-1
    flux_self_up=sigma*eps_up*Te4 #flux from each layer itself, vector.
    flux_self_down=sigma*eps_down*Te4 #flux from each layer itself, vector.

    Flux_up_layer = []
 
    trans=0
    
    for i in range(N): #Calculate layer flux from layer
        flux=flux_self_up[i]
        
        for k in range(i):#Add flux from other flux components from transmission below. range(0), dont it run
            trans=math.prod(t[k+1:i+1]) #transmission from layers above 
            flux+=trans*flux_self_up[k]
        
        Flux_up_layer.append(flux)
    
    
    Flux_down_layer= [] #invert layers
    flux_self_down=flux_self_down[::-1]
    t_down=t[::-1]
    
    for i in range(N): #Calculate layer flux
        flux=flux_self_down[i]
        
        
        for k in range(i):#Add flux from other flux components from transmission below. range(0), dont it run
            trans=math.prod(t_down[k+1:i+1]) #transmission from layers above
            flux+=trans*flux_self_down[k]
        
        Flux_down_layer.append(flux)
    Flux_down_layer[-1]=0
    Flux_down_layer=Flux_down_layer[::-1]
        
    return flux_self_up, flux_self_down, Flux_up_layer, Flux_down_layer


