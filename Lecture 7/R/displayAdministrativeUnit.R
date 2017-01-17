library(rgeos)
library(ggplot2)

displayAdministrativeUnit <-function(greenestUnit, level){
  name <- paste0('NAME_', level)
  centroid = gCentroid(greenestUnit,byid=TRUE)
  ggplot(data = greenestUnit, aes(x = "latitude", y = "longitude")) +
    
    geom_polygon(aes(x = greenestUnit@polygons[[1]]@Polygons[[1]]@coords[,1],
                     y = greenestUnit@polygons[[1]]@Polygons[[1]]@coords[,2]),
                 alpha = 0.5,
                 fill = "#0e5311",
                 col = "black")+
    geom_label(aes(x = centroid@coords[,1],
                   y = centroid@coords[,2]),
               label = greenestUnit@data[,name],
               col = "black")+
    #For lack of time, the exact administrative unit was not derived from the data
    ggtitle("Greenest administrative unit of the Netherlands")
}
