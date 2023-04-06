"""
Download conversations from conversation IDs in conv_ids.txt
Run hashtag_download.py and extract_conversation_ids.py first

Parse:
1 token file path
2 conv ID file path line by line file (xaa, xab, xac)
"""

import time
import json
import sys
import requests
# 1. token file path
file_path = "C:/Users/aAlekseeva/Documents/" 

with open(file_path+'token.txt', "r") as f:
    for line in f:
        BEARER_TOKEN = line.strip()

# The folder where json files of downloaded conersations will be stored
DATA_FOLDER = '../data/conv_ids/'

# 2. Read conversation ids
CONV_IDS = []
with open('../data/conv_ids.txt', 'r') as f:
    for line in f:
        CONV_IDS.append(line.strip())


PARAMS = {
'max_results': "100",  # max for conversations
'start_time': "2022-11-30T00:00:00Z", # (YYYY-MM-DDTHH:mm:ssZ) -> RFC3339 date-time
'end_time': "2023-01-15T23:59:59Z", # (YYYY-MM-DDTHH:mm:ssZ)
'tweet.fields': "attachments,author_id,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,reply_settings,source,text,withheld",
'expansions': "attachments.poll_ids,attachments.media_keys,author_id,geo.place_id,in_reply_to_user_id,referenced_tweets.id,entities.mentions.username,referenced_tweets.id.author_id",
'media.fields': "duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics,alt_text",
'place.fields': "contained_within,country,country_code,full_name,geo,id,name,place_type",
'poll.fields': "duration_minutes,end_datetime,id,options,voting_status",
'user.fields': "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld",
}


for conv_id in CONV_IDS:
    time.sleep(3)
    print(f'Downloading conv. {conv_id}...')
    count = 0
    PARAMS['query'] = f"conversation_id:{conv_id}"
    try:
        del PARAMS['next_token']
    except KeyError:
        pass
    while ('next_token' in PARAMS) or (count == 0):
        try:
            print(f'Downloading conv. {conv_id} with next token {PARAMS["next_token"]}...')
        except KeyError:
            pass
        session = requests.Session()
        session.headers.update({'Authorization': f'Bearer {BEARER_TOKEN}'})
        URL = f"https://api.twitter.com/2/tweets/search/all"
        req = requests.models.PreparedRequest()
        req.prepare_url(URL, PARAMS)
        r = session.get(req.url)
        if not r.ok:
            with open('download_log.txt', 'a') as f:
                f.write(f'Download failed for conv. {conv_id} -- status not ok\n')
                break
        try:
            json_loaded = json.loads(r.content)
        except:
            with open('download_log.txt', 'a') as f:
                f.write(f'Download failed for conv. {conv_id} -- JSON content not correctly loaded\n')
                break
        try:
            PARAMS['next_token'] = json_loaded['meta']['next_token']
        except KeyError:
            try:
                del PARAMS['next_token']
            except KeyError:
                pass
        count += 1
        try:
            if not json_loaded['meta']['result_count'] == 0:
                with open(f'{DATA_FOLDER}/{conv_id}_{count}.json', 'w',encoding="utf-8") as f:
                    json.dump(json_loaded, f, ensure_ascii=False)
        except:
            with open('download_log.txt', 'a') as f:
                f.write(f'Download failed for conv. {conv_id} -- JSON export failed\n')
                break

    with open("../data/conv_ids_used.txt","a") as f:
        f.write(conv_id+"\n")


