"""Download all tweets by a keyword/hashtag"""

import time
import json
import requests

path = "C:/Users/aAlekseeva/Documents/" 

with open(path+"token.txt", "r") as f:
    for line in f:
        BEARER_TOKEN = line.strip()

DATA_FOLDER = 'C:/TwitterChatGPTProject/data/16_hashtags/'
HASHTAGS = ['chatgpt']
#HASHTAGS = ['#aussieED', '#UKEdChat','#caedchat','#miched','#sschat',
#            '#NGSSchat','#TLAP', '#KidsDeserveIt','#HipHopEd', '#EduColor',
#            '#satchat', '#BFC530','#edtechchat', '#whatisschool', '#globaledchat', 
#            '#collaborativePD']

# Twitter API 2.1 query parameters
PARAMS = {
'max_results': "500",
'start_time': "2022-01-01T00:00:00Z", # (YYYY-MM-DDTHH:mm:ssZ) -> RFC3339 date-time
'end_time': "2023-01-31T23:59:59Z", # (YYYY-MM-DDTHH:mm:ssZ)
'tweet.fields': "attachments,author_id,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,reply_settings,source,text,withheld",
'expansions': "attachments.poll_ids,attachments.media_keys,author_id,geo.place_id,in_reply_to_user_id,referenced_tweets.id,entities.mentions.username,referenced_tweets.id.author_id",
'media.fields': "duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics,alt_text",
'place.fields': "contained_within,country,country_code,full_name,geo,id,name,place_type",
'poll.fields': "duration_minutes,end_datetime,id,options,voting_status",
'user.fields': "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld",
}

for hashtag in HASHTAGS:
    print(f'Downloading {hashtag}...')
    count = 0
    PARAMS['query'] = hashtag
    last_download_failed = False
    try:
        del PARAMS['next_token']
    except KeyError:
        pass
    # API pagination
    while 'next_token' in PARAMS or count == 0 or last_download_failed:
        time.sleep(3)
        try:
            print(f'Downloading {hashtag} with next token {PARAMS["next_token"]}...')
        except KeyError:
            pass
        session = requests.Session()
        session.headers.update({'Authorization': f'Bearer {BEARER_TOKEN}'})
        URL = f"https://api.twitter.com/2/tweets/search/all"
        req = requests.models.PreparedRequest()
        req.prepare_url(URL, PARAMS)
        r = session.get(req.url)
        if not r.ok:
            last_download_failed = True
            with open('download_log.txt', 'a') as f:
                f.write(f'Download failed for {hashtag} -- status not ok\n')
                continue
        try:
            json_loaded = json.loads(r.content)
        except:
            last_download_failed = True
            with open('download_log.txt', 'a') as f:
                f.write(f'Download failed for {hashtag} -- JSON content not correctly loaded\n')
                continue
        try:
            PARAMS['next_token'] = j['meta']['next_token']
        except KeyError:
            try:
                if not last_download_failed:
                    del PARAMS['next_token']
            except KeyError:
                pass
        if not last_download_failed:
            count += 1
        try:
            if not j['meta']['result_count'] == 0:
                with open(f'{DATA_FOLDER}/{hashtag}_{count}.json', 'w',encoding="utf-8") as f:
                    json.dump(json_loaded, f, ensure_ascii=False)
                last_download_failed = False
        except:
            last_download_failed = True
            with open('C:/TwitterChatGPTProject/logs/download_log.txt', 'a') as f:
                f.write(f'Download failed for {hashtag} -- JSON export failed\n')
                continue
