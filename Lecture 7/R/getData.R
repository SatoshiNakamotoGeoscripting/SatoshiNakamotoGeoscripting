preprocessData <- function(url,destdir,file){
  ifelse (!dir.exists(destdir), dir.create(destdir), FALSE)
  destfile=paste0(destdir, '/', file)
  download.file(url=url, destfile=destfile, method='auto')
  unzip(destfile, exdir=destdir)
}