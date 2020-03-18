import requests, shutil, os, tweepy
from datetime import datetime
from funcs import isOriginal, getTime
from secret import NASA_API_KEY

def Link_format(link): #Se formatea los links de youtube para que muestren una preview en el tweet
    if("embed/" in link):
        return link.replace("embed/", "watch?v=")
    else:
        return link

def Apod_fetch():
    APOD_ENDPOINT = "https://api.nasa.gov/planetary/apod"
    apod = requests.get(APOD_ENDPOINT, params= {"hd": True, "api_key": NASA_API_KEY})
    if(apod.status_code == 200):
        try:
            apod = apod.json()
            return {"title": apod["title"], "url": apod["url"], "type": apod["media_type"]}
        except:
            print("[" + getTime() + "] Hubo un error en el pedido de APOD.")

    else:
        print("[" + getTime() + "] Hubo un error en el pedido de APOD. Codigo de error: " + str(apod.status_code))
        return None

def Post(api):
    print("[" + getTime() + "] Se empieza la función de nasaAPI.py: Post(api)")
    TIMELINE_ACTUAL= tweepy.Cursor(api.user_timeline, screen_name=api.me().screen_name, tweet_mode="extended").items()
    Tweets = []
    for x in TIMELINE_ACTUAL:
        Tweets.append(x._json["full_text"])

    #Pedido a APOD API 
    APOD = Apod_fetch()
    if(isOriginal(APOD["title"], Tweets)):
        if(APOD["type"] == "image"):    
            #Descargar imagen localmente para despues adjuntarla al tweet
            res = requests.get(APOD["url"], stream=True)
            img_path = "img.jpeg"
            with open(img_path, "wb") as out_file:
                shutil.copyfileobj(res.raw, out_file)
            del res

            #Subir tweet con foto
            Estado = '"' + APOD["title"] + '" #APOD #Astronomy #Nasa'
            api.update_with_media(status= Estado, filename = img_path)
            print("[" + getTime() + "] Se publico el APOD: " + Estado)
            os.remove(img_path)
        else:
            URL= Link_format(APOD["url"])
            Estado = APOD["title"] + " " + URL + " #APOD #Astronomy #Nasa"
            api.update_status(status= Estado)
            print("[" + getTime() + "] Se publico el AVOD: " + Estado + " con el video " + APOD['url'])
    else:
        print("[" + getTime() + "] El APOD de la NASA " + APOD["title"] + " ya fue publicado en el timeline. No se publicó nada ahora mismo.")
        del APOD
    print("[" + getTime() + "] Se termina la función de nasaAPI.py: Post(api)\n")
    return None