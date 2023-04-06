# ChatGPT_project

## About

This repository documents the extraction and analysis of Twitter data on ChatGPT in the period of 30 Nov 2022 - 31 Jan 2023. 

Please contact anastasiia.alekseeva@student.uni-tuebingen.de for more information about this repository, or just leave a pull request.

## Download

This folder contains Python scripts to extract data from Twitter by using official Twitter API. Each file corresponds to the request to specific REST endpoints and parameters:

- api_keyword_download.py: searches and downloads all historical tweets that mention "chatgpt" (case insensitive) from 01-01-2022 to 31-01-2023.

- api_conv_download.py: searches and downloads all tweets by conversation id from 30-11-2022 to 31-01-2023. The conversation id is collected by using extract_conversation_ids.py.

- api_tweet_download.py: downloads tweets by their id. This request is necessary to collect full-text tweets that were retweeted and appeared in the dataset.

- api_user_download.py: download user information by user id as a part of bot detection procedure.

- api_geolocation_download.py: download information about place id, is necessary to get country names of the tweets with known geolocation.

To access the endpoints we used the Twitter API for Academic Research and the corresponding bearer token that was stored in a token.txt file.


## Data Preparation

This folder documents the pre-processing of downloaded tweets.

1. The collected json files were parsed into individual files.

2. The datasets for tweets and conversation tweets were concatenated into one dataset (data0).

3. Identified bot accounts were deleted from data0. 

4. data0 was anonymized to ensure that no data can be traced back to individuals through working with the data set. All user and tweets IDs are consistently substituted with a unique ID. E-mail addresses and phone numbers are substituted with placeholders (e.g., '<email>',<phone>). All user mentions in tweet are substituted with a pseudo-name (i.e. @anon1, @anon2').

## Analysis

This folder documents exploratory analysis of the data, sentiment analysis and topic modeling of the collected tweets, and the corresponding pre-processing.


