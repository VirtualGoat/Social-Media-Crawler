# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 12:25:37 2019

@author: Parth
"""
import os
import collections
from collections import Counter
import pickle 
import string
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from math import ceil
import tweepy

url_list=list()
username_list=list()
user_profile_list=list()
stored_tweets=list()
consumer_key='rNrnFupaEqKt0eb7hjbdHKdWg'
consumer_secret= 'DTTMoQOrCBmngaXmOnFhrBjdjwtT54x0AbGvNwwuqyYNWwEvc7'
access_token='1002268050513575936-gGrQUmDiMyCxO2Y88lc3ojqNzbtLGm'
access_token_secret='G572YTe2S5TQTTaXhFvl1WyNopa8ilrkgWSlCXBZQwU4C'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

def create_project_directory(directory):
    if not os.path.exists(directory):
        print("Creating a new Directory...")
        os.makedirs(directory)

def write_data(stored_tweets,filename):
    tweet_pickle=open(filename,'wb')
    pickle.dump(stored_tweets,tweet_pickle)
    tweet_pickle.close()


def get_tweet_id(tweets):
    tweet_ids=[]
    for i in tweets:
        tweet_ids.append(i.id)
    return tweet_ids

def get_indi_url_data(obj):
    url='https://twitter.com/'
    url+=obj.user.screen_name+'/status/'+str(obj.id)
    return url

def get_url_data(tweets):
    user_profile_list=[]
    up_url='https://twitter.com/'
    username_list=[]
    url_list=[]
    url='https://twitter.com/'


    #Only stores the usernames that don't have hiranandani in them. 
    for i in tweets:
        url1=url
        up_url1=up_url
        if 'hiranandani' not in (i.user.screen_name).lower():
            url1+=i.user.screen_name+'/status/'
            url1+=str(i.id)
            up_url1+=i.user.screen_name
            url_list.append(url1)
            username_list.append(i.user.screen_name)
            user_profile_list.append(up_url1)
            
    return url_list, username_list,user_profile_list



def flatten(x):
    result = []
    for el in x:
        if hasattr(el, "__iter__") and not isinstance(el, str):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result


def get_authorization():

    info = {"consumer_key": "rNrnFupaEqKt0eb7hjbdHKdWg",
            "consumer_secret": "DTTMoQOrCBmngaXmOnFhrBjdjwtT54x0AbGvNwwuqyYNWwEvc7",
            "access_token": "1002268050513575936-gGrQUmDiMyCxO2Y88lc3ojqNzbtLGm",
            "access_secret": "G572YTe2S5TQTTaXhFvl1WyNopa8ilrkgWSlCXBZQwU4C"}

    auth = tweepy.OAuthHandler(info['consumer_key'], info['consumer_secret'])
    auth.set_access_token(info['access_token'], info['access_secret'])
    return auth

'''
def get_tweets(query, n):
    _max_queries = 100  # arbitrarily chosen value
    api = tweepy.API(get_authorization(),wait_on_rate_limit=True)
    tweets = tweet_batch = api.search(q=query, count=n)
    ct = 1
    while len(tweets) < n and ct < _max_queries:
        print(len(tweets))
        tweet_batch = api.search(q=query, 
                                 count=n - len(tweets),
                                 max_id=tweet_batch.max_id)
        tweet_batch1=list()
        
        for i in tweet_batch:
            if i.id not in tweet_ids:
                tweet_batch1.append(i)    
        tweets.extend(tweet_batch1)
        ct += 1
    return tweets
'''
def pull_tweets(query):
    max_tweets=10000

    searched_tweets = []
    last_id = -1
    while len(searched_tweets) < max_tweets:
        count = max_tweets - len(searched_tweets)
        try:
            new_tweets = api.search(q=query, count=count, max_id=str(last_id - 1))
            if not new_tweets:
                break
            for i in new_tweets:
                url=get_indi_url_data(i)
                if url not in url_list:
                    #searched_tweets.extend(new_tweets)
                    searched_tweets.append(i)
                    last_id = new_tweets[-1].id
        except tweepy.TweepError as e:
                        # depending on TweepError.code, one may want to retry or wait
        # to keep things simple, we will give up on an error
            break

    return searched_tweets

#analytics
def analytics(stored_tweets):
    neut=0
    pos=0
    neg=0
    negative=list()
    

    
    for i in stored_tweets:
        blob=TextBlob(str(i.text))
        if blob.polarity<0:
            neg+=1
            negative.append(i)
        elif blob.polarity>0:
            pos+=1
        else:
            neut+=1
    negp=(neg/len(stored_tweets))*100
    neutp=(neut/len(stored_tweets))*100
    posp=(pos/len(stored_tweets))*100

    labels = 'Positive',"Negative","Neutral"
    sizes = [posp,negp,neutp]
    m=max(posp,negp,neutp)
    if m==posp:
        explode=(0.1,0,0)
    elif m==negp:
        explode = (0, 0.1, 0)
    else:
        explode= (0, 0, 0.1)
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()

    return negative
#wordcloud


def wordcloud(negative):
    hello=[]
    stop_words = set(stopwords.words('english')) 
    text_tweets=list()
    for i in negative:
        if 'hiranandani' not in (i.user.screen_name).lower():
            st=i.text    
            word_tokens = word_tokenize(st)
            filtered_sentence = []   
            removetable = str.maketrans('', '', '@#%')
            out_list = [s.translate(removetable) for s in word_tokens]
            for w in out_list: 
                if w not in stop_words: 
                    filtered_sentence.append(w) 
            x = [''.join(c for c in s if c not in string.punctuation) for s in filtered_sentence]
            x = [s for s in x if s]
            text_tweets.append(x)
    
    for i in text_tweets:
        if 'RT' in i:
            i.remove('RT')
    
    username_set=set(username_list)
    
    for j in text_tweets:
        l3 = [x for x in j if x not in username_set]
        hello.append(l3)    
            
    flat_tweets=list(flatten(hello))
    
    for i in flat_tweets:
        if i.isalpha()==False:
            flat_tweets.remove(i)
    
    counter=collections.Counter(flat_tweets)
     
    for word in list(counter):
        if str(word).isalpha()==False:
            del counter[word]
            
    c1=counter.most_common()
    return c1





#tweets_id=list()




#tweet=get_tweets('Hiranandani',100000)



'''
# assuming twitter_authentication.py contains each of the 4 oauth elements (1 per line)
#from twitter_authentication import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

auth = tweepy.OAuthHandler('rNrnFupaEqKt0eb7hjbdHKdWg', 'DTTMoQOrCBmngaXmOnFhrBjdjwtT54x0AbGvNwwuqyYNWwEvc7')
auth.set_access_token('1002268050513575936-gGrQUmDiMyCxO2Y88lc3ojqNzbtLGm', 'G572YTe2S5TQTTaXhFvl1WyNopa8ilrkgWSlCXBZQwU4C')

api = tweepy.API(auth)

query = 'hiranandani'
max_tweets = 100000
searched_tweets = [status for status in tweepy.Cursor(api.search, q=query).items(max_tweets)]

'''


'''
#retweeters
replies=[] 
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)  
for full_tweets in tweepy.Cursor(api.user_timeline,screen_name='brfootball',timeout=999999).items(10):
  for tweet in tweepy.Cursor(api.search,q='to:'+'brfootball',result_type='recent',timeout=999999).items(1000):
    if hasattr(tweet, 'in_reply_to_status_id_str'):
      if (tweet.in_reply_to_status_id_str==full_tweets.id_str):
        replies.append(tweet.text)
  print("Tweet :",full_tweets.text.translate(non_bmp_map))
  for elements in replies:
       print("Replies :",elements)
  replies.clear()


igsjc_tweets_jan = [tweet for tweet in tweepy.Cursor(
                    api.search, q="Hiranandani", since='2019-08-01', until='2019-09-30').items(3000)]


    
igsjc_tweets_jan = [tweet for tweet in tweepy.Cursor(api.search,
                           q="Hiranandani",
                           count=1000,
                           result_type="recent",
                           include_entities=True,
                           lang="en").items()]

igsjc_tweets_jan = api.search('Hiranandani',count=1000)
'''



'''
url_list1, username_list1,user_profile_list1=get_url_data(searched_tweets)
user_profile_list.append(user_profile_list1)

counter=collections.Counter(username_list)

df=pd.read_csv('Profiles.csv')
urls=list(df['Profile'])

for i in user_profile_list:
    if i not in urls:
        urls.extend(i)


d={'Profile':pd.Series(urls)}

finaldata=pd.DataFrame(d)
finaldata.to_csv("Profiles.csv",index=False,encoding='UTF-8')
'''



