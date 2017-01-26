# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 11:40:24 2017

@author: user
"""

### SENTIMENT TEST
### http://www.nltk.org/
### http://www.nltk.org/book/
### citate in our work: Bird, Steven, Edward Loper and Ewan Klein (2009), Natural Language Processing with Python. O’Reilly Media Inc.
### http://www.laurentluce.com/posts/twitter-sentiment-analysis-using-python-and-nltk/

import re
import nltk

## Both positive and negative tweets should be much bigger!!!
posTweets = [('I love this car', 'positive'),('This view is amazing', 'positive'),
              ('I feel great this morning', 'positive'),('I am so excited about the concert', 'positive'),
              ('He is my best friend', 'positive')]
              
negTweets = [('I do not like this car', 'negative'),('This view is horrible', 'negative'),
              ('I feel tired this morning', 'negative'),('I am not looking forward to the concert', 'negative'),
              ('He is my enemy', 'negative')]

pos_tweets = []
neg_tweets = []
with open('SentimentDataset.csv') as trainingset:
    i = 0
    lines = trainingset.readlines()
    line = lines[0]
    while i < int((0.01 * len(lines))):
        string_without_chars = line[:-5]
        print string_without_chars
        split_line = string_without_chars.split(',')
        tweet_text = split_line[3:]
        if split_line[1] == '1':
            pos_tweets.append((tweet_text, 1))
        else:
            neg_tweets.append((tweet_text, 0))
        i += 1
        line = lines[i+1]        
        
##Create a list of tweets with the tweet and its value              
tweets = []
for(words,sentiment) in posTweets + negTweets:
    wordsFiltered = [e.lower() for e in words.split() if len(e) >=3]  #We discard words with less than two words
    tweets.append((wordsFiltered,sentiment))

## Small Tweets list for testing
"""Load 10% of training set here"""

testTweets = [(['feel', 'happy', 'this', 'morning'], 'positive'),(['larry', 'friend'], 'positive'),
               (['not', 'like', 'that', 'man'], 'negative'),(['house', 'not', 'great'], 'negative'),
                (['your', 'song', 'annoying'], 'negative')]
                
## List with every word, ordered by frequency of appearance.
wordsList=[]
for word,sentiment in tweets:
    wordsList.extend(word)
    
    
wordlist = nltk.FreqDist(wordsList)
word_features = wordlist.keys()

def extract_features(testTweets):
    documentWords = set(testTweets)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in documentWords)
    return features

a = extract_features(['have','nice','car'])

## With our feature extractor, we can apply the features to our classifier using the method apply_features.
training_set = nltk.classify.apply_features(extract_features, tweets)

## Now that we have our training set, we can train our classifier.
classifier = nltk.NaiveBayesClassifier.train(training_set)

print label_probdist.prob('positive')

print classifier.show_most_informative_features(32)


### CLASSIFY!!!

tweet = 'Everythin is bad I hate this world'
print classifier.classify(extract_features(tweet.split()))