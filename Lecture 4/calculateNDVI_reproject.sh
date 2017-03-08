#!/bin/bash
#Team: Satoshi Nakamoto
#Date: 12 January 2017

#Computing NDVI
echo "Enter name of file"
read filename
echo "The input file: $filename"
ndvi="ndvi.tif"
echo "calculate ndvi"
gdal_calc.py -A $filename --A_band=4 -B $filename --B_band=3 --outfile=$ndvi --calc="(A.astype(float)-B)/(A.astype(float)+B)" --type='Float32'

#Resample to 60m
60fn="60m$filename.tif"
echo "Modify pixel size"
gdalwarp -tr 60 60 $ndvi $60fn

#Reproject to Lat/long WGS84 (EPSG: 4326)
reprfn="reprj$60fn.tf"
gdalwarp -t_srs EPSG:4326 $60fn $reprfn