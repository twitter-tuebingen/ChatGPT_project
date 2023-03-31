"""Download information about twitter accounts by their author ids"""

import time
import json
import requests
import pandas as pd

path = "C:/Users/aAlekseeva/Documents/" # put the path to the bearer token

with open(path+"token.txt", "r") as f:
    for line in f:
        BEARER_TOKEN = line.strip()

DATA_FOLDER = 'C:/TwitterChatGPTProject/data/potential_bots/'
AUTHOR_IDS = []

# Download stored user/author ids from txt file and split them into batches
batch=[]
batch_size=100
count=0
with open("data/potential_bots.txt","r") as f:
    for line in f:
        batch.append(line.strip())
        count+=1
        if count==batch_size:    
            AUTHOR_IDS.append(batch)
            count=0
            batch=[]
if batch:            
    AUTHOR_IDS.append(batch)


for num, author_id_batch in enumerate(AUTHOR_IDS):
    time.sleep(1)
    print(f'Downloading {num}...')
    PARAMS={}
    PARAMS['user_id'] = ",".join(author_id_batch)

    session = requests.Session()
    session.headers.update({'Authorization': f'Bearer {BEARER_TOKEN}'})
    URL = f"https://api.twitter.com/1.1/users/lookup.json?user_id="
    req = requests.models.PreparedRequest()
    req.prepare_url(URL, PARAMS)
    r = session.get(req.url)
    if not r.ok:
        last_download_failed = True
        with open('download_log.txt', 'a') as f:
            f.write(f'Download failed for {num} -- status not ok\n')
            continue
    json_loaded = json.loads(r.content)

    with open(f'{DATA_FOLDER}/userinfo_{num}.json', 'w',encoding="utf-8") as f:
        json.dump(json_loaded, f, ensure_ascii=False)