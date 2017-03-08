# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 09:08:21 2099

@author: Hector Muro, Alex Levering
Team: Satoshi Nakamoto
"""
## Standard libraries
from os import makedirs, chdir
from os.path import exists
from numpy import mean

## Non-standard libraries
from osgeo import ogr,osr
import simplekml
import folium

#Create data folder if it does not exist
if not exists('./data'):
    makedirs('./data')

# Move over to data directory
chdir('./data')

## Is the ESRI Shapefile driver available?
driverName = "ESRI Shapefile"
drv = ogr.GetDriverByName( driverName )
if drv is None:
    print "%s driver not available.\n" % driverName
else:
    print  "%s driver IS available.\n" % driverName

#Exports list of tuples/lists with WGS coordinates and gives a shp and optionally a kml as output
def shpFromPoints(filename, layername, points, save_kml = True):
    #Initialize all the variables needed to set up a SHP
    spatialReference = osr.SpatialReference()
    spatialReference.ImportFromProj4('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
    ds = drv.CreateDataSource(filename)
    layer=ds.CreateLayer(layername, spatialReference, ogr.wkbPoint)
    layerDefinition = layer.GetLayerDefn()
    
    point = ogr.Geometry(ogr.wkbPoint)
    feature = ogr.Feature(layerDefinition)
    
    kml = simplekml.Kml()
    for i, value in enumerate(points): #For each coordinate, add to shp and to the kml if save kml is true
        point.SetPoint(0,value[0], value[1])
        feature.SetGeometry(point)
        layer.CreateFeature(feature)
        if save_kml == True:
            kml.newpoint(name=str(i), coords = [(value[0],value[1])])
    ds.Destroy()        
    if save_kml == True:
        kml.save("my_points.kml")

#Creates a folium HTML with lat/long as iframe popups
def mapFromPoints(pts, outname, zoom_level, save = True, tiles = 'Stamen Terrain'):
    #Get the center of the map by deriving the mean of all lats/longs
    mean_long = mean([pt[1] for pt in pts])
    mean_lat = mean([pt[0] for pt in pts])
    point_map = folium.Map(location=[mean_long, mean_lat], zoom_start = zoom_level, tiles = tiles)
    for pt in pts:
        folium.Marker([pt[1], pt[0]],\
        popup = folium.Popup(folium.element.IFrame(
        html='''
                <b>Latitude:</b>  {lat}<br>
                <b>Longitude:</b> {lon}<br>
             '''.format(lat = pt[1], lon = pt[0]),\
        width=150, height=100),\
        max_width=150)).add_to(point_map)
    if save == True:
        point_map.save("{}.html".format(outname))
    return point_map

filename = "wageningenpoints.shp"
layername = "wagpoints"
pts = [ (5.665777, 51.987398),
        (5.663133, 51.978434),
        (5.663148, 51.988434) ]
               
shpFromPoints(filename, layername, pts)
mapFromPoints(pts, "satoshinakamoto", zoom_level = 13, tiles = 'openstreetmap')#, marker_icon = 'cloud')
