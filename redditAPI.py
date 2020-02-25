import praw, tweepy, random, requests, shutil, os, sched
from secret import reddit_client_id, reddit_secret, reddit_acc_pass, reddit_acc_user

def Reddit_post(api):
    reddit = praw.Reddit(client_id=reddit_client_id,
                         client_secret=reddit_secret,
                         password=reddit_acc_pass,
                         user_agent='useragent',
                         username=reddit_acc_user)

    Subreddits_list = ["Space", "Astrophotography", "Astronomy", "Spaceporn"] 
    chosen_sub = random.choice(Subreddits_list) #Elige algun subreddit al azar

    #Aunque solo se pida un post, la funcion devuelve un array. Este for solo itera una vez.
    for submission in reddit.subreddit(chosen_sub).top(time_filter= 'day', limit=1): 
        Estado = '"' + submission.title + '"\nsubmitted by https://www.reddit.com/user/' + str(submission.author) + " to https://www.reddit.com/r/" + str(submission.subreddit)
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
            print("Se publico el tweet del top post del subreddit " + str(submission.subreddit))
        else:
            #Subir tweet
            api.update_status(status= Estado)
            print("Se publico el tweet del top post del subreddit " + str(submission.subreddit))