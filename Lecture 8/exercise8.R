## Import libraries
library(randomForest)
library(raster)

## Import data
load("data/GewataB1.rda")
load("data/GewataB2.rda")
load("data/GewataB3.rda")
load("data/GewataB4.rda")
load("data/GewataB5.rda")
load("data/GewataB7.rda")
load("data/vcfGewata.rda")


## Build a brick containing all data
vcfGewata[vcfGewata > 100] <- NA
alldata <- brick(GewataB1, GewataB2, GewataB3, GewataB4, GewataB5, GewataB7, vcfGewata)
names(alldata) <- c("band1", "band2", "band3", "band4", "band5", "band7", "VCF")

## Exploratory plots
pairs(alldata)
hist(alldata, xlim = c(0, 3000), ylim = c(0, 750000))#, breaks = seq(0, 500, by = 100))

## Extract all data to a data.frame
df <- as.data.frame(getValues(alldata))

## Calibrate linear model
## Footnote: better reuslts might be achievable when removing bands from this list
## However, we did not do so to preserve the assignment.
model <- lm(VCF ~ df$band1 + df$band2 + df$band3 + df$band4 + df$band5 + df$band7, data = df)
step(model) #more statistics of the model

##Then we extract the coefficient of determination
summary(model)$r.squared

## Use the model to predict land cover
lcMap <- predict(model,df)

## Grab the results of band 1
predictedRaster <- alldata$band1
predictedRaster$predictedVCF <- lcMap
predictedRaster <- predictedRaster$predictedVCF

## Assign nodata to incorrect values
predictedRaster[predictedRaster < 0] <- NA

#Plot the predicted tree cover raster and compare with the original VCF raster
opar <- par(mfrow=c(1, 2)) 
plot(predictedRaster, main="Predicted VCF")
plot(alldata$VCF, main="Original VCF")
par(opar)

#Compute the RMSE between your predicted and the actual tree cover values
#RMSE
predictedRasterDF <- as.data.frame(predictedRaster) #we need a DataFrame to operate with its values
sqrt(mean((predictedRasterDF$predictedVCF-df$VCF)^2, na.rm = TRUE ))



##Are the differences between the predicted and actual tree cover the same for all
##of the 3 classes we used for the Random Forest classfication?
##Using the training polygons from the random forest classification, 
#calculate the RMSE separately for each of the classes and compare
load("data/trainingPoly.rda")
trainingPoly@data$Code <- as.numeric(trainingPoly@data$Class)
trainingPoly@data$Class #1 is cropland, 2 is forest and 3 is wetland

## Rasterize polygon classes
classes <- rasterize(trainingPoly,predictedRaster, field='Code')
names(classes) <- "class"

## Create zonal statistics
predictedRasterBrick <- brick(predictedRaster,alldata$VCF)
zonalStatistics<-zonal(predictedRasterBrick, classes, fun='mean')

## Convert and display computed RMSE's per class
## Class 1 is cropland, class 2 is forest, class 3 is wetland
zonalStatisticsDF <- as.data.frame(zonalStatistics)
predictedRasterBrickDF <- as.data.frame(predictedRasterBrick)
sqrt((zonalStatisticsDF$predictedVCF-zonalStatisticsDF$VCF)^2)#, na.rm = TRUE)
  
  
