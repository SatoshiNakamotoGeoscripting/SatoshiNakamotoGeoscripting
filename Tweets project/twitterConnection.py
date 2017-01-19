# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from twython import Twython
import json
import datetime 



##codes to access twitter API. 
APP_KEY = 
APP_SECRET =  
OAUTH_TOKEN =   
OAUTH_TOKEN_SECRET = 

##initiating Twython object 
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

##TODO:  This should work as an alternative but it doesn't. Need to find out why
#twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
#ACCESS_TOKEN = twitter.obtain_access_token()
#print ACCESS_TOKEN
#twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)

search_results = twitter.search(q=['#ns','#ov'], count=2)


#for result in search_results['statuses']:
#    print result

#for key in search_results:
#    print key
    
newdict = search_results["statuses"]
for key in newdict:
    print key