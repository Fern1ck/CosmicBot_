import requests

def get_Astronauts():
    astro= requests.get("http://api.open-notify.org/astros.json")
    if(astro.status_code == 200):
        astro = astro.json()
        if(astro["message"] == "success"):
            return astro

if __name__ == "__main__":  
    print(get_Astronauts())