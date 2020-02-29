import tweepy, requests, schedule, time, redditAPI, nasaAPI, astronauts
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

#astronauts.get_Astronauts(api)
#nasaAPI.Apod_post(api)
#redditAPI.Reddit_top_post(api)
for i in range(2):    
    redditAPI.Reddit_new_post(api)
    redditAPI.Reddit_top_post(api)

"""
#schedule.every().day.at(ASTRONAUTS).do(astronauts.get_Astronauts, api)
#schedule.every().day.at(ASAP_TIME).do(nasaAPI.Apod_post, api)
#schedule.every().day.at(TOP_TIME).do(redditAPI.Reddit_top_post, api)
#schedule.every().day.at(NEW_TIME).do(redditAPI.Reddit_new_post, api)

print("[" + str(time.localtime(time.time()).tm_hour) + ":" +  str(time.localtime(time.time()).tm_min) + ":" + str(time.localtime(time.time()).tm_sec) + "] Empiezan a ejecutarse las tareas...")
while(True):
    schedule.run_pending()
    tiempo = time.localtime(time.time())
    print("[" + str(tiempo.tm_hour) + ":" +  str(tiempo.tm_min) + ":" + str(tiempo.tm_sec) + "] La ejecución se para por " + str(SEGUNDOS) + " segundos.")
    time.sleep(2) #Evita la ejecucion constante del bucle
"""