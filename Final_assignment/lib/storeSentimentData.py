# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 11:44:55 2017

@author: user
"""
import psycopg2
## Should we connect with the file already named createTable?
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
                        label varchar(15),
                        sentiment numeric);
                    """.format(table_name = table_name)
    cur.execute(insert_query)
    con.commit()
    cur.close()
    con.close()

def insertSentiments(db_name, user, password, table_name, sentiment_tweets):
    try:
        con = psycopg2.connect("dbname={} user={} password={}".format(db_name, user, password))
        cur = con.cursor()
    except:
        print "oops error"
    for tweet in sentiment_tweets:
        insert_query = r"""INSERT INTO public.{table_name} VALUES (%s,%s,%s)""".format(table_name=table_name)
        data = (tweet[0],tweet[2],tweet[1])
        cur.execute(insert_query, data)
    con.commit()

def updateColumns(db_name, user, password,tweets_table,sentiment_table, list_columns, list_type):
    try:
        con = psycopg2.connect("dbname={} user={} password={}".format(db_name, user, password))
        cur = con.cursor()
    except:
        print "oops error"
    for i in range(len(list_columns)):    
        drop_column = """
            ALTER TABLE {tweets_table} DROP COLUMN IF EXISTS {column_name};
        """.format(tweets_table = tweets_table, column_name = list_columns[i])
        cur.execute(drop_column)
            
        add_column = """
            ALTER TABLE {tweets_table} ADD COLUMN {column_name}  {columntype};
        """.format(tweets_table = tweets_table, column_name=list_columns[i], columntype =list_type[i])
        cur.execute(add_column)
        
        update = """
            UPDATE {tweets_table} t2
            SET    {column_name} = t1.{column_name}
            FROM   {sentiment_table} t1
            WHERE  t2.id = t1.id              
        """.format(tweets_table=tweets_table,column_name=list_columns[i],sentiment_table=sentiment_table)
        cur.execute(update)
    #AND    t2.val2 IS DISTINCT FROM t1.val1  -- optional, to avoid empty updates
    
    con.commit()
    
def store(db_name,user,password,sentiment_tweets, sentiment_table,tweets_table,list_columns,list_types):
    createTable(db_name, user, password, sentiment_table, overwrite = False)
    insertSentiments(db_name, user, password, sentiment_table, sentiment_tweets)
    updateColumns(db_name, user, password,tweets_table,sentiment_table, list_columns, list_type)
    
    
    
    
    
    