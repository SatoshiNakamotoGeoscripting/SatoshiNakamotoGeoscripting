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
    #for tweet in tweets:
    sentiment_tweets = []
    for i in range(10): 
        tweet_id = tweets[i][0]
        tweet_id = str(tweet_id)
        tweet_id = int(tweet_id)
        ss = sid.polarity_scores(tweets[i][1])
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

def insertSentiments(tablename,sentiment_tweets):

    conn = psycopg2.connect("dbname=tweets user=user password=user")
    cursor = conn.cursor()                   
    
    insert = """INSERT INTO {tablename}(sentiment,label) VALUES {sentiment},{label} 
    """.format(tablename = tablename, 
                            sentiment = sentiment_tweets[1], 
                            label = sentiment_tweets[2]) 
                            #id = sentiment_tweets[0])
    cursor.execute(insert)
    #conn.commit()

insertSentiments("trumptweets2",sentiment_tweets)

#    add_columns = """
#        ALTER TABLE trumptweets2 ADD COLUMN sentiment  decimal;
#        ALTER TABLE trumptweets2 ADD COLUMN label varchar(15);
#    """
#    cursor.execute(add_columns)
#    conn.commit()