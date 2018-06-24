#! /usr/bin/env python3

from twython import Twython, TwythonStreamer, TwythonError
from secrets import *

# Initialize twython with relevant secret keys
api = Twython(consumer_key, consumer_secret, access_token, access_token_secret)

class MyStreamListener(TwythonStreamer):
    """
    This class defines how Twitter's streaming API should behave.
    """

    def on_success(self, status):
        """
        When a status is found, filter for the exact phrase and retweet.
        """
        # print(status['text'], status['id'])
        if is_wcw(status): # Use function for testing the phrase
            try:
                api.retweet(id=status['id'])
            except TwythonError:
                pass

    def on_error(self, status_code, data):
        """
        When API returns error, keep going unless the error is for rate limit.
        """
        if status_code == 420:
            self.disconnect()

# List relevant queries
queries = ["this is just to say", "so sweet and so cold", "plums icebox", "which you were probably"]
queries = ','.join(queries)

def is_wcw(status):
    """
    Determines whether or not the tweet is a William Carlos Williams parody,
    using the same list of queries that the streaming API uses.
    """
    test_text = ' '.join(status['text'].lower().split()) # Remove capital letters and excessive whitespace/linebreaks
    usernames = ['sosweetbot', 'JustToSayBot', 'thatisjustplums', 'EatenBot', 'the_niche_bot', 'KristenCostel10', 'litabottal', 'pythonnina', 'alatest5', 'LisaRob96585017','Stilson28400122', 'JohnDun40217560','Cordelia28', 'Rick63556459', 'botsnthings', 'timbot301', 'Rachel53001595'] # Block screen_names of known parody accounts
    if status['user']['screen_name'] not in usernames and all(u not in status['text'] for u in usernames):
        if 'which you were probably' in test_text: # Capture parodies of the form
            return True
        elif 'plums' in test_text and 'icebox' in test_text: # Capture parodies of the content
            return True
        elif 'this is just to say' in test_text and 'that were in' in test_text: # Get only relevant instances of "this is just to say"
            return True
        elif 'this is just to say' in test_text and 'forgive me' in test_text:
            return True
        elif 'this is just to say' in test_text and 'and so' in test_text:
            return True
        elif 'so sweet and so cold' in test_text and 'the arms of the ocean' not in test_text: # Get 'so sweet and so cold' tweets that aren't quoting Florence and the Machine
            return True
        else:
            return False
    else:
        return False

# Initialize stream listener
stream = MyStreamListener(consumer_key, consumer_secret, access_token, access_token_secret) # Create class instance

while True:
	try:
		stream.statuses.filter(track=queries) # Listen for queries (case insensitive)
	except:
		continue

# The code below used for testing the custom tweet filter function
# class status():
#      class user():
#           screen_name = 'johnrladd'
     # text = 'I have eaten\n\nThe plums\n\nAnd which\n\nyou were probably'
     # text = 'Plums a little, talk a little, plums a little, talk a little, icebox icebox, icebox icebox'
     # text = 'Totally normal tweet without any reference'

# status = status()
# myStreamListener.on_status(status)
