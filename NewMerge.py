import pandas as pd
import numpy as np
import argparse
import textwrap
import numpy as np
from astropy.io import fits

parser = argparse.ArgumentParser(description="Merges spectra and converts it to ASCII file",
                                epilog=textwrap.dedent(''' 
                                run as "python3 Merge.py <unseq> <amount of spectra> <name of output ascii file>"
                                ''')
                            )
parser.add_argument("input", type=str, help="List of unseqs of all spectra")
parser.add_argument("input2", type=str, help="Radial velocity of all spectra in the correct order in km/s")
parser.add_argument("output", type=str, help="Name of output file")
args = parser.parse_args()


unseqs = np.array([int(i) for i in args.input.split(',')])
rv = np.array([float(i) for i in args.input2.split(',')])
out = args.output


def doppler_shift(wavelengths, rv):
    c = 299792.458
    return wavelengths * np.sqrt((1 - rv/c)/(1 + rv/c))

def convert_spectrum(file):
    hdul = fits.open(file)

    flux = hdul[0].data.T
    L0 = hdul[0].header["CRVAL1"]
    step = hdul[0].header["CDELT1"]

    logL = np.linspace(L0, L0 + len(flux) * step, len(flux))
    lam = np.exp(logL)

    mask = np.isnan(flux)

    wavelength_good = lam[~mask]
    shifted_wavelengths = doppler_shift(wavelength_good, rv)

    flux_good = flux[~mask]
    data = np.array([shifted_wavelength, flux_good])

    return data

def check_compatibility(data):
    pass

def merge(out, files):
    spectra = [convert_spectrum(f'0{id}_HRF_OBJ_ext_CosmicsRemoved_log_merged_cf.fits') for id in files]

    wavelengths = [spectrum[0] for spectrum in spectra]
    flux = [spectrum[1] for spectrum in spectra]

    #if check_compatibility(wavelengths):

    NewSpectra = np.sum(flux, axis=0)

    data = np.array([wavelengths[0], NewSpectra])
    return output(out, data)
    
def output(out, data):
    np.savetxt(out, data.T, delimiter="\t")


if __name__ == "__main__":

    print(unseqs)
    print(rv)

    merge(f'{out}.asc', files)