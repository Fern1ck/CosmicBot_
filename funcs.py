from PIL import Image #Necesario para redimensionar la imagen
from datetime import datetime
from resizeimage import resizeimage #Necesario para redimensionar la imagen
from secret import Subreddits_list

def process_title(titulo): #Procesa los titulos de los posts en reddit.
    if(" [OC]" in titulo):
        return titulo.replace(" [OC]", "")
    elif("[OC] " in titulo):
        return titulo.replace("[OC] ", "")
    elif("[OC]" in titulo):
        return titulo.replace("[OC]", "")
    else:
        return titulo

def Redimensionar(img_path): #Redimensiona la imagen si se excede de los limites de resolucion de twitter 8192x8192
    RES_LIMIT= 1920
    with Image.open(img_path) as image:
        width, height = image.size
        if(width > RES_LIMIT or height > RES_LIMIT):
            new_size = (RES_LIMIT, RES_LIMIT)
            image.thumbnail(new_size, Image.ANTIALIAS)
            image.save(img_path, optimize= True, quality= 85)
        image.show()
    return None

def isOriginal(titulo, TWEETS): #Comprueba si el post elegido para publicarse ya fue publicado en el timeline del bot
    for status in TWEETS:
        if(process_title(titulo) in status):
            break
    else: #Si no se ejecuta el break
        return True
    return False

def getTime():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

class Scheduling():
    """Clase que organiza las funciones dedicadas a 
    planificar en que orden se van a sacar las fotos de
    los subreddits
    """
    def __init__(self, PATH):
        self.path = PATH

    def __OpenFile(self):
        try:
            file = open(self.path, "r+") #Abrir para lectura y escritura
        except FileNotFoundError:
            file = open(self.path, "w") #Lo crea
            file.close()
            file = open(self.path, "r+") #Abrir para lectura y escritura
            file.write(Subreddits_list[0].lower().capitalize())
        return file

    def __get_LastSub(self):
        f = self.__OpenFile()
        LastSub = f.read()
        f.close()
        return LastSub

    def get_NextSub(self):
        contents = self.__get_LastSub()
        NextSubIndex= Subreddits_list.index(contents) + 1
        try:
            NextSub = Subreddits_list[NextSubIndex]
        except:
            NextSub = Subreddits_list[0]
        return NextSub

    def set_NewSub(self, newSub):
        if(newSub.lower().capitalize() not in Subreddits_list):
            raise Exception #El subreddit especificado no forma parte de la lista de subreddits.

        f = self.__OpenFile()
        f.seek(0) #Cambia la posicion dentro del archivo al principio
        f.truncate() #Borra todo lo que exceda la posicion dentro del archivo
        f.write(newSub.lower().capitalize())
        f.close()
        return None