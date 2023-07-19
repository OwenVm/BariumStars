import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from rv import radial_velocity, rv_error, remove_nans

id = input("Enter the star's program number: ")

hdul = fits.open(f'{id}_HRF_OBJ_ext_CosmicsRemoved_log_merged_cf.fits')

flux = hdul[0].data.T
L0 = hdul[0].header['CRVAL1']
step = hdul[0].header['CDELT1']

logL = np.linspace(L0, L0+len(flux)*step, len(flux))
lam = np.exp(logL)

flux_removed, wavelength_removed = remove_nans(flux)
wavelength_good = lam[wavelength_removed]
data = np.array([wavelength_good, flux_removed])

name = input("Enter the star's name (this will be the name of the asc file): ")

np.savetxt(f'{name}.asc', data.T, delimiter='\t')

v0 = 2*float(input("Enter the star's radial velocity in km/s from SIMBAD: "))

cutoff = 100
new_cuttof = input("Enter the cutoff value for the peak finding algorithm (standard 100): ")
if new_cuttof != '':
    cutoff = float(new_cuttof)

lines = [6546.238, 6569.214]
new_lines = input("If you want to use different lines, give name of the txt file: ") + ".txt"
if new_lines != '':
    lines = np.loadtxt(new_lines)

a, b = radial_velocity(lines, flux, lam, v0, cutoff)
c = rv_error(lines, flux, lam, v0, cutoff)

print(f'Radial velocities of the star in km/s: {b:.5f} pm {c:.5f}')

