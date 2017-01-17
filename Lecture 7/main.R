source('R/getData.R')
source('R/computeGreenness.R')
source('R/getGreenestInTimespan.R')
source('R/displayAdministrativeUnit.R')

preprocessData('https://raw.githubusercontent.com/GeoScripting-WUR/VectorRaster/gh-pages/data/MODIS.zip',
        'data',
        'MODIS.zip')

greenValues <- computeGreenness("MOD", "NLD", 2)

#For several months at once - add all months in a year to check the yearly average
greenestUnit <- getGreenestInTimespan(greenValues, c("May","June","July"))
displayAdministrativeUnit(greenestUnit, 2)