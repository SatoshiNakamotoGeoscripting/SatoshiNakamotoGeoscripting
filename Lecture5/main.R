# Alex Levering, Hector Muro
# Team Satoshi Nakamoto
# 01/13/2017

#Set and check your working directory if necessary
setwd("/home/user/mytest/Lecture5")
getwd()

#Import libraries
library(raster)

#Sources
source('R/cleaningClouds.R')
source('R/ndvi.R')

# 1st: Download the files from the browser & Unpack them

source('R/preproces.R')

# Plotting clouds mask for both images. 
plot(LT5stack[[1]], main="Clouds mask in Landsat TM 5 image, 1990")
plot(LT8stack[[1]], main="Clouds mask in Landsat OLI image, 2014")

# 2nd: Cleaning the clouds. We use the first layer from the rasters, which contains the clouds mask that will be used 
#to clear out the clous from all the layers.
#We call the function that uses an algorithm found in the tutorial. 
#The inputs are the raster and its position in the whole range of layers.

LT5_nocloud<-cleaningClouds(LT5stack,1)
LT8_nocloud<-cleaningClouds(LT8stack,1)
#LT5_nocloud

####I try to plot a combination of bands (RGB), but I keep receiving this error "color intensity -0.0009375, not in [0,1]"
####It means the raster itself has negative values (?¿?¿), could not find a way to fix it.
####Therefore I plot single bands.

plot(LT5_nocloud[[2]])
plot(LT8_nocloud[[2]])

# 3rd: Applying NDVI
#We call the function NDVI which has as inputs the red and NIR bands for every image.
#We use overlay in order to keep more RAM free.

LT5_ndvi <- overlay(LT5_nocloud[[5]],LT5_nocloud[[6]],fun=ndviCalc)
plot(LT5_ndvi, main="NDVI for Landsat TM 5, 1990")
LT8_ndvi <- overlay(LT8_nocloud[[4]],LT8_nocloud[[5]],fun=ndviCalc)
plot(LT8_ndvi, main="NDVI for Landsat 8 OLI, 2014")

# 4th: Intersect both imagesto keep with the piece they share so they can be substracted (croping)
LT5_crop <- intersect(LT5_ndvi,LT8_ndvi)
LT8_crop <- intersect(LT8_ndvi,LT5_ndvi)

# 5th: Substraction. By substracting we will be able to see those parts of the image where the NDVI has increased or decreased.
NDVI_dif = LT8_crop - LT5_crop
plot(NDVI_dif, main="Difference between 2014's NDVI and 1990's NDVI")

#We create a raster from the last calculation
dir.create('./output')
writeRaster(x=NDVI_dif, filename="output/NDVI_differences.tif", datatype='FLT4S',overwrite= TRUE)
