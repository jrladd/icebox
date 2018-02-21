#! /usr/bin/env python3

import tweepy
from secrets import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if any(q in status.text for q in queries) and status.user.screen_name != "sosweetbot" and status.user.screen_name != "JustToSayBot":
            # print(status.user, status.text)
            api.retweet(status.id)

    def on_error(self, status_code):
        print(status_code)
        if status_code == 420:
            return False

queries = ["this is just to say", "so sweet and so cold", "plums icebox", "which you were probably"]
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
myStream.filter(track=queries)
