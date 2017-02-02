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
* Have PostGIS installed on PostgreSQL
* Set the file paths specified below to wherever your folder is
* Upgrade folium to the latest version (0.2.1)
"""



# Naming options for tables, intermediates and outputs are available in the wrapper.
if __name__ == "__main__":
    """The tool is not supplied with Tweets out-of-the-box. Set 'gather_data' to True and leave it
        running for a while. If loop is false it will terminate in a minute or so and create a map from the results automatically"""
    import tweetAnalysisWrapper
    tweetAnalysisWrapper.performTweetResearch(folder_path = r"/home/user/Desktop/GIT/Final_assignment",
                                              defaultdb = "postgres",
                                              user = "user",
                                              password = "user",
                                              ouputdb = "tweet_research",
                                              tweet_table_name = "tweets",
                                              gather_data = True,
                                              loop_gathering = False,
                                              APP_KEY = "",
                                              APP_SECRET =  "",
                                              OAUTH_TOKEN =  "",
                                              OAUTH_TOKEN_SECRET = "")