# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 10:51:48 2017

@author: Satoshi Nakamoto
names: Alex Levering and Hector Muro
"""

import createTable
import gatherData
import convertFormats
import sentimentAnalyzerVader #MUST FIX ISSUES HERE
import storeSentimentData


"""Database must be created beforehand manually in Postgres"""
#createTable.createTable(db_name=, user=, password=, table_name=, overwrite = False)
createTable.createTable(db_name="tweets", user="user", password="user", table_name = "trumptweets", overwrite = True)

"""Connection with Twitter in real-time gathering data. The table where tweets are going to be inserted is set by default "trumptweets"
    If another name is wanted, or the name is changed in the create Table call, it must be changed manually inside gatherData.py"""
gatherData.TweetsRealTime()

"""Retrieve tweets for further sentiment analysis, selecting only those in english because the sentiment library understands English only"""
sql = "SELECT * FROM trumptweets WHERE lang = 'en' or lower(lang) = 'en-GB' or lower(lang) = 'en-US'"
tweets = convertFormats.getTweetsFromDB("tweets","user", "user", sql)

"""Sentimet analysis"""
"""This requires the manual download of vader_lexicon.txt. Use nltk.download() once nltk library is downloaded"""
#import nltk
#nltk.download
sentiment_tweets = sentimentAnalyzerVader.SentimentAnalyzer(tweets)

"""Store in another table of the database the sentiment data just created and then add it to the original Tweetstable"""
storeSentimentData.createTable(db_name="tweets", user="user", password="user", table_name = "sentiment_table", overwrite = False)
storeSentimentData.insertSentiments(db_name="tweets", user="user", password="user", table_name = "sentiment_table",sentiment_tweets=sentiment_tweets)
storeSentimentData.updateColumns(db_name="tweets", user="user", password="user",tweets_table="trumptweets",
                                 sentiment_table="sentiment_table", list_columns = ["label","sentiment"], list_type=["varchar(15)", "numeric"])




#if __name__ == '__main__':
#
#    