## Libraries
library(raster)
## Load data
load("data/GewataB2.rda")
load("data/GewataB3.rda")
load("data/GewataB4.rda")

## Check out the attributes
GewataB2
## Some basic statistics using cellStats()
cellStats(GewataB2, stat=max)
cellStats(GewataB2, stat=mean)
# This is equivalent to:
maxValue(GewataB2)
## What is the maximum value of all three bands?
max(c(maxValue(GewataB2), maxValue(GewataB3), maxValue(GewataB4)))
## summary() is useful function for a quick overview
summary(GewataB2)

## Put the 3 bands into a RasterBrick object to summarize together
gewata <- brick(GewataB2, GewataB3, GewataB4)
# 3 histograms in one window (automatic, if a RasterBrick is supplied)
hist(gewata)