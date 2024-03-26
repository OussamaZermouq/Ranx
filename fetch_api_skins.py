import requests
import base64
import urllib3
from fetch_api import get_puuid

def get_port():
    try:
        with open("C:/Users/oussa/AppData/Local/Riot Games/Riot Client/Config/lockfile", 'r') as lockfile:
            return lockfile.read().split(':', 5)[2]
    except FileNotFoundError:
        print("No file")
    except Exception as e:
        print(e)

def get_password():
    try:
        with open("C:/Users/oussa/AppData/Local/Riot Games/Riot Client/Config/lockfile", 'r') as lockfile:
            return lockfile.read().split(':', 5)[3]
    except FileNotFoundError:
        print("No file")
    except Exception as e:
        print(e)

def fetch_cred():
    #this function works but the issue is that the creds that are 
    #returned are for the user that's logged in the riot client, 
    #which makes it impossible to genereate to other users
    #find a way to log into the account that we need.
    #TODO: https://valapidocs.techchrism.me/endpoint/cookie-reauth
    #Store the cookies after this request
    url = f"https://127.0.0.1:{get_port()}/entitlements/v1/token"
    
    string = b"riot:" + get_password().encode('utf-8')
    encoded_credentials = base64.b64encode(string).decode('utf-8')
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f'Basic {encoded_credentials}'
    }
    
    response = requests.request("GET", url, headers=headers, verify=False)
    return response.json()

def get_token_request():
    urllib3.disable_warnings()
    return fetch_cred()['accessToken']

def get_entitlment_token():
    urllib3.disable_warnings()
    return fetch_cred()['token']



def fetch_user_daily_skins(puuid:str):
    url = f'https://pd.eu.a.pvp.net/store/v2/storefront/{puuid}'
    headers = {
        "X-Riot-Entitlements-JWT": f"{get_entitlment_token()}",
        "Authorization": f"Bearer {get_token_request()}"
    }
    
    response = requests.request("GET", url,  headers=headers)
    return response.json()['SkinsPanelLayout']['SingleItemOffers']


def fetch_skin_item(uuid:str):
    url = f"https://valorant-api.com/v1/weapons/skinlevels/{uuid}"
    response = requests.request("GET", url)
    if response.json()['status'] == 200:
        return response.json()
    


def get_player_info():
    url = 'https://auth.riotgames.com/userinfo'
    headers = {
        "Authorization": f"Bearer {get_token_request()}"
    }
    
    response = requests.request("GET", url,  headers=headers)
    return response.json()



