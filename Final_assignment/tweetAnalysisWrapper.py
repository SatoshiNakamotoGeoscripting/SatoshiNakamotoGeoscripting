# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 10:51:48 2017

@author: Satoshi Nakamoto
names: Alex Levering and Hector Muro

Non-standard dependencies:
* Twython
* NLTK
* Folium
* Geocoder
* psycopg2

TO DO BEFOREHAND:
The following steps are non-automatable and have to be performed manually.
* Have the NLTK vader lexicon locally (nltk.download("vader"))
   - It may be that the lexicon does not install in the right location
     If this is the case, locate the file and place it #TODO: FILEPATH
* Set the file paths specified below to wherever your folder is
* Upgrade folium to the latest version (0.2.1)
"""

#------------------------------------------------------------------------------------
def performTweetResearch(folder_path,
                         user,
                         password,
                         defaultdb = "postgresql",
                         ouputdb = "tweetresearch",
                         tweet_table_name = "tweets",
                         gather_data = False,
                         loop_gathering = False,
                         APP_KEY = False,
                         APP_SECRET = False,
                         OAUTH_TOKEN = False,
                         OAUTH_TOKEN_SECRET = False):
    # Change working directory to load scripts if needed
    import os
    os.chdir(folder_path)
    
    from lib import gatherData
    from lib import dataManagement
    from lib import sentimentAnalyzerVader
    from lib import storeSentimentData
    from lib import visualizeData
    
    os.chdir(folder_path + r"/data")
    """Wrapper function that abstracts database creation, table names and other variables that are tedious to set"""
    # Abstracted table names
    sentiment_table_name = "sentiment"
    geojson_name = "countries.geo.json"
    polygon_table_name = "countrydata"
    output_geojson_name = "tweetspercountry.geojson"
    output_html_name = "tweets"
    
    dataManagement.createDatabase(default_dbname = defaultdb,
                                  new_dbname = ouputdb,
                                  user = user,
                                  password = password)
    
    dataManagement.createPostGISExtension(dbname = ouputdb,
                                          user = user,
                                          password = password)

    dataManagement.createPostgreSQLTable(dbname = ouputdb,
                                         user = user,
                                         password = password,
                                         table_name = tweet_table_name,
                                         overwrite = False)
    
    if gather_data != False: # In case a different output_dbname is specified, alter the getData script to connect to the other database instead
        if OAUTH_TOKEN_SECRET != False:
            gatherData.TweetsRealTime(dbname = ouputdb,
                                        user = user,
                                        password = password,
                                        table_name = tweet_table_name,
                                        APP_KEY = APP_KEY,
                                        APP_SECRET =  APP_SECRET,
                                        OAUTH_TOKEN =  OAUTH_TOKEN,
                                        OAUTH_TOKEN_SECRET = OAUTH_TOKEN_SECRET,
                                        loop_gathering = False)
        else:
            print "Twitter API tokens have not been specified. If you do not have them, make an account at developer.twitter.com and make a new application"
    
    """Retrieve tweets for further sentiment analysis, selecting only those in english because the sentiment library understands English only"""
    sql = "SELECT * FROM {table} WHERE lang = 'en' or lower(lang) = 'en-GB' or lower(lang) = 'en-US'".format(table = tweet_table_name)
    retrieved_tweets = dataManagement.getTweetsFromDB(ouputdb, user, password, sql)
    
    """Sentiment analysis"""
    analysed_tweets = sentimentAnalyzerVader.SentimentAnalyzer(retrieved_tweets)
    
    """Store in another table of the database the sentiment data just created and then add it to the original Tweetstable"""
    storeSentimentData.createSentimentTable(dbname = ouputdb,
                                           user = user,
                                           password = password,
                                           table_name = sentiment_table_name,
                                           overwrite = False)
                                   
    storeSentimentData.insertSentiments(dbname = ouputdb,
                                        user = user,
                                        password = password,
                                        table_name = sentiment_table_name,
                                        sentiment_tweets = analysed_tweets)
                                        
    storeSentimentData.updateColumns(dbname = ouputdb,
                                     user = user,
                                     password = password,
                                     tweets_table = tweet_table_name,
                                     sentiment_table = sentiment_table_name,
                                     list_columns = ["label","sentiment"],
                                     list_type=["varchar(15)", "numeric"])
    
    """Visualize data"""
    visualising_tweets = dataManagement.getTweetsFromDB(dbname = ouputdb,
                                             username = "user",
                                             password = "user",
                                             sql = "SELECT * FROM {}".format(tweet_table_name))
                             
    dataManagement.importPolyJSON(dbname = ouputdb,
                                   username = user,
                                   password = password,
                                   geojson = geojson_name,
                                   output_table_name = polygon_table_name)
                  
    records = visualizeData.getPointsPerPolygon(dbname = ouputdb,
                                              username = user,
                                              password = password,
                                              poly_table_name = polygon_table_name,
                                              tweet_table_name = tweet_table_name)

    dataManagement.exportPostgresqltoGeoJSON(dbname = ouputdb,
                                              username = user,
                                              password = password,
                                              output_filename = output_geojson_name)                                              
    
    filtered_tweets = dataManagement.filterTweetsToData(visualising_tweets)
    twitter_map = visualizeData.tweetMap(filtered_tweets, 3, "cartodbpositron")
    twitter_map.addTweets()
    twitter_map.addChoropleths(output_geojson_name, records)
    twitter_map.addPolygonCentroids(output_geojson_name, records)
    twitter_map.addLayerControl()
    twitter_map.saveMap(output_html_name)
    twitter_map.saveMap(output_html_name)

if __name__ == "__main__":
    performTweetResearch(defaultdb = "postgres",
                         user = "user",
                         password = "user",
                         ouputdb = "tweets",
                         tweet_table_name = "trumptweets2",
                         gather_data = False)