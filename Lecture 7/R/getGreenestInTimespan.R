library(raster)
library(rgdal)

getGreenestInTimespan <- function(greenValuesDF, months) {
  if(length(months) > 1){
    greenValuesDF@data$mean <- rowMeans(greenValuesDF@data[, months], na.rm=TRUE)
    greenestMunicipality <- greenValuesDF[which.max(greenValuesDF@data$mean), ]
  } else {
    greenestMunicipality <- greenValuesDF[which.max(greenValuesDF@data[, months]), ]
  }
  return(greenestMunicipality)
}

