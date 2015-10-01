"""
This script shows how to use our GalSim interface to create FITS images
that contain stars and galaxies
"""

import os
import galsim
from lsst.sims.catalogs.generation.db import CatalogDBObject
from lsst.sims.utils import ObservationMetaData
from lsst.sims.catUtils.baseCatalogModels import StarObj, GalaxyBulgeObj, GalaxyDiskObj, GalaxyAgnObj, \
                                                 OpSim3_61DBObject
from lsst.sims.GalSimInterface import SNRdocumentPSF, GalSimStars, GalSimGalaxies, GalSimAgn
from myana import *

#if you want to use the actual LSST camera
#from lsst.obs.lsstSim import LsstSimMapper

class testGalSimStars(GalSimStars):
    #only draw images in the u and g band for speed
    bandpassNames = ['u','g','r','z']

    #convolve with a PSF; note that galaxies are not convolved with a PSF
    #PSF defined in galSimInterface/galSimUtilities.py
    PSF = SNRdocumentPSF()

    #If you want to use the LSST camera, uncomment the line below.
    #You can similarly assign any camera object you want here
    #camera = LsstSimMapper().camera

class testGalSimGalaxies(GalSimGalaxies):
    bandpassNames = ['u','g','r','z']

    PSF = SNRdocumentPSF()

    #If you want to use the LSST camera, uncomment the line below.
    #You can similarly assign any camera object you want here
    #camera = LsstSimMapper().camera




class testGalSimAgn(GalSimAgn):
    bandpassNames = ['u','g','r','z']

    #defined in galSimInterface/galSimUtilities.py
    PSF = SNRdocumentPSF()

    #If you want to use the LSST camera, uncomment the line below.
    #You can similarly assign any camera object you want here
    #camera = LsstSimMapper().camera



#select an OpSim pointing
obsMD = OpSim3_61DBObject()
obs_metadata = obsMD.getObservationMetaData(88625744, 0.05, makeCircBounds = True)

catName = './outputs_cats/galSim_galaxies_example.txt'

bulges = CatalogDBObject.from_objid('galaxyBulge')
bulge_galSim = testGalSimGalaxies(bulges, obs_metadata=obs_metadata, column_outputs=['redshift'])
bulge_galSim.noise_and_background = None
bulge_galSim.PSF = None
bulge_galSim.write_catalog(catName, write_header=True, write_mode='a')

print 'done with bulges'

disks = CatalogDBObject.from_objid('galaxyDisk')
disk_galSim = testGalSimGalaxies(disks, obs_metadata=obs_metadata, column_outputs=['redshift'])
disk_galSim.copyGalSimInterpreter(bulge_galSim)
disk_galSim.noise_and_background = None
disk_galSim.PSF = None
disk_galSim.write_catalog(catName, write_header=True, write_mode='a')

print 'done with disks'

agn = CatalogDBObject.from_objid('galaxyAgn')
agn_galSim = testGalSimAgn(agn, obs_metadata=obs_metadata, column_outputs=['redshift'])
agn_galSim.copyGalSimInterpreter(disk_galSim)
agn_galSim.noise_and_background = None
agn_galSim.PSF = None
agn_galSim.write_catalog(catName, write_header=True, write_mode='a')

agn_galSim.write_images(nameRoot='./outputs_fits/galaxy')

print 'done with galaxyAgn'