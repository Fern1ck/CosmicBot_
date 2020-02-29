import praw, random, requests, shutil, os, time, tweepy, funcs
from secret import REDDIT_CLIENT_ID, REDDIT_SECRET, REDDIT_ACC_PASS, REDDIT_ACC_USER, REDDIT_USER_AGENT, Subreddits_list

reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                    client_secret=REDDIT_SECRET,
                    password=REDDIT_ACC_PASS,
                    user_agent=REDDIT_USER_AGENT,
                    username=REDDIT_ACC_USER)

def Choose_subreddit(): #Elige algun subreddit al azar
    return random.choice(Subreddits_list)

def get_top(chosen_sub, LIMITE, Tweets): 
    for post in reddit.subreddit(chosen_sub).top(time_filter= 'month', limit=LIMITE): 
        if(funcs.isOriginal(post.title, Tweets)):
            print(post.title + " ====> ES ORIGINAL")
            return post
        else:
            print(post.title + " ====> NO ES ORIGINAL")
    return get_top(chosen_sub, LIMITE + 30, Tweets)

def Reddit_top_post(api):
    chosen_sub = Choose_subreddit()
    TIMELINE_ACTUAL= tweepy.Cursor(api.user_timeline, screen_name=api.me().screen_name, tweet_mode="extended").items()
    Tweets = []
    for x in TIMELINE_ACTUAL:
        Tweets.append(x._json["full_text"])

    submission = get_top(chosen_sub, 30, Tweets)
    Estado = '"' + funcs.process_title(submission.title) + '"'
    
    if(submission.selftext == "" and ("jpg" in submission.url or "jpeg" in submission.url or "png" in submission.url)):
        #Si la publicación con una foto
        res = requests.get(submission.url, stream=True)
        img_path = ""
        if("jpeg" in submission.url):
            img_path = "redditTOP.jpeg"
        elif("jpg" in submission.url):
            img_path = "redditTOP.jpg"
        elif("png" in submission.url):
            img_path = "redditTOP.png"

        with open(img_path, "wb") as out_file:
            shutil.copyfileobj(res.raw, out_file)
        del res

        try:
            funcs.Redimensionar(img_path)
            try:
                api.update_with_media(filename= img_path, status= Estado + " #Astronomy #Space") #Subir tweet con foto 
            except tweepy.error.TweepError as e:
                if("'code': 186" in str(e)):
                    pass #AGREGAR ID A LISTA PARA NO PUBLICAR
        except:
            try:
                api.update_status(status= Estado + " " + submission.url + " #Astronomy #Space")
            except tweepy.error.TweepError as e:
                if("'code': 186" in str(e)):
                    pass #AGREGAR ID A LISTA PARA NO PUBLICAR

        os.remove(img_path)
        tiempo = time.localtime(time.time())
        print("[" + str(tiempo.tm_hour) + ":" + str(tiempo.tm_min) + ":" + str(tiempo.tm_sec) + "] Se publico el tweet\n")
    else:
        #Subir tweet con el link de lo adjuntado
        try:
            api.update_status(status= Estado + " " + submission.url + " #Astronomy #Space")
        except tweepy.error.TweepError as e:
                if("'code': 186" in str(e)):
                    pass #AGREGAR ID A LISTA PARA NO PUBLICAR
                
        tiempo = time.localtime(time.time())
        print("[" + str(tiempo.tm_hour) + ":" + str(tiempo.tm_min) + ":" + str(tiempo.tm_sec) + "] Se publico el tweet\n")
    return None

def get_new(chosen_sub, LIMITE, Tweets): 
    #Consigue el mejor post de los más recientes
    submissions_list = []
    for submission in reddit.subreddit(chosen_sub).new(limit= LIMITE): 
        submissions_list.append(submission)

    submissions_list.sort(key= lambda x: x.ups, reverse= True)

    for post in submissions_list:
        if(funcs.isOriginal(post.title, Tweets)):
            print(post.title + " ====> ES ORIGINAL")
            return post
        else:
            print(post.title + " ====> NO ES ORIGINAL")
    return get_new(chosen_sub, LIMITE + 5, Tweets)

def Reddit_new_post(api):
    chosen_sub = random.choice(Subreddits_list)
    TIMELINE_ACTUAL= tweepy.Cursor(api.user_timeline, screen_name=api.me().screen_name, tweet_mode="extended").items()
    Tweets = []
    for x in TIMELINE_ACTUAL:
        Tweets.append(x._json["full_text"])
    
    best_one = get_new(chosen_sub, 5, Tweets)
    Estado= '"' + funcs.process_title(best_one.title) + '"'

    if(best_one.selftext == "" and ("jpg" in best_one.url or "jpeg" in best_one.url or "png" in best_one.url)):
        #Si la publicación tiene una foto
        res = requests.get(best_one.url, stream=True)

        img_path = ""
        if("jpeg" in best_one.url):
            img_path = "redditNEW.jpeg"
        elif("jpg" in best_one.url):
            img_path = "redditNEW.jpg"
        elif("png" in best_one.url):
            img_path = "redditNEW.png"

        with open(img_path, "wb") as out_file:
            shutil.copyfileobj(res.raw, out_file)
        del res

        #Manejo de errores para tweetear. El nombre del post tiene que estar en el tweet, sino va a publicar doble cuando se compruebe si es original o no.
        try:
            funcs.Redimensionar(img_path)
            try:
                api.update_with_media(filename= img_path, status= Estado + " #Astronomy #Space")
            except tweepy.error.TweepError as e:
                if("'code': 186" in str(e)):
                    pass #AGREGAR ID A LISTA PARA NO PUBLICAR
        except:
            try:
                api.update_status(status= Estado + " " + best_one.url + " #Astronomy #Space")
            except tweepy.error.TweepError as e:
                if("'code': 186" in str(e)):
                    pass #AGREGAR ID A LISTA PARA NO PUBLICAR
        
        os.remove(img_path)
        tiempo = time.localtime(time.time())
        print("[" + str(tiempo.tm_hour) + ":" +  str(tiempo.tm_min) + ":" + str(tiempo.tm_sec) + "] Se publico el tweet.\n")
    else:
        #Subir tweet con el link de lo adjuntado
        try:
            api.update_status(status= Estado + " " + best_one.url + " #Astronomy #Space")
        except tweepy.error.TweepError as e:
            if("'code': 186" in str(e)):
                    pass #AGREGAR ID A LISTA PARA NO PUBLICAR

        tiempo = time.localtime(time.time())
        print("[" + str(tiempo.tm_hour) + ":" +  str(tiempo.tm_min) + ":" + str(tiempo.tm_sec) + "] Se publico el mejor post mas reciente del subreddit " + str(best_one.subreddit) + "\n")
    return None