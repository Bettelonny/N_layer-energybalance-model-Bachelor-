#2_stream
from Real_atmosphere import read_atmosphere
import numpy as np
import pandas as pd


def Ozone_absorption_constant_253K_P(file_csv,Bandends=[220,1100],Bandwidth=10):
    data=pd.read_csv(file_csv)
    #I just use 253 K data
    wavelength=data["Wavelength(nm)"]
    abs_253K=data["cm^2/molecule_253K"]

    #Convert to m^2/molecule
    abs_253K=abs_253K*10**(-4)
    #make a mean band of 10 nm
    #from 210 nm to 1100 nm
    absorptivity_interval_mean=[]
    
    Bandends=np.array(Bandends)
    band_interval_O = np.arange(Bandends[0],Bandends[1]+1,Bandwidth)
    idx_old=0
    for nm in band_interval_O:
        idx = np.abs(wavelength - nm).argmin()
        absorptivity_interval_mean.append(np.mean(abs_253K[idx_old:idx]))
        idx_old=idx
    return band_interval_O, absorptivity_interval_mean


def Sun_E_bands(band_interval_O_): #
    #Bandends=np.array(Bandends)
    #band_interval_O = np.arange(Bandends[0],Bandends[1]+1,Bandwidth)
    file="Spectra/Sun_spectra_TOA_1nm_1.csv"
    
    df = pd.read_csv(file)
    wavelength_sun=df["Wavelength(nm)"]
    I=df["I[w/(m^2*lambda)]"]

    # Match the solar spectrum to the ozone absorption bands
    E_bands = []
    band_interval_O_=np.concatenate((band_interval_O_, [band_interval_O_[-1]+(band_interval_O_[1]-band_interval_O_[0])])) #add one more element to make intervals
    for i in range(len(band_interval_O_)-1):
        idx = np.logical_and(wavelength_sun >= band_interval_O_[i], wavelength_sun < band_interval_O_[i+1])
        E_bands.append(np.sum(I[idx]))

    return E_bands #Still match wavelength


def E_abs_O(E_bands, absorptivity_interval_mean, band_interval_O, O3_interp, z_interp, dz=1000):
    #They have matched wavelength
    E_layer_abs = np.zeros(len(z_interp))
    
    for i in range(len(band_interval_O)): #Calc energy absorped in each layer, with dz
        E_in=E_bands[i]
        E_layer_abs_interval=[]
        for j in range(len(z_interp)):
            tau=absorptivity_interval_mean[i]*O3_interp[len(z_interp)-1-j]*dz #start from 50 km downwards
            E_layer_abs_interval.append(E_in*(1-np.exp(-tau)))
            E_in=E_in-E_in*(1-np.exp(-tau))
        E_layer_abs=E_layer_abs+E_layer_abs_interval[::-1] #reverse the order to match altitude
    
    return E_layer_abs