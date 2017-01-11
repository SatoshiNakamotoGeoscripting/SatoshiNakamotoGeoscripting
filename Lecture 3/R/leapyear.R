# Alex Levering, Hector Muro
# Team Satoshi Nakamoto
# 01/11/2017
# Case style: lowerCamelCase (both for variables and functions)
# Format style: K&R indentation

# Source: http://www.mathsisfun.com/leap-years.html
# Leap Years are any year that can be evenly divided by 4 (such as 2012, 2016, etc)
#   not if it can be evenly divided by 100, then it isn't (such as 2100, 2200, etc)
#     yes if it can be evenly divided by 400, then it is (such as 2000, 2400)

isLeapYear <- function(year) {
  #Check whether the number is greater than the first date of the Gregorian calendar
  if (is.numeric(year)) {
    if (year >= 1582) {
      # Condition 1 before OR statement: Check if year can be divided by 400 and not by 100
      # Condition 2 after the OR statement: Check if year can be divided by 4 and by 400
      isLeap <- ifelse(year %% 4 == 0 & year %% 100 != 0 | year %% 4 == 0 & year %% 400 == 0, TRUE, FALSE)
      return(isLeap)
    } else {
      stop(year, " is before the beginning of the Gregorian calendar")
    }
  } else {
    stop("Numeric input expected, got ", class(year))
  }
}