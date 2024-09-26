import string
import time
import threading
import urllib
import re
import io
import sys
from time import sleep
import pickle
import pandas as pd
import psycopg2



def formats(first, middle, last, domain):
    """
    Create a list of 30 possible email formats combining:
    - First name:          [empty] | Full | Initial |
    - Delimeter:           [empty] |   .  |    _    |    -
    - Last name:           [empty] | Full | Initial |
    """
    list = []
    #Email IDs
    if len(last)==0:
        list.append(first + '@' + domain)                    # first@example.com


    else:
        list.append(first[0] + last + '@' + domain)          # flast@example.com
        list.append(first[0] + '.' + last + '@' + domain)    # f.last@example.com
        list.append(first[0] + '_' + last + '@' + domain)    # f_last@example.com
        list.append(first + '@' + domain)                    # first@example.com
        list.append(first + last + '@' + domain)             # firstlast@example.com
        list.append(first + '.' + last + '@' + domain)       # first.last@example.com
        list.append(first + '_' + last + '@' + domain)       # first_last@example.com
        list.append(first + '-' + last + '@' + domain)       # first-last@example.com

        list.append(first + last[0] + '@' + domain)          # fistl@example.com
        list.append(first + '.' + last[0] + '@' + domain)    # first.l@example.com
        list.append(first + '_' + last[0] + '@' + domain)    # fist_l@example.com
        
        list.append(first[0] + middle + last + '@' + domain)          # fmiddlelast@example.com
        list.append(first[0] + '.' + middle + last + '@' + domain)    # f.middlelast@example.com
        list.append(first[0] + middle + '.' + last + '@' + domain)    # fmiddle.last@example.com
        list.append(first[0] + '_' + middle+ last + '@' + domain)    # f_middlelast@example.com
        list.append(first[0] + middle +'_' + last + '@' + domain)    # fmiddle_last@example.com
        list.append(first + middle+ last + '@' + domain)             # firstmiddlelast@example.com
        list.append(first + middle + '.' + last + '@' + domain)       # firstmiddle.last@example.com
        list.append(first + '.' + middle + last + '@' + domain)       # first.middlelast@example.com
        list.append(first + '_' + middle + last + '@' + domain)       # first_last@example.com
        list.append(first + middle + '_' + last + '@' + domain)       # first_last@example.com
        list.append(first + middle+ last[0] + '@' + domain)          # firstmiddlel@example.com
        list.append(first + '.' + middle +last[0] + '@' + domain)    # first.middlel@example.com
        list.append(first + middle + '.' +last[0] + '@' + domain)    # firstmiddle.l@example.com
        list.append(first + '_' + middle +last[0] + '@' + domain)    # first_middlel@example.com
        list.append(first + middle +'_' + last[0] + '@' + domain)    # firstmiddle_l@example.com        
       
        list.append(last + '@' + domain)                     # last@example.com
        list.append(last + first+ '@' + domain)              # lastfirst@example.com
        list.append(last + '.' + first + '@' + domain)       # last.first@example.com
        list.append(last + '_' + first + '@' + domain)       # last_first@example.com
        list.append(last[0] + '.' + first + '@' + domain)    # l.first@example.com    
        list.append(last[0] + first + '@' + domain)          # lfirst@example.com
        list.append(last + first[0] + '@' + domain)          # lastf@example.com
        list.append(last + '.' + first[0] + '@' + domain)    # last.f@example.com
        list.append(last + '_' + first[0] + '@' + domain)    # last_f@example.com
       
    return(list)


val="select distinct name from keywords"

try:     
    conn = psycopg2.connect(database='Hiranandani', user = "postgres", password = "parth123n@#*", host = "127.0.0.1", port = "5432")    
except:
    print("Create database first")


df=pd.read_sql(val,conn)

uname=list()
for i in df['name']:
    uname.append(i.translate(str.maketrans('', '', string.punctuation)))

a=['dr','ca','er']            

notdrca=list()
for i in uname:
    if any(x in i.lower() for x in a):
        continue
    else:
        notdrca.append(i)        
        
len2=list()
l1=list()
l3=list()
ln=list()

email_list=list()

for i in notdrca:
    if any(x in i.lower() for x in a):
        print(i)


for i in notdrca:
    try:
        i=i.lower()
        s=i.split()

        if len(s)==2:
            email_list.extend(formats(s[0],s[1],'','gmail.com'))
            len2.append(i)
        elif len(s)==1:
            email_list.extend(formats(s[0],'','','gmail.com'))        
            l1.append(i)
        elif len(s)==3:
            email_list.extend(formats(s[0],s[1],s[2],'gmail.com'))    
            l3.append(i)
        elif len(s)>3:
            ln.append(i)
            continue    
    except:
        continue        


try:
    h=open('emails.pickle','wb')
except Exception as e:
    print(e)
    
pickle.dump(email_list,h)



regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

match=re.match(regex,'harsha_nihar@yahoon')
if match==None:
    print(match)

