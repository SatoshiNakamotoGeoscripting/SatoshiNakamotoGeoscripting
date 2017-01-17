source('R/getData.R')
source('R/computeGreenness.R')
source('R/getGreenestInTimespan.R')
source('R/displayAdministrativeUnit.R')

preprocessData('https://raw.githubusercontent.com/GeoScripting-WUR/VectorRaster/gh-pages/data/MODIS.zip',
        'data',
        'MODIS.zip')

greenValues <- computeGreenness("MOD", "NLD", 2)

#Plot for one month
greenestUnit <- getGreenestInTimespan(greenValues, c("May"))
displayAdministrativeUnit(greenestUnit, 2)

#For several months at once - add all months in a year to check the yearly average
greenestUnit <- getGreenestInTimespan(greenValues, c("May","June","July"))
displayAdministrativeUnit(greenestUnit, 2)

#For all months in the year
greenestUnit <- getGreenestInTimespan(greenValues, c("January","February","March","April","May","June","July","August","September","October","November","December"))

