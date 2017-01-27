#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 16:23:07 2017

@author: user
"""
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import sys
reload(sys) #Prevents errors with utf-8 encoding not working properly
sys.setdefaultencoding('utf8')


pos_tweets = []
neg_tweets = []
with open('SentimentDataset.csv') as trainingset:
    i = 0
    lines = trainingset.readlines()
    line = lines[0]
    while i < int((0.005 * len(lines))):
        string_without_chars = line[:-5]
        split_line = string_without_chars.split(',')
        tweet_text = split_line[3:]
        print tweet_text
        if string_without_chars[1] == '1':
            pos_tweets.append((tweet_text, 'positive'))
        else:
            neg_tweets.append((tweet_text, 'negative'))
        i += 1
        line = lines[i+1]        

##Create a list of tweets with the tweet and its value              
labeled_tweets = []

for(words,sentiment) in pos_tweets + neg_tweets:
    #wordsFiltered = [e.lower() for e in words.split() if len(e) >=3] #We discard words with less than two letters
    labeled_tweets.append((words))#,sentiment))

" ".join(tweet for tweet in labeled_tweets)
testing = []
for tweet in labeled_tweets:
    for word in tweet:
        testing.append("".join(word))


sid = SentimentIntensityAnalyzer() #need to nltk.download() to use all the packages
for tweet in testing:
    print tweet    
    ss = sid.polarity_scores(tweet)
    for k in sorted (ss):
        #print ('%s: %s,' % (k, ss[k]))
        print('{0}: {1}, '.format(k, ss[k]))
