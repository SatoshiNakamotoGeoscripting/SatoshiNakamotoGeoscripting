# Alex Levering, Hector Muro
# Team Satoshi Nakamoto
# 01/11/2017
# Case style: lowerCamelCase (both for variables and functions)
# Format style: K&R indentation

source('R/leapyear.R')

#Tests
isLeapYear(1820) # Expected output: TRUE
isLeapYear(2000) # Expected output: FALSE
isLeapYear(2002) # Expected output: FALSE
isLeapYear(1581) # Expected output: 1581 is before the beginning of the Gregorian calendar
isLeapYear("1581") # Expected output: Error in isLeapYear("1581") : Numeric input expected, got character