# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 10:51:48 2017

@author: Satoshi Nakamoto
names: Alex Levering and Hector Muro

Non-standard dependencies:
* Twython
* NLTK
* Folium
* psycopg2

TO DO BEFOREHAND:
The following steps are non-automatable and have to be performed manually.
* Have the NLTK vader lexicon locally (nltk.download("vader") should do the trick)
* Install PostGIS in the database

"""
# Change working directory to load scripts if needed
import os
os.chdir(r"/home/user/Desktop/git/SatoshiNakamotoGeoscripting/Final_assignment")

from lib import gatherData
from lib import dataManagement
from lib import sentimentAnalyzerVader #MUST FIX ISSUES HERE
from lib import storeSentimentData
from lib import visualizeData

os.chdir(r"/home/user/Desktop/git/SatoshiNakamotoGeoscripting/Final_assignment/data")

"""Database must be created beforehand manually in Postgres"""
#createTable.createTable(db_name=, user=, password=, table_name=, overwrite = False)
dataManagement.createPostgreSQLTable(db_name="postgres", user="user", password="user", table_name = "t_tweets", overwrite = False)

"""Connection with Twitter in real-time gathering data. The table where tweets are going to be inserted is set by default "t_tweets"
    If another name is wanted, or the name is changed in the create Table call, it must be changed manually inside gatherData.py"""
# gatherData.TweetsRealTime()

"""Retrieve tweets for further sentiment analysis, selecting only those in english because the sentiment library understands English only"""
sql = "SELECT * FROM t_tweets WHERE lang = 'en' or lower(lang) = 'en-GB' or lower(lang) = 'en-US'"
tweets = dataManagement.getTweetsFromDB("postgres","user", "user", sql)

"""Sentiment analysis"""
#import nltk
#nltk.download
sentiment_tweets = sentimentAnalyzerVader.SentimentAnalyzer(tweets)

"""Store in another table of the database the sentiment data just created and then add it to the original Tweetstable"""
storeSentimentData.createTable(db_name="postgres", user="user", password="user", table_name = "sentiment_table", overwrite = False)
storeSentimentData.insertSentiments(db_name="postgres", user="user", password="user", table_name = "sentiment_table",sentiment_tweets=sentiment_tweets)
storeSentimentData.updateColumns(db_name="postgres", user="user", password="user",tweets_table="t_tweets",
                                 sentiment_table="sentiment_table", list_columns = ["label","sentiment"], list_type=["varchar(15)", "numeric"])


"""Visualize data"""
tweets = dataManagement.getTweetsFromDB(dbname = "postgres",
                                         username = "user",
                                         password = "user",
                                         sql = "SELECT * FROM t_tweets")
                         
dataManagement.importPolyJSON(dbname = "postgres",
                               username = "user",
                               password = "user",
                               geojson = "countries.geo.json",
                               output_table_name = "countrydata")
                              
dataManagement.exportPostgresqltoGeoJSON(dbname = "postgres",
                                          username = "user",
                                          password = "user",
                                          output_filename = "tweetspercountry")                              
              
records = visualizeData.getPointsPerPolygon(dbname = "postgres",
                                          username = "user",
                                          password = "user",
                                          poly_table_name = "countrydata",
                                          tweet_table_name = "t_tweets")

filtered_tweets = dataManagement.filterTweetsToData(tweets)         
trump_tweets = visualizeData.tweetMap(filtered_tweets, 3, "cartodbpositron")
trump_tweets.addTweets()
trump_tweets.addChoropleths("tweetspercountry.geojson", records)
trump_tweets.addPolygonCentroids("tweetspercountry.geojson", records)
trump_tweets.addLayerControl()
trump_tweets.saveMap("Trump Tweets Test")