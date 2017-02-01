# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 10:51:48 2017

@author: Satoshi Nakamoto
names: Alex Levering and Hector Muro
"""

# Change working directory to load scripts if needed
import os
os.chdir(r"/home/user/git/SatoshiNakamotoGeoscripting/Final_assignment")

from lib import gatherData
from lib import dataManagement
from lib import sentimentAnalyzerVader #MUST FIX ISSUES HERE
from lib import storeSentimentData
from lib import visualizeData

os.chdir(r"/home/user/git/SatoshiNakamotoGeoscripting/Final_assignment/data")

"""Database must be created beforehand manually in Postgres"""
#createTable.createTable(db_name=, user=, password=, table_name=, overwrite = False)
dataManagement.createPostgreSQLTable(db_name="tweets", user="user", password="user", table_name = "trumptweets", overwrite = False)

"""Connection with Twitter in real-time gathering data. The table where tweets are going to be inserted is set by default "trumptweets"
    If another name is wanted, or the name is changed in the create Table call, it must be changed manually inside gatherData.py"""
# gatherData.TweetsRealTime()

"""Retrieve tweets for further sentiment analysis, selecting only those in english because the sentiment library understands English only"""
sql = "SELECT * FROM trumptweets WHERE lang = 'en' or lower(lang) = 'en-GB' or lower(lang) = 'en-US'"
tweets = dataManagement.getTweetsFromDB("tweets","user", "user", sql)

"""Sentiment analysis"""
"""This requires the manual download of vader_lexicon.txt. Use nltk.download() once nltk library is downloaded"""
#import nltk
#nltk.download
sentiment_tweets = sentimentAnalyzerVader.SentimentAnalyzer(tweets)

"""Store in another table of the database the sentiment data just created and then add it to the original Tweetstable"""
storeSentimentData.createTable(db_name="tweets", user="user", password="user", table_name = "sentiment_table", overwrite = False)
storeSentimentData.insertSentiments(db_name="tweets", user="user", password="user", table_name = "sentiment_table",sentiment_tweets=sentiment_tweets)
storeSentimentData.updateColumns(db_name="tweets", user="user", password="user",tweets_table="trumptweets",
                                 sentiment_table="sentiment_table", list_columns = ["label","sentiment"], list_type=["varchar(15)", "numeric"])


"""Visualize data"""
tweets = dataManagement.getTweetsFromDB(dbname = "tweets",
                                         username = "user",
                                         password = "user",
                                         sql = "SELECT * FROM trumptweets")[-10:]
                         
dataManagement.importPolyJSON(dbname = "tweets",
                               username = "user",
                               password = "user",
                               geojson = "countries.geo.json",
                               output_table_name = "countrydata")
                              
dataManagement.exportPostgresqltoGeojson(dbname = "tweets",
                                          username = "user",
                                          password = "user",
                                          output_filename = "tweetspercountry")                              
              
records = visualizeData.getPointsPerPolygon(dbname = "tweets",
                                          username = "user",
                                          password = "user",
                                          poly_table_name = "countrydata",
                                          tweet_table_name = "trumptweets")

filtered_tweets = dataManagement.filterTweetsToData(tweets)
              
trump_tweets = visualizeData.tweetMap(filtered_tweets, 3, "cartodbpositron")
trump_tweets.addTweets()
trump_tweets.addChoropleths("tweetspercountry.geojson", records)
trump_tweets.addPolygonCentroids("tweetspercountry.geojson", records)
trump_tweets.addLayerControl()
trump_tweets.saveMap("Trump Tweets Test")