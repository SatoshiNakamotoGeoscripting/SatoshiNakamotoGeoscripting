# -*- coding: utf-8 -*-
"""
Date: 2/2/2017

Team: Satoshi Nakamoto
@Authors: Alex Levering and Hector Muro

Non-standard dependencies:
* Twython
* NLTK
* Folium
* Geocoder
* psycopg2

TO DO BEFOREHAND:
The following steps are non-automatable and have to be performed manually.
* Have the NLTK vader lexicon locally (nltk.download("vader_lexicon"))
* Have PostGIS installed on PostgreSQL
* Set the file paths specified below to wherever your folder is
* Upgrade folium to the latest version (0.2.1)
"""



# Naming options for tables, intermediates and outputs are available in the wrapper.
if __name__ == "__main__":
    """
        The tool is not supplied with Tweets out-of-the-box. Set 'gather_data' to True and leave it
        running for a while. If loop is false it will terminate in a minute or so and create a map from the results automatically
        
        This tool was tested and intended for OSGeo Live installs used in the GeoScripting course.
    """
    import tweetAnalysisWrapper
    tweetAnalysisWrapper.performTweetResearch(folder_path = r"/home/user/git/SatoshiNakamotoGeoscripting/Final_assignment",
                                              defaultdb = "postgres", # Making a new database requires connecting to an existing database
                                              user = "user", # PostgreSQL username (user is default value on OSGeo Live)
                                              password = "user", # PostgreSQL password (user is default on OSGeo Live)
                                              ouputdb = "tweet_research", # Specify the output database that is to be created
                                              tweet_table_name = "tweets", # Output table where the Tweets are stored
                                              gather_data = True, # When True: Will gather data from the Twitter stream
                                              search_terms = ["Trump"], # Twitter terms to search for                                   
                                              loop_gathering = False, # When True: Will not stop gathering when terminated - use for prolonged gathering
                                              APP_KEY = "", # Get these from developer.twitter.com when you make your application
                                              APP_SECRET =  "",
                                              OAUTH_TOKEN =  "",
                                              OAUTH_TOKEN_SECRET = "")
