import numpy as np

def remove_nans(flux):
    '''
    removes all the nans from flux and returns the flux and the indexes of the non nans
    '''
    indexes = []
    for i in range(len(flux)):
        if ~np.isnan(flux[i]):
            indexes.append(i)
    return flux[indexes], indexes

def radial_velocity_shift(lam, lam0):
    ''' 
    lam: observed wavelength of peak
    lam0: rest wavelength of peak
    returns velocity of the star in km/s
    '''
    c = 299792.458 # km/s
    return c*(lam-lam0)/lam0

def local_continuum(flux, lam, lam_lower, lam_upper):
    ''' 
    lam_lower: lower bound of the wavelength range of the peak of interest, assuming initial guess for v0
    lam_upper: upper bound of the wavelength range of the peak of interest, assuming initial guess for v0
    returns the median of the flux in the wavelength range
    '''
    return np.median(flux[(lam>lam_lower) & (lam<lam_upper)])

def find_peak(flux, lam, lam0, v0, cutoff):
    '''
    returns the observed wavelength of the peak
    '''
    lam_lower = lam0*(1-v0/299792)
    lam_upper = lam0*(1+v0/299792)
    lc = local_continuum(flux, lam, lam_lower, lam_upper)
    wavelength_range = lam[np.where((lam>lam_lower) & (lam<lam_upper))]
    
    peak = []
    indexes = []
    for i in wavelength_range:
        flux_value = flux[np.where(lam==i)]
        if np.abs(flux_value - lc) > cutoff:
            peak.append(i)
            indexes.append(np.where(lam==i)[0][0])
    
    '''for i in range(len(peak)-1):
        if np.where(lam==peak[i])[0][0] - np.where(lam==peak[i+1])[0][0] != 1:
            print("Multiple peaks found")
            return'''

    if len(peak) == 0:
        print('No peak found, maybe increase v0 or decrease the cutoff.')
        return None
    
    return lam[np.where(flux==min(flux[indexes]))[0]][0]
        
def find_rv_peak(flux, lam, lam0, v0, cutoff):
    '''
    returns the radial velocity of the star in km/s
    '''
    observed = find_peak(flux, lam, lam0, v0, cutoff)
    if observed is None:
        return None
    return radial_velocity_shift(observed, lam0)

def radial_velocity(lines, flux, lam, v0, cutoff):
    '''
    lines: list of rest wavelengths of the peaks of interest in angstrom
    flux: flux of the star, arbitrary units
    lam: wavelength values of the spectrum in angstrom
    v0: initial guess of the radial velocity of the star in km/s (for example from SIMBAD)
    cutoff: cutoff value for the peak, the higher the value, the more sensitive the peak finding algorithm
    returns the radial velocities of the star in km/s for each peak and the mean radial velocity
    '''
    rv = []
    for line in lines:
        rv_new = find_rv_peak(flux, lam, line, v0, cutoff)
        if rv_new is not None:
            rv.append(rv_new)
    return rv, np.mean(rv)

def rv_error(lines, flux, lam, v0, cutoff):
    '''
    lines: list of rest wavelengths of the peaks of interest in angstrom
    flux: flux of the star, arbitrary units
    lam: wavelength values of the spectrum in angstrom
    v0: initial guess of the radial velocity of the star in km/s (for example from SIMBAD)
    cutoff: cutoff value for the peak, the higher the value, the more sensitive the peak finding algorithm
    uses error propagation to calculate the error of the radial velocity, given a list of radial velocities from different lines
    '''
    rv, mean = radial_velocity(lines, flux, lam, v0, cutoff)
    return np.sqrt(np.sum((rv-mean)**2)/(len(rv)-1))
