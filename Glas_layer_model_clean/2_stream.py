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
    band_interval_O = np.arange(Bandends[0],Bandends[1]+1,Bandwidth)
    idx_old=0
    for nm in band_interval_O:
        idx = np.abs(wavelength - nm).argmin()
        absorptivity_interval_mean.append(np.mean(abs_253K[idx_old:idx]))
        idx_old=idx
    return band_interval_O, absorptivity_interval_mean

def Ozone_concentration_profile(z_interp):
    #z_interp in m
    #Read standard atmosphere data
    df = read_atmosphere(file="Standard_Atmospheres/us_standard.csv")
    z = df['Altitude(m)'].values  # Altitude in meters
    O3 = df['O3(molec/cm^3)'].values * 1e6  # Convert from molec/cm^3 to molec/m^3

    # Interpolate O3 concentration to the new z grid
    O3_interp = np.interp(z_interp, z, O3)
    return O3_interp

def Sun_E_bands(file="Sun_spectra_TOA_1nm_1.csv", Bandends=[220,1100],Bandwidth=10): #
    band_interval_O = np.arange(Bandends[0],Bandends[1]+1,Bandwidth)
    df = pd.read_csv(file)
    wavelength_sun=df["Wavelength(nm)"]
    I=df["I[w/(m^2*lambda)]"]

    # Match the solar spectrum to the ozone absorption bands
    E_bands = []
    for i in range(len(band_interval_O)-1):
        idx = np.logical_and(wavelength_sun >= band_interval_O[i], wavelength_sun < band_interval_O[i+1])
        E_bands.append(np.sum(I[idx]))

    return E_bands

def E_abs_O(E_bands, absorptivity_interval_mean, O3_interp, z_interp):
    #Calculate the absorbed energy by ozone in each layer and band
    #E_bands in W/m^2 for each band
    #absorptivity_interval_mean in m^2/molecule for each band
    #O3_interp in molec/m^3 for each layer
    #z_interp in m for each layer

    #Calculate the thickness of each layer
    dz = np.diff(z_interp, prepend=0)  # Thickness of each layer in meters

    # Initialize the absorbed energy array
    E_abs = np.zeros((len(z_interp), len(E_bands)))  # Absorbed energy in W/m^2 for each layer and band

    # Calculate absorbed energy for each layer and band
    for i in range(len(z_interp)):
        for j in range(len(E_bands)):
            # Beer-Lambert law: I = I0 * exp(-alpha * c * dz)
            alpha = absorptivity_interval_mean[j]  # Absorptivity in m^2/molecule
            c = O3_interp[i]  # O3 concentration in molec/m^3
            I0 = E_bands[j]  # Incident energy in W/m^2
            I = I0 * np.exp(-alpha * c * dz[i])  # Transmitted energy
            E_abs[i, j] = I0 - I  # Absorbed energy in W/m^2
            # Calculate transmitted energy through the layer