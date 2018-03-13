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
        if is_wcw(status): # Use function for testing the phrase
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
    """
    Determines whether or not the tweet is a William Carlos Williams parody,
    using the same list of queries that the streaming API uses.
    """
    test_text = ' '.join(status.text.lower().split()) # Remove capital letters and excessive whitespace/linebreaks
    usernames = ['sosweetbot', 'JustToSayBot', 'thatisjustplums', 'EatenBot', 'the_niche_bot'] # Block screen_names of known parody accounts
    if status.user.screen_name not in usernames and all(u not in status.text for u in usernames):
        if 'which you were probably' in test_text: # Capture parodies of the form
            return True
        elif 'plums' in test_text and 'icebox' in test_text: # Capture parodies of the content
            return True
        elif 'this is just to say' in test_text and 'that were in' in test_text: # Get only relevant instances of "this is just to say"
            return True
        elif 'so sweet and so cold' in test_text and 'in the arms of the ocean' not in test_text: # Get 'so sweet and so cold' tweets that aren't quoting Florence and the Machine
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
