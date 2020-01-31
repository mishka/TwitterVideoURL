import json
import builtins as __builtin__
from os import getenv
from time import gmtime, strftime
from dotenv import load_dotenv
from tweepy import API
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import StreamListener


load_dotenv()
KEYWORDS = ["enter", "keywords", "to", "track", "here", "api", "supports", "up", "to", "400", "keywords"]
CONSUMER_KEY = getenv('CONSUMER')
CONSUMER_SECRET = getenv('CONSUMER_SECRET')
ACCESS_TOKEN = getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = getenv('ACCESS_TOKEN_SECRET')

AUTH = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
AUTH.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = API(AUTH, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)


def print(*args, **kwargs):
    return __builtin__.print(strftime("| %H:%M:%S |", gmtime()), *args, **kwargs)

class Tracker(StreamListener):
    def on_data(self, tweet):
        tweet_json = json.loads(tweet)

        user_name, user_tag = tweet_json['user']['name'], tweet_json['user']['screen_name']
        reply_id, parent_id= tweet_json['id'], tweet_json['in_reply_to_status_id']

        print(f'New request from: {user_name}, {user_tag}')
        print(f'Parent ID, Reply ID: {parent_id}, {reply_id}')
        
        parent_tweet = api.get_status(parent_id, tweet_mode = 'extended')
        result = 0
        
        try:
            video_url = parent_tweet.extended_entities['media'][0]['video_info']['variants'][0]['url']
            result = 1
        except AttributeError:
            print("Video is not available, skipping\n")

        if result:
            api.update_status(video_url, in_reply_to_status_id = reply_id, auto_populate_reply_metadata = True)
            print(f'{video_url}\nRequest completed!\n')

    @staticmethod
    def on_error(status_code):
        print(f'Error: {repr(status_code)}')


if __name__ == '__main__':
    print('Listening to the stream!\n')
    T_STREAM = Stream(AUTH, Tracker())
    T_STREAM.filter(track = KEYWORDS, is_async = True)
