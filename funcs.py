from PIL import Image #Necesario para redimensionar la imagen
from resizeimage import resizeimage #Necesario para redimensionar la imagen

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