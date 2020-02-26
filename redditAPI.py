import praw, random, requests, shutil, os, time
from PIL import Image #Necesario para redimensionar la imagen
from resizeimage import resizeimage #Necesario para redimensionar la imagen
from secret import REDDIT_CLIENT_ID, REDDIT_SECRET, REDDIT_ACC_PASS, REDDIT_ACC_USER

reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                    client_secret=REDDIT_SECRET,
                    password=REDDIT_ACC_PASS,
                    user_agent='Cosmic Bot',
                    username=REDDIT_ACC_USER)

Subreddits_list = ["Space", "Astrophotography", "Astronomy", "Spaceporn"] 

def process_title(titulo):
    if(" [OC]" in titulo):
        return titulo.replace(" [OC]", "")
    elif("[OC] " in titulo):
        return titulo.replace("[OC] ", "")
    elif("[OC]" in titulo):
        return titulo.replace("[OC]", "")
    else:
        return titulo

def Redimensionar(img_path): # FIXME 
    #Redimensiona la imagen si se excede de los limites de resolucion de twitter 8192x8192
    RES_LIMIT= 8192
    with Image.open(img_path) as image:
        width, height = image.size
        if(width > RES_LIMIT or height > RES_LIMIT):
            new_size = (RES_LIMIT, RES_LIMIT)
            image= image.resize(new_size)
            image.save(img_path, quality= 65)
        image.show()
    return None

def Reddit_top_post(api):
    chosen_sub = random.choice(Subreddits_list) #Elige algun subreddit al azar
    print("SUBREDDIT ELEGIDO PARA EL TOP: " + chosen_sub)
    #Aunque solo se pida un post, la funcion devuelve un array. Este for solo itera una vez.
    for submission in reddit.subreddit(chosen_sub).top(time_filter= 'month', limit=1): 
        Estado = '"' + process_title(submission.title) + '". Submitted to https://www.reddit.com/r/' + str(submission.subreddit) + '/ by /u/' + str(submission.author)

        #Si la publicación solo tiene algo multimedia
        if(submission.selftext == ""):
            #Descargar imagen localmente para despues adjuntarla al tweet
            res = requests.get(submission.url, stream=True)
            img_path = "reddit.jpeg"
            with open(img_path, "wb") as out_file:
                shutil.copyfileobj(res.raw, out_file)
            del res

            Redimensionar(img_path)

            #Subir tweet con foto
            api.update_with_media(filename= img_path, status= Estado)
            os.remove(img_path)
            tiempo = time.localtime(time.time())
            print("[" + str(tiempo.tm_hour) + ":" +  str(tiempo.tm_min) + ":" + str(tiempo.tm_sec) + "] Se publico el tweet del top post del subreddit " + str(submission.subreddit) + "\n")
        else:
            #Subir tweet
            api.update_status(status= Estado + submission.selftext)
            tiempo = time.localtime(time.time())
            print("[" + str(tiempo.tm_hour) + ":" +  str(tiempo.tm_min) + ":" + str(tiempo.tm_sec) + "] Se publico el tweet del top post del subreddit " + str(submission.subreddit) + "\n")
    return None

def Reddit_new_post(api):
    chosen_sub = random.choice(Subreddits_list) #Elige algun subreddit al azar
    print("SUBREDDIT ELEGIDO PARA LOS ULTIMOS 5 POSTS: " + chosen_sub)

    #Consigue el mejor post de los 5 más recientes
    submissions_list = []
    for submission in reddit.subreddit(chosen_sub).new(limit=5): 
        submissions_list.append(submission)
    submissions_list.sort(key=lambda x: x.ups, reverse= True)
    best_one= submissions_list[0]

    Estado = '"' + best_one.title + '". Submitted to https://www.reddit.com/r/' + str(best_one.subreddit) + '/ by /u/' + str(best_one.author)

    if(best_one.selftext == ""):
        #Descargar imagen localmente para despues adjuntarla al tweet
        res = requests.get(best_one.url, stream=True)
        img_path = "best_out_of_5_reddit.jpeg"
        with open(img_path, "wb") as out_file:
            shutil.copyfileobj(res.raw, out_file)
        del res

        Redimensionar(img_path)

        #Subir tweet con foto
        api.update_with_media(filename= img_path, status= Estado)
        os.remove(img_path)
        tiempo = time.localtime(time.time())
        print("[" + str(tiempo.tm_hour) + ":" +  str(tiempo.tm_min) + ":" + str(tiempo.tm_sec) + "] Se publico el tweet del top post del subreddit " + str(best_one.subreddit) + "\n")
    else:
        #Subir tweet
        api.update_status(status= Estado + best_one.selftext)
        tiempo = time.localtime(time.time())
        print("[" + str(tiempo.tm_hour) + ":" +  str(tiempo.tm_min) + ":" + str(tiempo.tm_sec) + "] Se publico el mejor post mas reciente del subreddit " + str(best_one.subreddit) + "\n")
    return None