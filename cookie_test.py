import requests
import urllib3

url = "https://auth.riotgames.com/api/v1/authorization"
session = requests.Session()
username = 'Notsmerfing2021'
password = 'P@Sword123789'

headers = {
'Content-Type':'application/json'
}

data = {
    "client_id": "play-valorant-web-prod",
    "nonce": "1",
    "redirect_uri": "https://playvalorant.com/opt_in",
    "response_type": "token id_token",
    'scope': 'account openid',
}


# headers = {'Content-Type': 'application/json', 'User-Agent': self.user_agent}
r = session.post('https://auth.riotgames.com/api/v1/authorization', json=data, headers=headers)
cookies = {'cookie': {}}
for cookie in r.cookies.items():
    cookies['cookie'][cookie[0]] = str(cookie).split('=')[1].split(';')[0]

urllib3.disable_warnings()
session = session.put(url, data=data, headers=headers, verify=False)

with session.put('https://auth.riotgames.com/api/v1/authorization', json=data, headers=headers) as r:
    data = r.json()
    for cookie in r.cookies.items():
        cookies['cookie'][cookie[0]] = str(cookie).split('=')[1].split(';')[0]



print(r.cookies.items())