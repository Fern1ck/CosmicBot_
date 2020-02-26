import requests, shutil, os, time
from secret import NASA_API_KEY

def Apod_fetch():
    APOD_ENDPOINT = "https://api.nasa.gov/planetary/apod"
    apod = requests.get(APOD_ENDPOINT, params= {"hd": True, "api_key": NASA_API_KEY})
    if(apod.status_code == 200):
        apod = apod.json()
        return {"title": apod["title"], "url": apod["url"], "type": apod["media_type"]}
    else:
        print("HUBO UN ERROR EN EL PEDIDO DE APOD: " + apod)
        return None

def Apod_post(api):
    #Pedido a APOD API 
    APOD = Apod_fetch()
    if(APOD["type"] == "image"):
        #Descargar imagen localmente para despues adjuntarla al tweet
        res = requests.get(APOD["url"], stream=True)
        img_path = "img.jpeg"
        with open(img_path, "wb") as out_file:
            shutil.copyfileobj(res.raw, out_file)
        del res

        #Subir tweet con foto
        Estado = APOD["title"] + "\n#APOD"
        api.update_with_media(status= Estado, filename = img_path)
        tiempo = time.localtime(time.time())
        print("[" + str(tiempo.tm_hour) + ":" +  str(tiempo.tm_min) + ":" + str(tiempo.tm_sec) + "] Se publico el APOD: " + Estado + "con la imagen " + img_path +  "\n")
        os.remove(img_path)
    else:
        Estado = "Check out the Astronomy Video of the Day!: " + APOD["title"] + "\n#AVOD"
        api.update_status(status= Estado)
        tiempo = time.localtime(time.time())
        print("[" + str(tiempo.tm_hour) + ":" +  str(tiempo.tm_min) + ":" + str(tiempo.tm_sec) + "] Se publico el AVOD: " + Estado + " con el video " + APOD['url'] + "\n")
    return None
