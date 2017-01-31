#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 16:23:07 2017

@author: user
"""
## FOUND HERE http://www.nltk.org/howto/sentiment.html
## Source code http://www.nltk.org/_modules/nltk/sentiment/vader.html
## http://www.nltk.org/api/nltk.sentiment.html
## Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model 
##for Sentiment Analysis of Social Media Text. Eighth International Conference on
## Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.
## http://www.postgresqltutorial.com/postgresql-python
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import psycopg2
import sys
reload(sys) #Prevents errors with utf-8 encoding not working properly
sys.setdefaultencoding('utf8')

def getTweetsFromDB(dbname, user, password, table_name):
    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect("dbname={} user={} password={}".format(dbname, user, password))
    cursor = conn.cursor()
    
    # Retrieve data from database and extract coordinates
    cursor.execute("SELECT * FROM {} WHERE lang = 'en'".format(table_name))
    records = cursor.fetchall()
    
    list_of_tweets = []
    for i, record in enumerate(records):
        tweet_text = record[11].encode('utf-8')
        tweet_id = record[0]
        
        list_of_tweets.append([tweet_id,tweet_text])
    return list_of_tweets

tweets = getTweetsFromDB("tweets","user","user","trumptweets2")

def SentimentAnalyzer(tweets):
    sid = SentimentIntensityAnalyzer() #need to nltk.download() to use all the packages

    sentiment_tweets = []
    #for i in range(10):
    for tweet in tweets:   
        tweet_id = tweet[0]
        tweet_id = str(tweet_id)
        tweet_id = int(tweet_id)
        ss = sid.polarity_scores(tweet[1])
        if ss['compound'] <= -0.293:
            label = 'negative'
        elif ss['compound'] >= 0.293:
            label = 'positive'
        else:
            label = 'neutral'
        sentiment = ss['compound']
        
        sentiment_tweets.append((tweet_id,sentiment,label))
    return sentiment_tweets
                  
sentiment_tweets = SentimentAnalyzer(tweets)

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
createTable(db_name="tweets", user="user", password="user", table_name = "sentiment_tweets", overwrite = True)

def insertSentiments(db_name, user, password, table_name, sentiment_tweets):
    try:
        con = psycopg2.connect("dbname={} user={} password={}".format(db_name, user, password))
        cur = con.cursor()
    except:
        print "oops error"
    for tweet in sentiment_tweets:
        insert_query = r"""INSERT INTO public.sentiment_tweets VALUES (%s,%s,%s)"""
        data = (tweet[0],tweet[2],tweet[1])
        cur.execute(insert_query, data)
    con.commit()
insertSentiments("tweets","user","user","sentiment_tweets",sentiment_tweets)

def updateColumn(db_name, user, password,target_table,source_table, list_columns, list_type):
    try:
        con = psycopg2.connect("dbname={} user={} password={}".format(db_name, user, password))
        cur = con.cursor()
    except:
        print "oops error"
    for i in range(len(list_columns)):    
        drop_column = """
            ALTER TABLE trumptweets2 DROP COLUMN IF EXISTS {column_name};
        """.format(column_name = list_columns[i])
        cur.execute(drop_column)
            
        add_column = """
            ALTER TABLE trumptweets2 ADD COLUMN {column_name}  {columntype};
        """.format(column_name=list_columns[i], columntype =list_type[i])
        cur.execute(add_column)
        
        update = """
            UPDATE {target_table} t2
            SET    {column_name} = t1.{column_name}
            FROM   {source_table} t1
            WHERE  t2.id = t1.id              
        """.format(target_table=target_table,column_name=list_columns[i],source_table=source_table)
        cur.execute(update)
    #AND    t2.val2 IS DISTINCT FROM t1.val1  -- optional, to avoid empty updates
    
    con.commit()
    
    
updateColumn("tweets", "user", "user","trumptweets2","sentiment_tweets",["label","sentiment"],["varchar(15)","numeric"])
    
