import time
import json
import requests

path = "C:/Users/aAlekseeva/Documents/" # put the path to the bearer token

with open(path+"token.txt", "r") as f:
    for line in f:
        BEARER_TOKEN = line.strip()

DATA_FOLDER = 'C:/TwitterChatGPTProject/data/geo/'

PLACE_IDS = []
with open('../data/place_ids.txt', 'r') as f:
    for line in f:
        PLACE_IDS.append(line.strip())

for num,place_id in enumerate(PLACE_IDS):
    time.sleep(12)
    print(f'Downloading {num}...')

    session = requests.Session()
    session.headers.update({'Authorization': f'Bearer {BEARER_TOKEN}'})
    URL = f"https://api.twitter.com/1.1/geo/id/"
    req = requests.models.PreparedRequest()
    r = session.get(URL+str(place_id)+".json")
    if not r.ok:
        last_download_failed = True
        with open('download_log.txt', 'a') as f:
            f.write(f'Download failed for {num} -- status not ok\n')
            continue
    json_loaded = json.loads(r.content)
    with open(f'{DATA_FOLDER}/place_id_{num}.json', 'w',encoding="utf-8") as f:
        json.dump(json_loaded, f, ensure_ascii=False)
