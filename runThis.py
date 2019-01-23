#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 18:33:30 2018

@author: chunguanghe
"""

# following 4 lines of code sometimes works and sometimes doesn't; The result is saved in csv in zip file;
# import Google_Trends_Scraper
# import GoogleIndex_clean
# Google_Trends_Scraper.google_index()
# GoogleIndex_clean.clean()

import boxOffice
boxOffice.getBoxOfficeData()

import TwitterFollowersCount
TwitterFollowersCount.getStudioData()

import movie_rate
movie_rate.getMovieRate()



#following code are merging and cleaning data
import pandas as pd
import numpy as np

stockPrice = pd.read_excel("stock_price_downloaded_from_databases.xlsx")
boxOffice = pd.read_csv("boxOfficeData_raw.csv")
googleIndex = pd.read_csv("GoogleIndexs_clean.csv")
movieRate = pd.read_csv("moviescore.csv")
twitterStudioFollower = pd.read_csv("twitterStudios.csv")
twitterMoviesFollower = pd.read_csv("twitterMoviess.csv")

# map studio with parent company
mapping = {'FOX':'Fox','VIA':'Par.','CMCSA':'Uni.','T':'WB','LGF':'LGF','SNE':'Sony','DIS':'BV'}
mapping = dict(zip(list(mapping.values()),mapping.keys()))

googleIndex['Parent Company']= googleIndex['Studio'].map(mapping)
boxOffice['Parent Company']= boxOffice['Studio'].map(mapping)
# add studio and parent company data
movieRate = pd.merge(movieRate,boxOffice,left_on='movie',right_on='Title',how = 'left')[['movie','metascore','imdbscore','Studio','Parent Company']]
# add studio and parent company to twitter movie follower data
twitterMoviesFollower = pd.merge(twitterMoviesFollower,boxOffice,left_on='movie name',right_on='Title',how = 'left').drop(columns=['account name','Title','Weekend Gross','Theater Count','Average','Total Gross','Budget'])
# boxOffice data cleanning: discard the dollar sign and comma in numbers and transfer them to float number
boxOffice['Theater Count'] = boxOffice['Theater Count'].str.replace(",","").astype(float)
boxOffice['Average'] = boxOffice['Average'].str.replace(r"[$,]","").astype(float)
boxOffice['Total Gross'] = boxOffice['Total Gross'].str.replace(r"[$,]","").astype(float)
boxOffice['Weekend Gross'] = boxOffice['Weekend Gross'].str.replace(r"[$,]","").astype(float)
boxOffice['Budget'] = boxOffice['Budget'].str.replace(r"[$,]","")
boxOffice['Budget'] = boxOffice['Budget'].str.replace("-",str(np.nan),regex=True)

# first sheet: company newest date example overall stock price, movie number, weekend gross, etc.
companyOverall = stockPrice[stockPrice['Date']==stockPrice['Date'].max()]
# add in theater movie number and total weekend gross to each company
companyOverall = pd.merge(companyOverall,boxOffice[['Parent Company','Title']].groupby('Parent Company').count(),left_on="Parent Company",right_index= True,how = 'left')
companyOverall = pd.merge(companyOverall,boxOffice[['Weekend Gross','Parent Company']].groupby('Parent Company').sum(),left_on="Parent Company",right_index= True,how='left')
companyOverall.rename(columns={'Title':"In Theater Movies"},inplace=True)
# googleIndex data cleaning
googleIndex['Date'] = googleIndex['Date'].astype('datetime64')
# add in movies' total google index to each company
googleIndexGroupBy = googleIndex.groupby(['Date','Parent Company']).sum()
googleIndexGroupBy.reset_index(level=['Date', 'Parent Company'],inplace=True)
companyOverall = pd.merge(companyOverall,googleIndexGroupBy,on=["Parent Company",'Date'],how = 'left')
# add in average movie score to each company
companyAveMovieScore = movieRate.groupby('Parent Company').mean()
companyOverall = pd.merge(companyOverall,companyAveMovieScore,on="Parent Company",how = 'left')
# add twitter total movie follower data
companyOverall = pd.merge(companyOverall,twitterMoviesFollower.groupby('Parent Company').sum(),on ='Parent Company',how = 'left')

#third sheet: all movies details
allMovies = pd.merge(boxOffice,googleIndex.groupby('MovieTitle').mean(),left_on='Title',right_on='MovieTitle',how = 'left')
allMovies = pd.merge(allMovies,movieRate,left_on='Title',right_on= 'movie',how = 'left').drop(columns=['Parent Company_y','Studio_y'])
allMovies = pd.merge(allMovies,twitterMoviesFollower,left_on='Title',right_on= 'movie name',how = 'left').drop(columns=['Parent Company','Studio'])
allMovies = allMovies[['Parent Company_x', 'Studio_x','Title','Total Gross','GoogleIndex','metascore','imdbscore',' followers count',' tweets count']]
allMovies.rename(columns={'Parent Company_x':"Parent Company","Studio_x":"Studio","Title":"Movie","GoogleIndex":"AveGoogleIndex"},inplace=True)

writer = pd.ExcelWriter('group8_Result.xlsx', engine='xlsxwriter')
# Write each dataframe to a different worksheet.
companyOverall.to_excel(writer,sheet_name = "companyOverall",index = False)
stockPrice.to_excel(writer,sheet_name = "stockPrice",index = False)
allMovies.to_excel(writer,sheet_name = "allMovies",index = False)
writer.save()

import analysis_JL
analysis_JL.analysis()