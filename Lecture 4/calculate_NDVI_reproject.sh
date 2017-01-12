#!/bin/bash
#Team: Satoshi Nakamoto
#Names: Alex Levering & Hector Muro
#Date: 12 January 2017

#Computing NDVI
echo "Enter name of file"
read filename
echo "The input file: $filename"
ndvi="ndvi"
echo "calculate ndvi"
gdal_calc.py -A $filename --A_band=4 -B $filename --B_band=3 --outfile=$ndvi --calc="(A.astype(float)-B)/(A.astype(float)+B)" --type='Float32'

#Resample to 60m
fn60="60m$filename"
echo "Modify pixel size"
gdalwarp -tr 60 60 $ndvi $fn60

#Reproject to Lat/long WGS84 (EPSG: 4326)
reprfn="reprj$fn60"
echo "Enter source EPSG (For this assignment: 32636)"
read srsEPSG
echo "Enter target EPSG (For this assignment: 4326)"
read trgEPSG
gdalwarp -s_srs EPSG:$srsEPSG -t_srs EPSG:$trgEPSG $fn60 $reprfn

rm "$ndvi"
rm  "$fn60"