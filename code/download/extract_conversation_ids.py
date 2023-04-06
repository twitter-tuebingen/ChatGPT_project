# -*- coding: utf-8 -*-
'''Get conversation IDs from downloaded hashtag json files'''

import json
from tqdm import tqdm
import os

path='C:/TwitterChatGPTProject/data/'
files = os.listdir(path)
files
conv_ids = []

for file in tqdm(files):
    with open(path+file, 'r',encoding="utf-8") as f:
        temp = json.load(f)
        conv_ids.extend(d["conversation_id"] for d in temp['data'])

n_tweets = len(conv_ids)
len(set(conv_ids))

from collections import Counter
freq=Counter(conv_ids)
freq.most_common(10)

with open(path+"conv_ids.txt", 'w') as f:
    for cid in res:
        f.write(f'{cid}\n')