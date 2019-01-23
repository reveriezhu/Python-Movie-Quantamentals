# -*- coding: UTF-8 -*-

import sys
import json
import time
import urllib
import requests
import ssl
import datetime
import calendar
from functools import wraps
import numpy as np
import pandas as pd
from imp import reload
from bs4 import BeautifulSoup
import re
reload(sys)
#sys.setdefaultencoding("utf-8")

#limiting the date range as the past 30 days
now = datetime.datetime.now()
month = (now.month + 10) % 12 + 1
year = int(now.year - month / 12)+1
day = min(now.day, calendar.monthrange(year, month)[1])
before = now.replace(year=year, month=month, day=day)
start_date = before.strftime('%Y-%m-%d')
end_date = now.strftime('%Y-%m-%d')

#using beautifulsoup to scrap movies in release
page = requests.get("https://www.boxofficemojo.com/weekend/chart/")
soup = BeautifulSoup(page.content,'html.parser')
# constructing a dataframe with the title and studio
df=pd.DataFrame(columns=('Title','Studio'))
count=0
for td in soup.findAll('table')[4].findAll('tr')[1:-1]:
    Title = td.getText().split("\n")[2]
      #replace any char that's not space/alphanumeric 
    regex = re.compile('[^a-z A-Z0-9]')
    #First parameter is the replacement, second parameter is your input string
    fTitle = regex.sub('',Title)
    Studio = td.getText().split("\n")[3]
    df.loc[count]=[fTitle,Studio]
    count=count+1
# constructing a map with the title and studio
d1={}
for td in soup.findAll('table')[4].findAll('tr')[1:-1]:
    Title = td.getText().split("\n")[2]
      #replace any char that's not space/alphanumeric 
    regex = re.compile('[^a-z A-Z0-9]')
    #First parameter is the replacement, second parameter is your input string
    fTitle = regex.sub('',Title)
    Studio = td.getText().split("\n")[3]
    d1[fTitle]=Studio


def google_index():

    ssl.wrap_socket = sslwrap(ssl.wrap_socket)
    keys=get_keys()
    #keys=['samsung','abc','gone with the wind']
    result=[]
    '''for key in keys:
         print(key)'''
    for key in keys:
        content = get_google_trend(list(key.split("?")))
        #get_studio(key)
        result.extend(content)      

    formattedResult = pd.DataFrame(result)
    #print(formattedResult)
    
    formattedResult.to_csv("GoogleIndexs_raw.csv",index = False)
    return formattedResult

def get_studio(key):
    studio = d1[key]
    return(studio)
    
# return a list of movies in the release and the name of studio
def get_keys():
    movies = list(df['Title'])
    return(movies)
    
#get the token(for the url of google trend) for each key values(name of movie)
def get_token(keys): # accepting a list of  key values per calling
    q = ''
    for key in keys:
        q += key + ','
    if len(q)  > 0:
        q = q[:-1]
    headers = {}
    headers['Host'] = 'trends.google.com'
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'
    headers['Referfer'] = 'https://trends.google.com/trends/explore?date=today%201-m&q=' + urllib.parse.quote(q)
    headers['Cookie'] = '__utmt=1; __utma=10102256.539038748.1495043708.1495043708.1495435554.2; __utmb=10102256.8.9.1495435587029; __utmc=10102256; __utmz=10102256.1495043708.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); NID=103=JBmZSCUdgzRzy0ZMp31uy5nS1gwKm-imoboVE3nf2HrEX-UXQO95jS1NNaaFE1bkUkQ5MQkc-lveM2g3h4evgY12Bs4UpJS4PbUXBuwiM7CkqAwo8TfRrVPa-wH7uieP'
    headers['Connection'] = 'keep-alive'
    headers['Accept'] = 'application/json, text/plain, */*'
    headers['Accept-Language'] = 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
    headers['Accept-Encoding'] = 'gzip, deflate, sdch, br'
    headers['x-client-data'] = 'CJG2yQEIpbbJAQjEtskBCPucygEIqZ3KAQ=='

    req = {}
    req['category'] = 0
    req['property'] = ''
    req['comparisonItem'] = []
    for key in keys:
        req['comparisonItem'].append({"geo": "","keyword":  urllib.parse.quote(key).replace(' ', '+'),"time":"today+1-m"})
    value = {}
    value['hl'] = 'en-US'
    value['tz'] = '-480'
    value['req'] = str(req).replace(' ','')
    url = 'https://trends.google.com/trends/api/explore?'
    for index in value:
        url = url + index + '=' + value[index] + '&'
    results = requests.get(url, headers=headers, verify=False, allow_redirects=False)
    page = results.content
    jsonData = page[5:]
    data = json.loads(jsonData, encoding="utf-8")
    the_token = data['widgets'][0]['token']
    return the_token



#get the google index from the site pointed to by the url

def get_google_trend(keys):
    token = get_token(keys)
    print(token)
    q = ''
    for key in keys:
        q += key + ','
    if len(q) > 0:
        q = q[:-1]
    headers = {}
    headers['Host'] = 'trends.google.com'
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'
    headers['Referfer'] = 'https://trends.google.com/trends/explore?date=today%201-m&q=' + urllib.parse.quote(q)
    headers['Cookie'] = '__utmt=1; __utma=10102256.539038748.1495043708.1495043708.1495435554.2; __utmb=10102256.9.9.1495435587029; __utmc=10102256; __utmz=10102256.1495043708.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); NID=103=JBmZSCUdgzRzy0ZMp31uy5nS1gwKm-imoboVE3nf2HrEX-UXQO95jS1NNaaFE1bkUkQ5MQkc-lveM2g3h4evgY12Bs4UpJS4PbUXBuwiM7CkqAwo8TfRrVPa-wH7uieP'
    headers['Connection'] = 'keep-alive'
    headers['Accept'] = 'application/json, text/plain, */*'
    headers['Accept-Language'] = 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
    headers['Accept-Encoding'] = 'gzip, deflate, sdch, br'
    headers['x-client-data'] = 'CJG2yQEIpbbJAQjEtskBCPucygEIqZ3KAQ=='

    req = {}
    req['time'] = start_date + "+" + end_date
    req['resolution'] = "DAY"
    req['locale'] = "en-US"
    req['comparisonItem'] = []
    for key in keys:
        req['comparisonItem'].append({"geo": {}, "complexKeywordsRestriction": {"keyword": [{"type": "BROAD", "value": urllib.parse.quote(key).replace(' ','+')}]}})
    req['requestOptions'] = {"property":"","backend":"IZG","category":0}
    value = {}
    value['hl'] = 'en-US'
    value['tz'] = '-480'
    value['req'] = str(req).replace(' ','')
    value['token'] = token
    url = 'https://trends.google.com/trends/api/widgetdata/multiline?'
    for index in value:
        url = url + index + '=' + value[index] + '&'
    results = requests.get(url, headers=headers, verify=False)
    page = results.content
    jsonData = page[5:]
    data = json.loads(jsonData, encoding="utf-8")
    items = data['default']['timelineData']
    result = []
    for item in items:
        timestamp = int(item['time'])
        time_temp = time.localtime(timestamp)
        date = time.strftime("%Y-%m-%d", time_temp)
        values = item['value']
        for index in range(len(values)):
            temp = {'key': keys[index], 'date': date, 'google_index': values[index]}
            result.append(temp)
    return result



def sslwrap(func):
    @wraps(func)
    def bar(*args, **kw):
        kw['ssl_version'] = ssl.PROTOCOL_TLSv1
        return func(*args, **kw)
    return bar



if __name__ == '__main__':
    google_index()

