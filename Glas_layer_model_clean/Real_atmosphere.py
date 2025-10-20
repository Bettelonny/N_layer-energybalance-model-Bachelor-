import numpy as np
import pandas as pd

def read_atmosphere(file="Standard_Atmospheres/us_standard.csv",height=50,dz=1000):
    #Read standard atmosphere data
    df = pd.read_csv(file)
    z=df['z'][0:35]
    T_real=df['t'][0:35]
    O3=df['O3'][0:35] #in ppmv

    p_real=df['p'][0:35] #in hPa
    O3=O3*1e-6 #convert to volume fraction
    n_air=df['n'][0:35] #in molec/cm^3
    n_air=n_air*1e6 #convert to molec/m^3
    O3=O3*n_air #convert to molec/m^3


    #interpolate z and O3 to 1000 m resolution
    z_interp = np.arange(0, height*1000+1, dz) # from 0 to 50 km with 1 km step
    O3_interp = np.interp(z_interp, z*1000, O3) # interpolate O3 to the new z grid
    return z_interp, O3_interp, T_real, p_real, n_air
#z_interp, O3_interp, T_real, p_real = read_atmosphere(height=50,dz=1000)
#print(z_interp,O3_interp)