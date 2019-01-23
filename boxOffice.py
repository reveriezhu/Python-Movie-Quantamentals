#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 18:51:15 2018

@author: chunguanghe
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
def getBoxOfficeData():
    page = requests.get("https://www.boxofficemojo.com/weekend/chart/")
    soup = BeautifulSoup(page.content,'html.parser')
    df=pd.DataFrame(columns=('Title','Studio','Weekend Gross','Theater Count','Average','Total Gross','Budget'))
    count=0
    for td in soup.findAll('table')[4].findAll('tr')[1:-1]:
        Title = td.getText().split("\n")[2]
        Studio = td.getText().split("\n")[3]
        WeekendGross = td.getText().split("\n")[4]
        TheaterCount = td.getText().split("\n")[6]
        Average = td.getText().split("\n")[8]
        TotalGross = td.getText().split("\n")[9]
        Budget = td.getText().split("\n")[10]
        df.loc[count]=[Title,Studio,WeekendGross,TheaterCount,Average,TotalGross,Budget]
        count=count+1
    df.to_csv("boxOfficeData_raw.csv",index = False)