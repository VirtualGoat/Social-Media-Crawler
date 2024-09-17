# =============================================================================
# # -*- coding: utf-8 -*-
# """
# Created on Fri Dec 20 17:48:46 2019
# 
# @author: Parth
# """
# import concurrent.futures 
# import pickle
# import re
# import smtplib
# import dns.resolver
# import time
# import psycopg2
# start_time = time.time()
# 
# '''
# print("Connecting to database")
# try:     
#     conn = psycopg2.connect(database='Hiranandani', user = "postgres", password = "parth123n@#*", host = "127.0.0.1", port = "5432")    
# except:
#     print("Create database first")
# 
# mycursor=conn.cursor()
# 
# table='emails'
# '''
# def verify(emails):
#     valid_emails=list()
#     for inputAddress in emails:
#         try:
#             fromAddress= 'abc@gmail.com'
#             regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
#              
#             addressToVerify= str(inputAddress)
#              
#             match=re.match(regex,addressToVerify)
#              
#             if match==None:
#                 print('Bad syntax')
#                 raise ValueError("Bad syntax")
#                  
#             splitAddress= addressToVerify.split('@')
#             domain=str(splitAddress[1])
#             
#             records= dns.resolver.query(domain,'MX')
#             mxRecord= records[0].exchange
#             mxRecord= str(mxRecord)
#              
#             server=smtplib.SMTP()
#             server.set_debuglevel(0)
#             
#             server.connect(mxRecord)
#             server.helo(server.local_hostname)
#             server.mail(fromAddress)
#             code,message =server.rcpt(str(addressToVerify))
#             server.quit()
#             
#             if code==250:
#                 valid_emails.append(inputAddress)
#                 print(inputAddress)
#                 print("Success")
#                 #sql = "INSERT INTO 'emails' (valid) VALUES (%s)"
#                 #val = (str(addressToVerify))
#                 #mycursor.execute(sql, val)
#                 #conn.commit()
#             else:
#                 print("Bad")
#         except Exception as e:
#             print(e)
#            # return valid_emails
# 
# with open('emails.pickle', 'rb') as f:
#     emails = pickle.load(f)
# 
# Verifying list of emails
# emails=['nagarkarparth69123@hotmail.com',"nagarkarparth2201@yahoo.com","nagarkarparth@yahoo.co.in","kala69iyer@gmail.com","nagarkarparth@yahoo.com","harsha_nihar@yahoo.co.in"]
# verify(emails)
# print("--- %s seconds ---" % (time.time() - start_time))
# 
# 
# #conn.close()
# '''
# with concurrent.futures.ThreadPoolExecutor(4) as executor:
#     future = executor.submit(verify, emails[:12])
#     return_value = future.result()
# '''
# =============================================================================
# =============================================================================
# import tweepy
# 
# consumer_key=''
# consumer_secret= ''
# access_token=''
# access_token_secret=''
# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)
# 
# api = tweepy.API(auth,wait_on_rate_limit=True)
# 
# 
# 
# u=api.get_user('Flatstreet1')
# print(u.url)
# 
# import requests
# 
# site = requests.get(u.url)
# print(site.url)
# 
# =============================================================================


# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'ACc76ec8846f23aa30432e36936c514ebf'
auth_token = '7205e6034e384bc1e7f8c324affb1771'
client = Client(account_sid, auth_token)

phone_number = client.lookups \
                     .phone_numbers('+919930426913') \
                     .fetch(type=['caller-name'])

print(phone_number.caller_name)


