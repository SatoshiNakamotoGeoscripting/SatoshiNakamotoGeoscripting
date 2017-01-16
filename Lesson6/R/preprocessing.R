#Unziping, preprocessing

preprocessing <- function(){
dir.create('./data')
download.file(url = 'http://www.mapcruzin.com/download-shapefile/netherlands-places-shape.zip', 
              destfile = 'data/netherlands-places-shape.zip', method = 'auto')
download.file(url = 'http://www.mapcruzin.com/download-shapefile/netherlands-railways-shape.zip', 
              destfile = 'data/netherlands-railways-shape.zip', method = 'auto')
### doesnt work at the moment!
unzip("data/netherlands-places-shape.zip",exdir="data/places")
unzip("data/netherlands-railways-shape.zip",exdir ="data/railways")
}
