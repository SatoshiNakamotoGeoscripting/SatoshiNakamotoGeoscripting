# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 09:08:21 2099

@author: Hector Muro, Alex Levering
Team: Satoshi Nakamoto
"""
## Loading the modules
from osgeo import ogr,osr
import os
import folium
from numpy import mean
import simplekml

os.chdir('./data')

## Is the ESRI Shapefile driver available?
driverName = "ESRI Shapefile"
drv = ogr.GetDriverByName( driverName )
if drv is None:
    print "%s driver not available.\n" % driverName
else:
    print  "%s driver IS available.\n" % driverName

#Set SRS

def shpFromPoints(filename, layername, points, save_kml = True):
    spatialReference = osr.SpatialReference()
    spatialReference.ImportFromProj4('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
    ds = drv.CreateDataSource(filename)
    layer=ds.CreateLayer(layername, spatialReference, ogr.wkbPoint)
    layerDefinition = layer.GetLayerDefn()
    
    point = ogr.Geometry(ogr.wkbPoint)
    feature = ogr.Feature(layerDefinition)
    
    kml = simplekml.Kml()
    for i, value in enumerate(points):
        point.SetPoint(0,value[0], value[1])
        feature.SetGeometry(point)
        layer.CreateFeature(feature)
        kml.newpoint(name=str(i), coords = [(value[0],value[1])])
    ds.Destroy()        
    if save_kml == True:
        kml.save("my_points.kml")
    
#ogr.main(["","-f", "KML", "shit.kml", filename])
    #ogr2ogr shp to kml
    
filename = "wageningenpoints.shp"
layername = "wagpoints"
pts = [(51.987398, 5.665777),
               (51.978434, 5.663133)]
shpFromPoints(filename, layername, pts)

def mapFromPoints(pts, outname, zoom_level, save = True):
    mean_long = mean([pt[0] for pt in pts])
    mean_lat = mean([pt[1] for pt in pts])
    point_map = folium.Map(location=[mean_long, mean_lat], zoom_start = zoom_level)
    for pt in pts:
        folium.Marker([pt[0], pt[1]],\
        popup = folium.Popup(folium.element.IFrame(
        html='''
                <b>Latitude:</b>  {lat}<br>
                <b>Longitude:</b> {lon}<br>
             '''.format(lat = pt[0], lon = pt[1]),\
        width=150, height=100),\
        max_width=150)).add_to(point_map)
    if save == True:
        point_map.save("{}.html".format(outname))
    return point_map

mapFromPoints(pts, "DisMyShit", zoom_level = 13)