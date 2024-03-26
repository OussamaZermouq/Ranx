import json

def load_json():
    with open('./accounts.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def check_user_exist(username, tag):
    accounts_json = load_json()

    for account in accounts_json['accounts']:
        if (account['username'] == username) and (account['tag']==tag):
            return -1
    return 0

def write_to_json(username:str, tag:str, login:str, password:str):
    
    accounts_json = load_json()
    previous_id = len(accounts_json['accounts'])
    
    if check_user_exist(username=username, tag=tag)!=-1:
        new_account = {
            'id':previous_id,
            'username':username,
            'tag':tag,
            'login':login,
            'password':password,
        }    
        #in this function we get the account.json['accounts'] and we add new info to it
        #we then dump the new data in the old file which is in the accounts_json variable
        accounts_json['accounts'].append(new_account)
        
        with open('./accounts.json', 'w', encoding='utf-8') as file:
            json.dump(accounts_json, file)
        return 0
    else:
        return -1

