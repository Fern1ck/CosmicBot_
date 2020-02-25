import tweepy
import requests
from secret import twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_token_secret
from nasaAPIs import Apod_post
from redditAPI import Reddit_post

#Autenticacion del bot
auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
auth.set_access_token(twitter_access_token, twitter_access_token_secret)
api = tweepy.API(auth)

#Apod_post(api)
Reddit_post(api)