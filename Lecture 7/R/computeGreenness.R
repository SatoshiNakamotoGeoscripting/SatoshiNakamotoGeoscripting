library(raster)
library(rgdal)

computeGreenness <- function(filePrefix, administrativeRegion, level) {
  #Get modis data
  modisPath <- list.files(path = "data", pattern = glob2rx(paste(filePrefix,'.grd', sep = '*')), full.names = TRUE)
  modisLoaded <- brick(modisPath)

  #Load corresponding administrative data
  admin <- getData('GADM', country = administrativeRegion, level = level, path = "data")
  adminReprojected <- spTransform(admin, CRS(proj4string(modisLoaded)))
  
  #Find averages per municipality
  modisMasked <- mask(modisLoaded, mask = adminReprojected)
  greenValues <- extract(modisMasked, adminReprojected, fun="mean", df = FALSE, sp = TRUE, na.rm = TRUE)
  
  return(greenValues)
}

