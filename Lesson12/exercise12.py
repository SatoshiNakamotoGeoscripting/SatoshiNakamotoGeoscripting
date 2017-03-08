# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 11:51:06 2017

@author: Alex Levering und Hector Muro
"""
from __future__ import division
## Generic libraries

import numpy as np
import os
from os import makedirs, chdir
from os.path import exists
import tarfile
import fnmatch
import urllib

## Non-generic libraries
from osgeo import gdal
from osgeo.gdalconst import GA_ReadOnly, GDT_Float32
os.chdir('/home/user/Lesson12')


if not exists('./data'):
    makedirs('./data')

## Download data
def dataDownload(url,filename):
    urllib.urlretrieve(url,filename)

dataDownload('https://www.dropbox.com/s/zb7nrla6fqi1mq4/LC81980242014260-SC20150123044700.tar.gz?dl=1',
             'landsat.tar.gz')

## Untar files
def untarDirectory(directory):
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file,'*tar.gz'):
            tar = tarfile.open(file)
            tar.extractall(directory)
            tar.close()
untarDirectory('./data')

## Select bands
def bandSelection(band):
    for image in os.listdir('./data'):
        if fnmatch.fnmatch(image,'*'+band+'.tif'):
            gdalBand = gdal.Open('./data/'+image, GA_ReadOnly)
    return gdalBand

band4 = bandSelection('4')
band5 = bandSelection('5')
#type(band4)
## NDWI
def ndwi(band_A,band_B):
    # Read data into an array + set data type
    band_AArr = band_A.ReadAsArray(0,0,band_A.RasterXSize, band_A.RasterYSize).astype(np.float32)
    band_BArr = band_B.ReadAsArray(0,0,band_B.RasterXSize, band_B.RasterYSize).astype(np.float32)
    print type(band_BArr)
    
    # Derive the NDWI
    mask = np.greater(band_AArr+band_BArr,0)
    
    # set np.errstate to avoid warning of invalid values (i.e. NaN values) in the divide 
    with np.errstate(invalid='ignore'):
        ndwi = np.choose(mask,(-99,(band_AArr-band_BArr)/(band_AArr+band_BArr)))
    print "NDWI min and max values", ndwi.min(), ndwi.max()
    # Check the real minimum value
    print ndwi[ndwi>-99].min()
    
      
    # Write the result to disk
    driver = gdal.GetDriverByName('GTiff')
    outDataSet=driver.Create('./data/ndwi.tif', band_A.RasterXSize, band_A.RasterYSize, 1, GDT_Float32)
    outBand = outDataSet.GetRasterBand(1)
    outBand.WriteArray(ndwi,0,0)
    outBand.SetNoDataValue(-99)
    
    # set the projection and extent information of the dataset
    outDataSet.SetProjection(band_A.GetProjection())
    outDataSet.SetGeoTransform(band_A.GetGeoTransform())
        
    # Finally let's save it... or like in the OGR example flush it
    outBand.FlushCache()
    outDataSet.FlushCache()

ndwi(band4,band5)

## Reproject

bash = 'gdalwarp -t_srs "EPSG:4326" ./data/ndwi.tif ./data/ndwi_ll.tif'
os.system(bash)
