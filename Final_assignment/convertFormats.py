# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 11:35:10 2017

@author: user
"""
import psycopg2

def getTweetsFromDB(dbname, username, password, sql):
    """From an existing Tweets database, collect all records"""
    con = psycopg2.connect("dbname={} user={} password={}".format(dbname, username, password))
    cur = con.cursor()
    
    # Retrieve data from database and extract coordinates
    cur.execute(sql)
    records = cur.fetchall()
    
    con.close()
    cur.close()
    return records


def importPolyJSON(dbname, username, password, geojson, output_table_name):
    """Import specified geojson file into postgresql spatial db"""
    # http://gis.stackexchange.com/questions/172092/import-geojson-into-postgis
    # http://morphocode.com/using-ogr2ogr-convert-data-formats-geojson-postgis-esri-geodatabase-shapefiles/
    bash = 'ogr2ogr -f "PostgreSQL" PG:"dbname={dbname} user={user}" "{geojson}" -nln {output_table_name} -overwrite'.format(
            dbname = dbname,
            user = username,
            geojson = geojson,
            output_table_name = output_table_name)
    system(bash)