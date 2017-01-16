#libraries
library(rgeos)
library(rgdal)
library(sp)
library(ggmap)
library(ggplot2)

#sources
source("R/preprocessing.R")
source("R/readShapefiles.R")
source("R/citiesCloseToRailType.R")
source("R/plot.R")

#download and unzip the Shapefiles
preprocessing()

#read the shapefiles
railways <- getSHP("data/railways","railways.shp")
places <- getSHP("data/places","places.shp")

#find the cities that are closer than 1000 to an industrial rail type
cities <- citiesCloseToRailType(railways, places, "industrial")

#Create a plot that shows the buffer, the points, and the name of the city
plot(cities)


