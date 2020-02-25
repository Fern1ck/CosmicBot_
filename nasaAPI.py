import requests, tweepy, shutil, os
from secret import nasa_api_key 

def Apod_fetch():
    APOD_ENDPOINT = "https://api.nasa.gov/planetary/apod"
    apod = requests.get(APOD_ENDPOINT, params= {"hd": True, "api_key": nasa_api_key})
    if(apod.status_code == 200):
        apod = apod.json()
        return {"title": apod["title"], "url": apod["url"], "type": apod["media_type"]}

def Apod_post(api):
    #Pedido a APOD API 
    APOD = Apod_fetch() 
    if(APOD["media_type"] == "image"):
        #Descargar imagen localmente para despues adjuntarla al tweet
        res = requests.get(APOD["url"], stream=True)
        img_path = "img.jpeg"
        with open(img_path, "wb") as out_file:
            shutil.copyfileobj(res.raw, out_file)
        del res

        #Subir tweet con foto
        Estado = APOD["title"] + "\n#APOD"
        api.update_with_media(status= Estado, filename = img_path)
        os.remove(img_path)
        print("Se actualizo el estado")
    else:
        Estado = "Check out the Astronomy Video of the Day!: " + APOD["title"] + "\n#APOD"
        api.update_status(status= Estado)
        print("Se actualizo el estado")
