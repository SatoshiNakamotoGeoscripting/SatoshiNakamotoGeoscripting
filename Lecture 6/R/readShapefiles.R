#Read shapefiles
getSHP <- function(path,shapefile){
  dsn = file.path(path,shapefile)
  shapefile <- readOGR(dsn,layer = ogrListLayers(dsn))
  return(shapefile)
}