    # -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import geocoder
import psycopg2

def createTable(db_name, user, password, table_name, overwrite = False):
    try:
        con = psycopg2.connect("dbname={} user={} password={}".format(db_name, user, password))
        cur = con.cursor()
    except:
        print "oops error"
        
    if overwrite == False:
        insert_query =  """CREATE TABLE IF NOT EXISTS {table_name} (
                            id  	bigint,
                            time	varchar(50),
                            latitude	varchar(50),
                            longitude	varchar(50),
                            selfrepcity varchar(500),    
                            lang	varchar(10),
                            source	varchar(100),
                            countrycode	varchar(10),
                            countryname	varchar(100),
                            location	varchar(100),
                            retweet	varchar(10),
                            text        varchar(500),
                            loclat   varchar(30),
                            loclong  varchar(30));
                        """.format(table_name = table_name)
        data = (table_name)
    else:
        insert_query =  """DROP TABLE IF EXISTS {table_name};
                            CREATE TABLE {table_name} (
                            id  	bigint,
                            time	varchar(50),
                            latitude	varchar(50),
                            longitude	varchar(50),
                            selfrepcity varchar(500),    
                            lang	varchar(10),
                            source	varchar(100),
                            countrycode	varchar(10),
                            countryname	varchar(100),
                            location	varchar(100),
                            retweet	varchar(10),
                            text        varchar(500),
                            loclat   decimal,
                            loclong  decimal);
                        """.format(table_name = table_name)
    cur.execute(insert_query)
    con.commit()
    cur.close()
    con.close()
createTable(db_name="tweets", user="user", password="user", table_name = "drugtable", overwrite = True)