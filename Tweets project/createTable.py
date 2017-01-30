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
        
    if overwrite == True:
        del_table_query = """DROP TABLE IF EXISTS {table_name};""".format(table_name = table_name)
        cur.execute(del_table_query)
    insert_query =  """CREATE TABLE IF NOT EXISTS {table_name} (
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
createTable(db_name="tweets", user="user", password="user", table_name = "trumptweets3", overwrite = True)