
citiesCloseToRailType <- function(railwayData, placesData, railtype, bufferDistance = 1000){
  selectedRailType <- railways[railways$type==railtype, ]#the comma is necessary!

  #it is not projected (still in long/lat), so should we project it so that units are in m?
  prjStringRD <- CRS("+proj=sterea +lat_0=52.15616055555555 +lon_0=5.38763888888889 +k=0.9999079 +x_0=155000 +y_0=463000 +ellps=bessel +towgs84=565.2369,50.0087,465.658,-0.406857330322398,0.350732676542563,-1.8703473836068,4.0812 +units=m +no_defs")
  selectedRailTypeRD <- spTransform(selectedRailType, prjStringRD)
  
  railBuffer <- gBuffer(selectedRailTypeRD,byid=TRUE,width=bufferDistance)
  
  placesRD <- spTransform(placesData, prjStringRD)
  placesInRailBuffer <- as.data.frame(gIntersects(railBuffer, placesRD, byid=TRUE))
  
  names(placesInRailBuffer) <- "intersect"
  placesRD@data$intersect <- placesInRailBuffer$intersect
  
  intersectedPlaces <- placesRD[placesRD@data$intersect == TRUE, ]
  returnList <- list("intersectedPlaces"=intersectedPlaces,"railBuffer"=railBuffer)
  
  return(returnList)
}