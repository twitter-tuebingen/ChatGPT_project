"""Download tweets by tweet id"""

import time
import json
import requests
import pandas as pd


path = "C:/Users/aAlekseeva/Documents/" # put the path to the bearer token

with open(path+"token.txt", "r") as f:
    for line in f:
        BEARER_TOKEN = line.strip()


DATA_FOLDER = 'C:/TwitterChatGPTProject/data/missing_tweets/'

# Download stored tweet ids from txt file and split them into batches
TWEET_IDS = []
tweet_batch=[]
batch_size=100
count=0
with open("data/missing_retweets.txt","r") as f:
    for line in f:
        tweet_batch.append(line.strip())
        count+=1
        if count==batch_size:    
            TWEET_IDS.append(tweet_batch)
            count=0
            tweet_batch=[]
if tweet_batch:            
    TWEET_IDS.append(tweet_batch)

# Twitter API 2.1 query parameters
PARAMS = {
'tweet.fields': "attachments,author_id,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,reply_settings,source,text,withheld",
'expansions': "attachments.poll_ids,attachments.media_keys,author_id,geo.place_id,in_reply_to_user_id,referenced_tweets.id,entities.mentions.username,referenced_tweets.id.author_id",
'media.fields': "duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics,alt_text",
'place.fields': "contained_within,country,country_code,full_name,geo,id,name,place_type",
'poll.fields': "duration_minutes,end_datetime,id,options,voting_status",
'user.fields': "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld",
}

for num,tw_id_batch in enumerate(TWEET_IDS):

    time.sleep(3)
    print(f'Downloading {num}...')
    PARAMS['ids'] = ",".join(tw_id_batch)

    session = requests.Session()
    session.headers.update({'Authorization': f'Bearer {BEARER_TOKEN}'})
    URL = f"https://api.twitter.com/2/tweets"
    req = requests.models.PreparedRequest()
    req.prepare_url(URL, PARAMS)
    r = session.get(req.url)
    if not r.ok:
        last_download_failed = True
        with open('download_log.txt', 'a') as f:
            f.write(f'Download failed for {num} -- status not ok\n')
            continue
    json_loaded = json.loads(r.content)
    data = json_loaded["data"]

    with open(f'{DATA_FOLDER}/tweets_{num}.json', 'w',encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


