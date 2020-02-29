import requests, time

def get_Astronauts(api):
    # Si no es el primer dia del mes no hace nada
    day_of_month = time.localtime().tm_mday
    if day_of_month != 1:
        return 

    astro= requests.get("http://api.open-notify.org/astros.json")
    if(astro.status_code == 200 and astro.json()["message"] == "success"):
        count = astro.json()["number"]
        if(count > 0):
            print("At the moment, there are " + str(count) + " astronauts in space: ", end="")
            for i in astro.json()["people"]:
                if(count > 0):
                    print(i["name"], end="")
                    count = count - 1
                    if(count == 1):
                        print(" and", end=" ")
                    elif(count > 1):
                        print(", ", end="")
                    elif(count == 0):
                        print(".")
                else:
                    print("At the moment, there are no astronauts in space.")
    #IMPLEMENTAR PUBLICACION
    return None