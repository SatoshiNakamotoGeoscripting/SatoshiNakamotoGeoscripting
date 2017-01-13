# Alex Levering, Hector Muro
# Team Satoshi Nakamoto
# 01/13/2017

#CleaningClouds

cleaningClouds <-function(stack,cloudlayernum){
  #We extract the layer that corresponds to the cloud mask.
  fmask <- stack[[cloudlayernum]]
  #We then delete this layer from our stack.
  LT_nocloud <- dropLayer(stack,cloudlayernum)
  
  #Function with the algorithm to clear out the clouds from an image
  cloud2NA <- function(x, y){
    x[y != 0] <- NA
    return(x)
  }
  #We use overlay while calling the function in order to keep more RAM free.
  LT_cloudfree <- overlay(x = LT_nocloud, y = fmask, fun = cloud2NA)
  
  #We associate the names from the stack without clouds layer to the new stack in order to keep track of them
  names(LT_cloudfree) = names(LT_nocloud)
  return(LT_cloudfree)
}
