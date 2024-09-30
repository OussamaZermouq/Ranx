from requests_cache import CachedSession
from dotenv import load_dotenv
import os
from datetime import timedelta

load_dotenv()
token = os.getenv('API_KEY')

def fetch_user(username:str, tag:str):
    url = f'https://api.henrikdev.xyz/valorant/v1/account/{username}/{tag}?force=false'
    headers = {
        "Accept": "application/json",
        "Authorization":f'{token}'
    }
    urls_expire_after = {
        url: -1,
    }
    session = CachedSession('session', expire_after=timedelta(days=1), cache_control='no-cache')
    response = session.get(url, headers=headers)
    if response.status_code!=200:
        print("PLAYER NOT FOUND")
        return -1
    else:
        return response.json()


def get_puuid(username:str, tag:str):
    data = fetch_user(username=username, tag=tag)
    if data['status'] == 200:
        puuid = data['data']['puuid']
        return puuid
    return data



#TODO:if a new season or act is live, add it here.
seasons = ['e1a1','e1a2','e1a3','e2a1','e2a2','e2a3','e3a1','e3a2','e3a3',
           'e4a1','e4a2','e4a3','e5a1','e5a2','e5a3','e6a1','e6a2','e6a3',
           'e7a1','e7a2','e7a3','e8a1','e8a2','e8a3','e9a1','e9a2']

def fetch_last_MMR_registered(puuid:str):
    url = f'https://api.henrikdev.xyz/valorant/v2/by-puuid/mmr/eu/{puuid}'

    headers = {
        "Accept": "application/json",
        "Authorization":f'{token}'
    }
    output = {}
    error = {'error': 'No data available'}
    session = CachedSession('session_ranks', expire_after=timedelta(days=1), cache_control='no-cache')
    response = session.get(url, headers=headers)
    if response.status_code!=200:
        return -1
    elif response.json()['status'] == 429:
        return -2
    else:
        data = response.json()['data']
        by_season = data['by_season']
        for season in reversed(seasons):
            if by_season[season] != error:
                last_registered_rank = by_season[season]
                output = {'rank':last_registered_rank['final_rank_patched'], 'act':season, 'old': 'true' if season != seasons[-1] else 'false'}
                break
        return output 


print(fetch_last_MMR_registered(get_puuid('Memphré','0001')))


# def return_last_filled_rank(puuid:str):
#     for season in reversed(seasons):
#         rank = fetch_current_rank(puuid = puuid, episode = season)
#         print(rank)
#         if rank is None or rank == 'Unrated':
#             continue
#         elif rank == -1:
#             return -1
#         elif rank == -2:
#             return -2
#         else:
#             return {'rank':rank,'season':season}

def get_rr(puuid:str):
    url = f"https://api.henrikdev.xyz/valorant/v1/by-puuid/mmr/eu/{puuid}"
    headers = {
        "Accept": "application/json",
        "Authorization":f'{token}'
    }
    urls_expire_after = {
        url: -1,
    }
    session = CachedSession('session_rr', expire_after=timedelta(days=1), cache_control='no-cache')

    response = session.get(url, headers=headers)
    if response.json()['status'] == 200:
        print(response.json()['data']['ranking_in_tier'])
        return response.json()['data']['ranking_in_tier']
    elif response.json()['status'] == 429:
        return -2


def get_level(username:str,tag:str):
    return fetch_user(username,tag)['data']['account_level']