# Alex Levering, Hector Muro
# Team Satoshi Nakamoto
# 01/13/2017

#NDVI calculator

ndviCalc <- function(red, nir) {
  ndvi <- (nir - red) / (nir + red)
  return(ndvi)
}