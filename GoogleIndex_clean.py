

import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
def clean():
	rawdata=pd.read_csv('GoogleIndexs_raw.csv')
	keySeries=rawdata['key']

	#using beautifulsoup to scrap movies in release
	page = requests.get("https://www.boxofficemojo.com/weekend/chart/")
	soup = BeautifulSoup(page.content,'html.parser')
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


	newdata=pd.DataFrame(columns=('Date','GoogleIndex','MovieTitle','Studio'))
	count = 0
	for i in range(len(rawdata.index)):
	   newdata.loc[i]=[rawdata['date'][i],rawdata['google_index'][i],rawdata['key'][i],d1[keySeries[i]]]

	newdata.to_csv("GoogleIndexs_clean.csv",index = False)
    
