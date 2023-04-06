import pandas as pd
import os
import json

path='../data/keyword_search_2/'
files = os.listdir(path)

count=0
for file in files:
    with open(path+file, 'r',encoding="utf-8") as f:
        temp = json.load(f)
        if count==0:
            conv = pd.json_normalize(temp["data"])
            count+=1
        else:
            df = pd.json_normalize(temp["data"])
            conv = pd.concat([conv,df],axis=0)
conv = conv.reset_index(drop=True)
conv.to_json("../data/for_analysis/data_31jan_data.json")