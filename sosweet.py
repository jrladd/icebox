#! /usr/bin/env python3

import tweepy
from secrets import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

def search_tweets(count):
    queries = ['"this is just to say"', '"so sweet and so cold"', "plums icebox"]
    q = " OR ".join(queries)+" exclude:retweets"
    results = api.search(q, result_type="recent", count=count)
    return results

results = search_tweets(40)
for r in results:
    print(r.id, r.text)
