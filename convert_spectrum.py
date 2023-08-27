import argparse

import numpy as np
from astropy.io import fits

parser = argparse.ArgumentParser(description="Convert fits to ASCII file")
parser.add_argument("input", type=str, help="parameter file")
parser.add_argument("output", type=str, help="map voor .vtu files")
args = parser.parse_args()

file = args.input
out = args.output

hdul = fits.open(file)

flux = hdul[0].data.T
L0 = hdul[0].header["CRVAL1"]
step = hdul[0].header["CDELT1"]

logL = np.linspace(L0, L0 + len(flux) * step, len(flux))
lam = np.exp(logL)

mask = np.isnan(flux)

wavelength_good = lam[~mask]
flux_good = flux[~mask]
data = np.array([wavelength_good, flux_good])


np.savetxt(out, data.T, delimiter="\t")
