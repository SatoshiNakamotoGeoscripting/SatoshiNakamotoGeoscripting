#Set and check your working directory if necessary
setwd("/home/user/Lesson5")
getwd()

#Import libraries
library(raster)

#Sources

source('R/cleaningClouds.R')
source('R/ndvi.R')




#1st!!!
#Download the files from the browser
download.file(url = 'https://www.dropbox.com/s/akb9oyye3ee92h3/LT51980241990098-SC20150107121947.tar.gz?dl=0', 
              destfile = 'landsat5.tar.gz', method = 'wget')
download.file(url = 'https://www.dropbox.com/s/i1ylsft80ox6a32/LC81970242014109-SC20141230042441.tar.gz?dl=0#', 
              destfile = 'landsat8.tar.gz', method = 'wget')

#Unpack (untar) them and create a folder per each image
untar('landsat5.tar.gz',exdir='LT5')
untar('landsat8.tar.gz',exdir='LT8')

#Create two lists with the file names in order to create a stack/brick afterwards
#If full.names = TRUE, names are stored with the whole path (NECESSARY?)
#Else only the file name
getwd()
listLT5 <- list.files('./LT5' , 
                      pattern = glob2rx('*.tif'), full.names = TRUE)
listLT8 <- list.files('./LT8' , 
                      pattern = glob2rx('*.tif'), full.names = TRUE)

#2nd!!!! CREATE STACKS!
LT5stack <- stack(listLT5)
LT8stack <- stack(listLT8)
listLT8

#3rd!!! Cleaning the clouds
#We call the function to clean the clouds from each raster. The inputs are the raster and the number of the layer which corresponds to the clouds one

LT5_nocloud<-cleaningClouds(LT5stack,1)
LT8_nocloud<-cleaningClouds(LT8stack,1)


plotRGB(LT8_nocloud,4,5,6)

# 4th Applying NDVI
#We call the function NDVI which has as inputs the red and NIR bands for every image.

#LT5_nocloud
#LT8_nocloud
LT5_ndvi <- ndvCalc(LT5_nocloud[[6]],LT5_nocloud[[7]])
plot(LT5_ndvi)
LT8_ndvi <- ndvCalc(LT8_nocloud[[4]],LT8_nocloud[[5]])
plot(LT8_ndvi)

#I try to plot a combination of bands, but I keep receiving this error "color intensity -0.0009375, not in [0,1]"
#It means the raster itself has negative values (?¿?¿), could not find a way to fix it.
#Therefore I plot single bands.

#




