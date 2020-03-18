import tweepy, requests, schedule, redditAPI, nasaAPI, astronauts, time
from funcs import getTime
from secret import TWIITER_CONSUMER_KEY, TWIITER_CONSUMER_SECRET, TWIITER_ACCESS_TOKEN, TWIITER_ACCESS_TOKEN_SECRET

#Autenticacion del bot
auth = tweepy.OAuthHandler(TWIITER_CONSUMER_KEY, TWIITER_CONSUMER_SECRET)
auth.set_access_token(TWIITER_ACCESS_TOKEN, TWIITER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

ASTRONAUTS= "13:30"
ASAP_TIME= "11:30"
TOP_TIME= "17:00"
NEW_TIME= "22:00"
SEGUNDOS = 5

schedule.every().day.at(ASTRONAUTS).do(astronauts.Post, api)
schedule.every().day.at(ASAP_TIME).do(nasaAPI.Post, api)
schedule.every().day.at(TOP_TIME).do(redditAPI.Top_post, api)
schedule.every().day.at(NEW_TIME).do(redditAPI.New_post, api)

print("[" + getTime() + "] Empiezan a ejecutarse las tareas...")
while(True):
    schedule.run_pending()
    print("[" + getTime() + "] La ejecución se para por " + str(SEGUNDOS) + " segundos.")
    time.sleep(SEGUNDOS) #Evita la ejecucion constante del bucle