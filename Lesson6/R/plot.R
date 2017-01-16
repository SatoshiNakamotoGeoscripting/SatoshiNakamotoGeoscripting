#plot

plot<-function(list){

  ggplot(data = cities$railBuffer,aes(x="latitude",y="longitude")) +
    
    geom_polygon(aes(x=cities$railBuffer@polygons[[1]]@Polygons[[1]]@coords[,1],
                     y=cities$railBuffer@polygons[[1]]@Polygons[[1]]@coords[,2]),
                 alpha = 0.5)+
    geom_point(aes(x=cities$intersectedPlaces@coords[,1], 
                   y=cities$intersectedPlaces@coords[,2]), 
               data = as.data.frame(coordinates(cities$intersectedPlaces)),
               size=7)+
    geom_label(aes(x=cities$intersectedPlaces@coords[,1], 
                   y=cities$intersectedPlaces@coords[,2]),
               label=cities$intersectedPlaces$name,
               col="black",
               vjust = "top",
               position = position_nudge(y=-100))
  
}