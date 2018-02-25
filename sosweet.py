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
        if is_wcw(status):
            try:
                # print(status.user, status.text)
                api.retweet(status.id)
            except tweepy.TweepError:
                pass

    def on_error(self, status_code):
        """
        When API returns error, keep going unless the error is for rate limit.
        """
        if status_code == 420:
            return False

# List relevant queries
queries = ["this is just to say", "so sweet and so cold", "plums icebox", "which you were probably"]

def is_wcw(status):
    test_text = ' '.join(status.text.lower().split())
    usernames = ['sosweetbot', 'JustToSayBot', 'thatisjustplums', 'EatenBot']
    if status.user.screen_name not in usernames:
        if 'which you were probably' in test_text:
            return True
        elif 'plums' in test_text and 'icebox' in test_text:
            return True
        elif 'this is just to say' in test_text and 'that were in' in test_text:
            return True
        else:
            return False
    else:
        return False

# Initialize stream listener
myStreamListener = MyStreamListener() # Create class instance
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener) # Start stream
myStream.filter(track=queries) # Listen for queries (case insensitive)

# The code below used for testing the custom tweet filter function
# class status():
#      class user():
#           screen_name = 'johnrladd'
     # text = 'I have eaten\n\nThe plums\n\nAnd which\n\nyou were probably'
     # text = 'Plums a little, talk a little, plums a little, talk a little, icebox icebox, icebox icebox'
     # text = 'Totally normal tweet without any reference'

# status = status()
# myStreamListener.on_status(status)
