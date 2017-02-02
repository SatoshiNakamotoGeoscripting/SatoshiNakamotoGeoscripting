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

import tweetAnalysisWrapper

# More naming options are available in the wrapper function, but are abstracted away for neatness sake
if __name__ == "__main__":
    tweetAnalysisWrapper.performTweetResearch(defaultdb = "postgres",
                         user = "user",
                         password = "user",
                         ouputdb = "tweetresearch",
                         tweet_table_name = "tweets",
                         gather_data = False)