import logging
import tweepy
from tweepy import OAuthHandler
import pymongo
import config
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='../logs/log_tweetcollector.log', filemode='w'
)

# OAuth 2 Authentication
AUTH = tweepy.OAuthHandler(config.CONSUMER_TOKEN, config.CONSUMER_SECRET)
AUTH.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)

# Mongo DB
client = pymongo.MongoClient("mongodb://mongodb:27017/")

class MongoStreamListener(tweepy.StreamListener):
    """
    https://github.com/tweepy/tweepy/blob/v3.8.0/tweepy/streaming.py
    """

    def __init__(self, max_tweets, client, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter=0
        self.client = client
        self.max_tweets = max_tweets

    def on_connect(self):
        logging.info("connected to stream")

    def on_status(self, status): 

            # specify what data should be captured from tweets
            tweet = {'date': status.created_at, 'text': status.text}
            # tweet = {'date': status.created_at}
          
            logging.critical(f'\n\n\nTWEET INCOMING: {tweet["text"]}\n\n\n')

            print(f'{status.created_at}: {status.text}')

            self.client.twitter.tweets.insert_one(tweet)
            logging.info("inserted one tweet in mongodb")


            # tweet = {'date': status.created_at, 'text': status.text}
            # self.client.twitter.tweets.insert_one(tweet)


            self.counter += 1
            if (self.counter >= self.max_tweets):
                logging.info(f'inserted {self.counter} tweets')
                return False 


    def on_error(self, status_code):
        logging.warning(f'error code during stream: {status_code}')
        return True # try to reconnect using backoff strategy

stream = tweepy.Stream(
    auth = AUTH, 
    listener=MongoStreamListener(max_tweets=5, client=client))

stream.filter(
    track=['covid'],
    languages=['en']
)
