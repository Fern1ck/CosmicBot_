import tweepy, requests, schedule, redditAPI, nasaAPI, astronauts, time
from funcs import getTime
from variables import TWIITER_CONSUMER_KEY, TWIITER_CONSUMER_SECRET, TWIITER_ACCESS_TOKEN, TWIITER_ACCESS_TOKEN_SECRET

#Autenticacion del bot
auth = tweepy.OAuthHandler(TWIITER_CONSUMER_KEY, TWIITER_CONSUMER_SECRET)
auth.set_access_token(TWIITER_ACCESS_TOKEN, TWIITER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

ASAP_TIME= "12:30"
ASTRONAUTS= "13:30"
TOP_TIME_1= "15:00"
TOP_TIME_2= "16:00"
TOP_TIME_3= "17:00"
NEW_TIME_1= "18:00"
NEW_TIME_2= "22:00"
NEW_TIME_3= "00:00"
MINUTOS = 15

#Se declaran las tareas diarias a ejecutar
schedule.every().day.at(ASTRONAUTS).do(astronauts.Post, api)
schedule.every().day.at(ASAP_TIME).do(nasaAPI.Post, api)
schedule.every().day.at(TOP_TIME_1).do(redditAPI.Top_post, api)
schedule.every().day.at(TOP_TIME_2).do(redditAPI.Top_post, api)
schedule.every().day.at(TOP_TIME_3).do(redditAPI.Top_post, api)
schedule.every().day.at(NEW_TIME_1).do(redditAPI.New_post, api)
schedule.every().day.at(NEW_TIME_2).do(redditAPI.New_post, api)
schedule.every().day.at(NEW_TIME_3).do(redditAPI.New_post, api)

print("[" + getTime() + "] Empiezan a ejecutarse las tareas...")
while(True):
    schedule.run_pending()
    print("[" + getTime() + "] La ejecución se para por " + str(MINUTOS) + " minutos.")
    time.sleep(MINUTOS * 60) #Evita la ejecucion constante del bucle
