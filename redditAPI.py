import praw, random, requests, shutil, os, time
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
    else:
        return titulo

def Reddit_top_post(api):
    chosen_sub = random.choice(Subreddits_list) #Elige algun subreddit al azar
    print("SUBREDDIT ELEGIDO: " + chosen_sub)

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

            #Subir tweet con foto
            api.update_with_media(filename= img_path, status= Estado)
            os.remove(img_path)
            tiempo = time.localtime(time.time())
            print("[" + str(tiempo.tm_hour) + ":" +  str(tiempo.tm_min) + ":" + str(tiempo.tm_sec) + "] Se publico el tweet del top post del subreddit " + str(submission.subreddit) + "\n")
        else:
            #Subir tweet
            api.update_status(status= Estado)
            tiempo = time.localtime(time.time())
            print("[" + str(tiempo.tm_hour) + ":" +  str(tiempo.tm_min) + ":" + str(tiempo.tm_sec) + "] Se publico el tweet del top post del subreddit " + str(submission.subreddit) + "\n")
    return None

def Reddit_new_post(api):
    chosen_sub = random.choice(Subreddits_list) #Elige algun subreddit al azar
    print("SUBREDDIT ELEGIDO: " + chosen_sub)
    chosen_sub = "space"

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

        #Subir tweet con foto
        api.update_with_media(filename= img_path, status= Estado)
        os.remove(img_path)
        tiempo = time.localtime(time.time())
        print("[" + str(tiempo.tm_hour) + ":" +  str(tiempo.tm_min) + ":" + str(tiempo.tm_sec) + "] Se publico el tweet del top post del subreddit " + str(best_one.subreddit) + "\n")
    else:
        #Subir tweet
        api.update_status(status= Estado)
        tiempo = time.localtime(time.time())
        print("[" + str(tiempo.tm_hour) + ":" +  str(tiempo.tm_min) + ":" + str(tiempo.tm_sec) + "] Se publico el mejor post mas reciente del subreddit " + str(best_one.subreddit) + "\n")
    return None