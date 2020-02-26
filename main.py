import tweepy, requests, schedule, time
from secret import TWIITER_CONSUMER_KEY, TWIITER_CONSUMER_SECRET, TWIITER_ACCESS_TOKEN, TWIITER_ACCESS_TOKEN_SECRET
from nasaAPI import Apod_post
from redditAPI import Reddit_top_post, Reddit_new_post

#Autenticacion del bot
auth = tweepy.OAuthHandler(TWIITER_CONSUMER_KEY, TWIITER_CONSUMER_SECRET)
auth.set_access_token(TWIITER_ACCESS_TOKEN, TWIITER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

ASAP_TIME= "11:30"
TOP_TIME= "16:53"
NEW_TIME= "22:00"
SEGUNDOS = 120

schedule.every().day.at(ASAP_TIME).do(Apod_post, api)
schedule.every().day.at(TOP_TIME).do(Reddit_top_post, api)
schedule.every().day.at(NEW_TIME).do(Reddit_new_post, api)

print("[" + str(time.localtime(time.time()).tm_hour) + ":" +  str(time.localtime(time.time()).tm_min) + ":" + str(time.localtime(time.time()).tm_sec) + "] Empiezan a ejecutarse las tareas...")
while(True):
    schedule.run_pending()
    tiempo = time.localtime(time.time())
    print("[" + str(tiempo.tm_hour) + ":" +  str(tiempo.tm_min) + ":" + str(tiempo.tm_sec) + "] La ejecución se para por " + str(SEGUNDOS) + " segundos.")
    time.sleep(SEGUNDOS) #Evita la ejecucion constante del bucle