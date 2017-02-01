#Downloading, unpacking, preprocessing
dir.create('./data')
download.file(url = 'https://www.dropbox.com/s/akb9oyye3ee92h3/LT51980241990098-SC20150107121947.tar.gz?dl=0', 
              destfile = 'data/landsat5.tar.gz', method = 'wget')
download.file(url = 'https://www.dropbox.com/s/i1ylsft80ox6a32/LC81970242014109-SC20141230042441.tar.gz?dl=0#', 
              destfile = 'data/landsat8.tar.gz', method = 'wget')

#Unpack (untar) them and create a folder per each image
untar('landsat5.tar.gz',exdir='LT5')
untar('landsat8.tar.gz',exdir='LT8')
#exdir will create two folders containing the two Landsat images, in the working directory.

#Create Stacks from the multiple layers that have been unpacked
#Create two lists with the file names in order to create a stack/brick afterwards.
listLT5 <- list.files('./LT5' ,pattern = glob2rx('*.tif'), full.names = TRUE)
listLT8 <- list.files('./LT8' ,pattern = glob2rx('*.tif'), full.names = TRUE)

LT5stack <- stack(listLT5)
LT8stack <- stack(listLT8)