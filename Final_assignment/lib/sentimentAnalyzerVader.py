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
## http://www.postgresqltutorial.com/postgresql-python
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import psycopg2
import sys
reload(sys) #Prevents errors with utf-8 encoding not working properly
sys.setdefaultencoding('utf8')


def SentimentAnalyzer(tweets):
    sid = SentimentIntensityAnalyzer() #need to nltk.download() to use all the packages

    sentiment_tweets = []
    #for i in range(10):
    for tweet in tweets:   
        tweet_id = tweet[0]
        tweet_id = str(tweet_id)
        tweet_id = int(tweet_id)
        ss = sid.polarity_scores(tweet[11])
        if ss['compound'] <= -0.293:
            label = 'negative'
        elif ss['compound'] >= 0.293:
            label = 'positive'
        else:
            label = 'neutral'
        sentiment = ss['compound']
        
        sentiment_tweets.append((tweet_id,sentiment,label))
    return sentiment_tweets

