# -*- coding: utf-8 -*-
'''Get conversation IDs from downloaded hashtag json files'''

#import glob
import json
from tqdm import tqdm
import os

# read all hashtag json files
#files = glob.glob('C:/TwitterChatGPTProject/data/') # ignores .gitkeep
path='C:/TwitterChatGPTProject/data/'
files = os.listdir(path)
files
conv_ids = []

# check if tweet sparked a conversation (has replies)
for file in tqdm(files):
    with open(path+file, 'r',encoding="utf-8") as f:
        temp = json.load(f)
        conv_ids.extend(d["conversation_id"] for d in temp['data'])
        
       # res |= {(d['conversation_id']) for d in temp['data'] if d['public_metrics']['reply_count'] > 0}

n_tweets = len(conv_ids)
len(set(conv_ids))

from collections import Counter
freq=Counter(conv_ids)
freq.most_common(10)

# write conversation ids to file
# DG: TODO Shouldn't the results be placed in the 0-Data folder?
with open(path+"conv_ids.txt", 'w') as f:
    for cid in res:
        f.write(f'{cid}\n')