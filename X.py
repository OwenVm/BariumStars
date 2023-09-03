#This script creates a list of HERMES spectra given a star and/or program number
#and can also retrieve spectra to the output directory specified by the user
#############################################################################
import numpy as np
from astropy.io import fits
import pandas as pd
from pathlib import Path
import os
from ivs.catalogs import sesame
import sys
import shutil
############################################################################
def retrieve_file(unseq,Night,Destdir):
    filename = HermesPath.joinpath(str(Night),'reduced', f'00{unseq}_HRF_OBJ_ext_CosmicsRemoved_log_merged_cf.fits')
    print(filename.as_posix())
    FilePath = Destdir.joinpath(f'00{unseq}_HRF_OBJ_ext_CosmicsRemoved_log_merged_cf.fits')
    if not FilePath.is_file():
        try:
            shutil.copy(filename.as_posix(),Destdir.as_posix())
            print(f'Copied {filename.as_posix()} to {Destdir.as_posix()}')
        except Exception as e:
            print(str(e))
    else:
        print('File already copied!')
############### DEFAULTS ###########################
limit = 0.002777778 #this is 10 arcsec
conv=np.pi/180
progid=None
calibration='CALIBRATION'
retrieve=True #True if you want to retrieve spectra to outpath
###########################################################
#First, we get in the arguments from the user
args=sys.argv
if (len(args) > 1):
    for k in np.arange(1,len(args)):
        if(args[k] == "-s"):
            searchterm = str(sys.argv[k+1]).strip()
            print(f'Searching for {searchterm}')
            info=sesame.search(searchterm)
            print(f'Search complete')
            try:
                ra = info['jradeg']
                dec=info['jdedeg']  	
                print(f'ra = {ra}')
                print(f'dec = {dec}')
            except:
                print('Not resolved by simbad')
                ra=0
                dec=0
        if(args[k] == "-p"):
            progid = int(sys.argv[k+1])
        if (args[k] == "-r"):
            limit = float(sys.argv[k+1])

            print(f'ra = {ra}')
            print(f'dec = {dec}')
else:
    #    #   no parameters received from the command line, give help.
   print('''USAGE  : python MakeListStar_Karan.py -s <objectsearch>  [-r <searchradius_in_degrees>] -p <program_id>

            -s: name which will be understood by SIMBAD e.b. BD+39_4926 or hd_213985
            take care to replace spaces with _")
            -r: search radius is degrees. The objects are looked for within this searchradius from the simbad entry
                the default is 10 arcseconds
            -p: search for all entries of that program id''')
   sys.exit()

################# DIRECTORIES ######################
basedir=Path.cwd()
HermesPath=Path('/STER/mercator/hermes')
#Keep outpath = basedir if you want the output in current working directory,
#otherwise it creates a subfolder
outpath=basedir.joinpath(searchterm)
#################################################
#open the master file with pandas
print('Reading in /STER/mercator/hermes/HermesFullDataOverview.tsv')
data = pd.read_csv("/STER/mercator/hermes/HermesFullDataOverview.tsv",sep='\t',skiprows=2)
print("Done!")
header = ['unseq', 'prog_id', 'obsmode', 'bvcor', 'observer', 'object', 'ra','dec', 'bjd', 'exptime', 'pmtotal', 'date-avg', 'airmass','filename']
data.columns=header

#If resolved by simbad, then use the coordinates to search, else use the searchterm and/or prog id
if ra:
    distance=np.sqrt(((data['ra']-ra)*np.cos(ra*conv))**2 + (data['dec']-dec)**2)
    if not progid:
        data_filtered =data.loc[(distance<limit) & (data['object']!=calibration)]
    else:
        data_filtered =data.loc[(distance<limit) & (data['prog_id']==progid) & (data['object']!=calibration)]
else:
    if not progid:
        data_filtered =data.loc[(data['object']==searchterm) | (searchterm in data['object']) & (data['object']!=calibration)]
    else:
        data_filtered =data.loc[(data['object']==searchterm) | (searchterm in data['object']) & (data['prog_id']==progid) & (data['object']!=calibration)]

#get a nights column so it's easier to save
nights =[data_filtered['filename'].values[i].split('/')[4] for i in range(len(data_filtered))]
data_filtered=data_filtered.assign(night=nights)

cols_to_save = ['unseq','date-avg','object','bjd','bvcor','prog_id','exptime','airmass','pmtotal','night']

outpath.mkdir(exist_ok=True)
#filelist=outpath.joinpath(f'{searchterm}.list')
base = Path.cwd()
base2 = base.joinpath('./Lists')
filelist=base2.joinpath(f'{searchterm}.list')

data_filtered.to_csv(path_or_buf=filelist,index=False,columns=cols_to_save,sep='\t')
print(f'Saved data to {filelist}')

if retrieve:
    for i,row in data_filtered.iterrows():
        retrieve_file(row['unseq'],row['night'],outpath)
else:
    print('Did not retrieve data')
