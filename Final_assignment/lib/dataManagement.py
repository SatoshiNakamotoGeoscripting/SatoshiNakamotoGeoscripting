# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 11:35:10 2017

@author: user
"""
import psycopg2
from os import system
import urllib2

def createDatabase(default_dbname, new_dbname, user, password):
    try:    
        con = psycopg2.connect("dbname={} user={} password={}".format(default_dbname, user, password))
        con.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()
    except:
        print "Unable to connect to the database or set the isolation level"
    try:
        insert_query = """CREATE DATABASE {dbname};""".format(dbname = new_dbname)
        cur.execute(insert_query)
        con.commit()
        cur.close()
        con.close()
    except:
        print "Failed to create database. It might already exist or you do not have the rights to make a new database."

def createPostGISExtension(dbname, user, password):
    con = psycopg2.connect("dbname={} user={} password={}".format(dbname, user, password))
    cur = con.cursor()
    try:
        insert_query = """CREATE EXTENSION PostGIS;"""
        cur.execute(insert_query)
        con.commit()
    except:
        print "Extension PostGIS already exists, or PostGIS is not installed"
    cur.close()
    con.close()

def createPostgreSQLTable(dbname, user, password, table_name, overwrite = False):
    con = psycopg2.connect("dbname={} user={} password={}".format(dbname, user, password))
    cur = con.cursor()
    
    if overwrite == True:
        del_table_query = """DROP TABLE IF EXISTS {table_name};""".format(table_name = table_name)
        cursor.execute(del_table_query)
    insert_query = """CREATE TABLE IF NOT EXISTS {table_name} (
                    id  	bigint,
                    time	varchar(50),
                    latitude	decimal,
                    longitude	decimal,
                    selfrepcity varchar(500),    
                    lang	varchar(10),
                    source	varchar(250),
                    countrycode	varchar(10),
                    countryname	varchar(250),
                    location	varchar(250),
                    url	varchar(100),
                    text        varchar(500),
                    loclat   decimal,
                    loclong  decimal);
                """.format(table_name = table_name)
    cur.execute(insert_query)
    con.commit()
    cur.close()
    con.close()

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

def exportPostgresqltoGeoJSON(dbname, username, password, output_filename):
    """Using bash, export a postgresql table to GeoJSON format"""
    # Export temporary table to GeoJSON
    bash = 'ogr2ogr -f "GeoJSON" {geojson} PG:"dbname={dbname} user={user} password={password}" "polygonStatistics"'.format(
        dbname = dbname,
        user = username,
        password = password,
        geojson = output_filename)    
    system(bash)

def filterTweetsToData(all_tweets):
    """Select relevant data from all returned records for marker assignment"""
    # TODO: Use pandas Dataframe as data sharing mechanism for direct column name assignment
    list_of_tweets = []
    for i, record in enumerate(all_tweets):
        tweet_text = record[11].encode('utf-8')
        tweet_sentiment_overall = record[14]
        tweet_label = record[15]
        
        
        # If it can use accurate coordinates, add these coordinates and True, else the estimated coords with False
        if record[2] != 9999:
            tweet_coords = (float(record[2]),float(record[3]), True)
        else:
            tweet_coords = (float(record[12]),float(record[13]), False)
        
        list_of_tweets.append([tweet_text, (tweet_sentiment_overall, tweet_label), tweet_coords])
    return list_of_tweets