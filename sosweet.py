#! /usr/bin/env python3

import tweepy
from secrets import *

# Initialize tweepy with relevant secret keys
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

class MyStreamListener(tweepy.StreamListener):
    """
    This class defines how Twitter's streaming API should behave.
    """

    def on_status(self, status):
        """
        When a status is found, filter for the exact phrase and retweet.
        """
        test_text = ' '.join(status.text.lower().split())
        if any(q in test_text for q in queries) and status.user.screen_name != "sosweetbot" and status.user.screen_name != "JustToSayBot":
            # print(status.user, status.text)
            api.retweet(status.id)

    def on_error(self, status_code):
        """
        When API returns error, keep going unless the error is for rate limit.
        """
        if status_code == 420:
            return False

# List relevant queries
queries = ["this is just to say", "so sweet and so cold", "plums icebox", "which you were probably"]

# Initialize stream listener
myStreamListener = MyStreamListener() # Create class instance
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener) # Start stream
myStream.filter(track=queries) # Listen for queries (case insensitive)

# The code below used for testing the custom tweet filter function
# class status():
#      class user():
#           screen_name = 'johnrladd'
#      text = 'I have eaten\n\nThe plums\n\nAnd which\n\nyou were probably'
#
# status = status()
# myStreamListener.on_status(status)
