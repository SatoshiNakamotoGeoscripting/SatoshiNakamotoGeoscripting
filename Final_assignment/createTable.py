    # -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import psycopg2
import geocoder

def createTable(db_name, user, password, table_name, overwrite = False):
    try:
        con = psycopg2.connect("dbname={} user={} password={}".format(db_name, user, password))
        cursor = con.cursor()
        print "connected"
    except:
        print "connection failed!"
        
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
    cursor.execute(sql)
    con.commit()
    cursor.close()
    con.close()
#createTable(db_name="tweets", user="user", password="user", table_name = "trumptweets", overwrite = True)
    