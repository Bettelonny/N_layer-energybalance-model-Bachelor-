
import matplotlib.pyplot as plt
import pandas as pd
def plot_layers(Temps):
    plt.figure(figsize=(6,4))
    plt.scatter(Temps,range(len(Temps)))
    plt.xlabel('Layer')
    plt.ylabel('Temperature (K)')
    plt.title('Temperature profile of the layers')
    plt.grid()
    plt.show()
    return

def plot_profile_atmosphere(Temps,height):
    plt.figure(figsize=(6,4))
    plt.plot(Temps,height/1000)
    plt.xlabel('Temperature (K)')
    plt.ylabel('Height (km)')
    plt.title('Temperature profile of the atmosphere')
    plt.grid()
    plt.show()
    return

#plot flux
def plot_flux(Flux_up,Flux_down,height):
    plt.figure(figsize=(6,4))
    plt.plot(Flux_up,height/1000,label='Upward flux')
    plt.plot(Flux_down,height/1000,label='Downward flux')
    plt.xlabel('Flux (W/m2)')
    plt.ylabel('Height (km)')
    plt.title('Flux profile of the atmosphere')
    plt.grid()
    plt.ylim(0,max(height)/1000)
    plt.xlim(min(min(Flux_up),min(Flux_down))-10,max(max(Flux_up),max(Flux_down))+10)
    plt.gca().invert_yaxis()
    plt.legend()
    plt.show()
    return

#spektrum plot
def plot_spectrum(wavelength,absorptivity):
    plt.figure(figsize=(6,4))
    plt.plot(wavelength, absorptivity)
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Absorptivity (m^2/molecule)')
    plt.title('Absorption Spectrum')
    plt.grid()
    plt.show()
    return

def plot_sun_spectrum(file="Spectra/Sun_spectra_TOA_1nm_1.csv"): #
    df = pd.read_csv(file)
    wavelength_sun=df["Wavelength(nm)"]
    I=df["I[w/(m^2*lambda)]"]
    plt.figure(figsize=(6,4))
    plt.plot(wavelength_sun, I)
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('I[w/(m^2*lambda)]')
    plt.title('Solar Spectrum at Top of Atmosphere')
    plt.grid()
    plt.show()
    return
    
def plot_E_abs_O(E_abs_O,z_interp):
    plt.figure(figsize=(6,4))
    plt.plot(E_abs_O,z_interp/1000)
    plt.xlabel('Absorbed Energy (W/m2)')
    plt.ylabel('Height (km)')
    plt.title('Energy absorbed by Ozone in the Atmosphere')
    plt.grid()
    plt.show()
    return
