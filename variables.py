import os
from dotenv import load_dotenv
load_dotenv()

#TWITTER API
TWIITER_CONSUMER_KEY = os.getenv("TWIITER_CONSUMER_KEY")
TWIITER_CONSUMER_SECRET = os.getenv("TWIITER_CONSUMER_SECRET")
TWIITER_ACCESS_TOKEN = os.getenv("TWIITER_ACCESS_TOKEN")
TWIITER_ACCESS_TOKEN_SECRET = os.getenv("TWIITER_ACCESS_TOKEN_SECRET")

#NASA API
NASA_API_KEY = os.getenv("NASA_API_KEY")

#REDDIT API
REDDIT_CLIENT_ID= os.getenv("REDDIT_CLIENT_ID")
REDDIT_SECRET= os.getenv("REDDIT_SECRET")
REDDIT_ACC_USER= os.getenv("REDDIT_ACC_USER")
REDDIT_ACC_PASS= os.getenv("REDDIT_ACC_PASS")
REDDIT_USER_AGENT= os.getenv("REDDIT_USER_AGENT")
Subreddits_list = ["Space", "Astrophotography", "Astronomy", "Spaceporn"] 
PostsToAvoid = []