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
* Have PostGIS installed on PostgreSQL
* Set the file paths specified below to wherever your folder is
* Upgrade folium to the latest version (0.2.1)
"""



# Naming options for tables, intermediates and outputs are available in the wrapper.
if __name__ == "__main__":
    import tweetAnalysisWrapper
    tweetAnalysisWrapper.performTweetResearch(folder_path = r"/home/user/git/SatoshiNakamotoGeoscripting/Final_assignment",
                                              defaultdb = "postgres",
                                              user = "user",
                                              password = "user",
                                              ouputdb = "tweet_research",
                                              tweet_table_name = "tweets",
                                              gather_data = True,
                                              loop_gathering = False,
                                              APP_KEY = "Q530eYJ2divtkAltNRF9ORY6G",
                                              APP_SECRET =  "xgRzCBf53goOm1ir06spIT8oAmvQFu5kr53ptycDn4CCEw0MYc",
                                              OAUTH_TOKEN =  "2567730218-I3fdSSmhVi8vDq0zn94OGTnfkpTpPqKpOHaqvD5",
                                              OAUTH_TOKEN_SECRET = "maoKC8LRS2rxpRmSz9mUbOCTc8TE2VxAaBJQTue2stqQS")