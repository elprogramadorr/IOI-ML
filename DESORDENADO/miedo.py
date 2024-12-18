import requests
import pandas as pd

def get_bolivian_competitors():
    # Endpoint de la API de Codeforces para obtener todos los usuarios
    url = "https://codeforces.com/api/user.ratedList"
    
    try:
        # Solicitar datos de la API
        response = requests.get(url)
        response = response.json()
        bolivian_user = []
        for user in response["result"]:
            if "country" in user and user["country"] == "Bolivia":
                
                user = {
                    "handle": user["handle"],
                    "rating": user["rating"]
                }
                bolivian_user.append(user)
        
        df = pd.DataFrame(bolivian_user)
        df.to_csv("bolivian_users.csv", index=False)
        return bolivian_user
    

    except Exception as e:
        print(f"Error: {e}")
        return None
        
        

# Ejecutar la función
print(get_bolivian_competitors())
