import requests
from requests_cache import CachedSession
import time


def fetch_user(username:str, tag:str):
    url = f'https://api.henrikdev.xyz/valorant/v1/account/{username}/{tag}?force=false'
    headers = {
        "Accept": "application/json"
    }
    urls_expire_after = {
        url: -1,    
    }
    session = CachedSession('session', urls_expire_after=urls_expire_after, cache_control='no-cache')
    response = session.get(url, headers=headers)
    if response.json()['status']==200:
        return response.json()
    elif response.json()['status'] == 429:
        print('Rate limit exceeded, sleeping for 60 seconds')
        return -2
    else:
        print(response.json()['status'])
        return -1

def get_puuid(username:str, tag:str):
    data = fetch_user(username=username, tag=tag)
    if data['status'] == 200:
        puuid = data['data']['puuid']
        return puuid
    return data



#TODO:if a new season or act is added, add it here.
seasons = ['e1a1','e1a2','e1a3','e2a1','e2a2','e2a3','e3a1','e3a2','e3a3',
           'e4a1','e4a2','e4a3','e5a1','e5a2','e5a3','e6a1','e6a2','e6a3',
           'e7a1','e7a2','e7a3','e8a1','e8a2','e8a3']

#TODO: return a dict that has the rank and the season at the same time
def fetch_rank(puuid:str, episode:str):
    url = f'https://api.henrikdev.xyz/valorant/v2/by-puuid/mmr/eu/{puuid}?season={episode}'
    headers = {
        "Accept": "application/json"
    }
    urls_expire_after = {
        url: -1,
    }
    session = CachedSession('session_ranks', urls_expire_after=urls_expire_after, cache_control='no-cache')
    response = session.get(url, headers=headers)
    if response.json()['status'] == 200:
        return response.json()['data']['final_rank_patched']
    elif response.json()['status'] == 429:
        return -2
    else:
        return -1

def return_last_filled_rank(puuid:str):
    for season in reversed(seasons):
        rank = fetch_rank(puuid = puuid, episode = season)
        if rank is None or rank == 'Unrated':
            continue
        elif rank == -1:
            return -1
        elif rank == -2:
            return -2
        else:
            return {'rank':rank,'season':season}

def get_rr(puuid:str):
    url = f"https://api.henrikdev.xyz/valorant/v1/by-puuid/mmr/eu/{puuid}"
    headers = {
        "Accept": "application/json"
    }
    urls_expire_after = {
        url: -1,
    }
    session = CachedSession('session_rr', urls_expire_after=urls_expire_after, cache_control='no-cache')

    response = session.get(url, headers=headers)
    if response.json()['status'] == 200:
        return response.json()['data']['ranking_in_tier']
    elif response.json()['status'] == 429:
        return -2


def get_level(username:str,tag:str):
    return fetch_user(username,tag)['data']['account_level']

