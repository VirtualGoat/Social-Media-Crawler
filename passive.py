# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 14:15:51 2019

@author: Parth
"""
import urllib
import re
import io
import re
import sys
from time import sleep
import pickle
import os
from math import ceil
import active
import tweepy
consumer_key='rNrnFupaEqKt0eb7hjbdHKdWg'
consumer_secret= 'DTTMoQOrCBmngaXmOnFhrBjdjwtT54x0AbGvNwwuqyYNWwEvc7'
access_token='1002268050513575936-gGrQUmDiMyCxO2Y88lc3ojqNzbtLGm'
access_token_secret='G572YTe2S5TQTTaXhFvl1WyNopa8ilrkgWSlCXBZQwU4C'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)



'''
for i in reply:
    print(i.in_reply_to_status_id)
    url2=url1
    url2+=i.user.screen_name+'/status/'+str(i.id)
    print(url2)
'''

#creating a separate folder for  each tweet
query='Hiranandani'
profile_file=query+'/Profiles.csv'
status_file=query+'/status.csv'
tweets_file=query+'/tweets.pickle'

#Opening the file containing previously stored tweets
try:
    h=open(tweets_file,'rb')
except:
    print("Run the initial code first.")

tweets=pickle.load(h)

status_and_replies=dict()


def get_user_ids_of_post_likes(post_id):
    try:
        json_data = urllib.request.urlopen('https://twitter.com/i/activity/favorited_popup?id=' + str(post_id)).read()
        json_data = json_data.decode('utf-8')
        found_ids = re.findall(r'data-user-id=\\"+\d+', json_data)
        unique_ids = list(set([re.findall(r'\d+', match)[0] for match in found_ids]))
        return unique_ids

    except urllib.request.HTTPError:
        return False

likers=list()
for i in tweets: 
    id1=get_user_ids_of_post_likes(i.id)
    likers.extend(id1)


url1='https://twitter.com/'
try: 
    for j in tweets:
        sleep(3)
        reply=api.search(q=j.user.screen_name,since_id=j.id,count=10000)
        print("For User: ",j.user.screen_name)
        url3=url1
        url3+=j.user.screen_name+'/status/'+str(j.id) 
        li=list()
        for i in reply:
            if i.in_reply_to_status_id==j.id:
                url2=url1
                url2+=i.user.screen_name+'/status/'+str(i.id)
                
                li.append(url2)                
                print(url2)
            print("\n\n")
        status_and_replies[url3]=li
except Exception as e:
    print(e)




