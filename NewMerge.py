import pandas as pd
import numpy as np
import argparse
import textwrap
import numpy as np
from astropy.io import fits

parser = argparse.ArgumentParser(description="Merges spectra and converts it to ASCII file",
                                epilog=textwrap.dedent(''' 
                                run as "python3 Merge.py "unseq1, unseq2, ..." "rv1, rv2, ..." <name of output ascii file>"
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

def convert_spectrum(file, rv):
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
    data = np.array([shifted_wavelengths, flux_good])

    return data

def check_compatibility(data):

    first_elements = np.array([data[i][0] for i in range(len(data))])
    max_first = np.argmax(first_elements)

    last_elements = np.array([data[i][-1] for i in range(len(data))])
    min_last = np.argmin(last_elements)

    diffs_min = np.array([data[i] - data[max_first][0] for i in range(len(data))] ,dtype = object)
    diffs_max = np.array([data[i] - data[min_last][-1] for i in range(len(data))] ,dtype = object)

    indices_min = np.array([np.argmin(np.abs(diff)) for diff in diffs_min])
    indices_max = np.array([np.argmin(np.abs(diff)) for diff in diffs_max])

    return indices_min, indices_max

def merge(out, files, rv):

    spectra = [convert_spectrum(f'0{unseqs[i]}_HRF_OBJ_ext_CosmicsRemoved_log_merged_cf.fits', rv[i]) for i in range(len(files))]

    wavelengths = [spectrum[0] for spectrum in spectra]
    flux = [spectrum[1] for spectrum in spectra]

    Left_indices, Right_indices = check_compatibility(wavelengths)

    print(Left_indices)
    print(Right_indices)

    lengths = Right_indices - Left_indices
    min_length = np.min(lengths)

    new_wavelength = np.array([wavelengths[i][Left_indices[i]:Left_indices[i] + min_length] for i in range(len(wavelengths))]) 
    new_flux = np.array([flux[i][Left_indices[i]:Left_indices[i] + min_length] for i in range(len(flux))])

    NewSpectra = np.sum(new_flux, axis = 0)
    new_data = np.array([new_wavelength[0], NewSpectra], dtype = object)
    return output(out, new_data)
    
def output(out, data):
    np.savetxt(out, data.T, delimiter="\t")

if __name__ == "__main__":

    print(unseqs)
    print(rv)

    merge(f'{out}.asc', unseqs, rv)