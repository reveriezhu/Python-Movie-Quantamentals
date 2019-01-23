# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 19:33:48 2018

@author: Asus-pc

This program provides basic analysis on the result from data scrapping and cleaning processes of our project.
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Create three Dataframes based on the result of data scrapping and cleaning process
xlsx = pd.ExcelFile('group8_Result.xlsx')
df1 = pd.read_excel(xlsx, 'companyOverall')
df2 = pd.read_excel(xlsx, 'stockPrice')
df3 = pd.read_excel(xlsx, 'allMovies')

#this function prepares the Pandas Dataframe for Studio Statistics function of the program
def dfStudioStat(studioIndex): 
    infoDF = df1.iloc[studioIndex - 1]
    stockDF = df2.iloc[((studioIndex - 1) * 22):(studioIndex * 22), 1:]
    stockDF['Date'] =  pd.to_datetime(stockDF['Date'], format='%d%b%Y')
    #stockDF = stockDF.set_index('Date')
    movieDF = df3.loc[df3['Parent Company'] == infoDF[0]]
    return infoDF, stockDF, movieDF

#this function creates two plots for the studio when it's called and save the figures to the folder
def plot_stockPrice(df,studioName):
    #High, Low, Close price plot
    df.plot(x = 'Date', y = ['High', 'Low', 'Close'], figsize = (10,4), grid = True)
    plt.title(studioName + ' from ' + str(df['Date'].iloc[0].date()) + ' to ' + str(df['Date'].iloc[-1].date()))
    plt.ylabel('stock price')
    fig1 = plt.gcf()
    plt.show()
    figName = studioName + '_' + str(df['Date'].iloc[0].date()) + '_' + str(df['Date'].iloc[-1].date())
    fig1.savefig(figName + '_stockPrice.png')
    
    #Volatility plot
    df['Change'] = np.log(df['Close']/df['Close'].shift())
    df['Volatility'] = df['Change'].rolling(8).std().shift()
    df.plot(x = 'Date', y = 'Volatility', figsize = (10,4), grid = True)
    plt.title(studioName + ' from ' + str(df['Date'].iloc[0].date()) + ' to ' + str(df['Date'].iloc[-1].date()))
    plt.ylabel('volatility')
    plt.legend()
    fig2 = plt.gcf()
    plt.show() 
    fig2.savefig(figName + '_volatility.png')

#this function creates one plot of cumulative Google Index of all rencent movies for the Studio and save the figure to the folder
def plot_googleIndex(studioName):
    sName = {'FOX':'Fox', 'CMCSA':'Uni.', 'DIS':'BV', 'SNE':'Sony', 'T':'WB','VIA':'Par.'}
    raw_df = pd.read_csv('GoogleIndexs_clean.csv')
    df = raw_df[raw_df['Studio'] == sName[studioName]]
    df = pd.DataFrame(df.groupby('Date')['GoogleIndex'].sum()).reset_index()
    df['Date'] = pd.to_datetime(df['Date'])
    print('\nPlease find the accumulative Google Index for ' + studioName + ' from ' + str(df['Date'].iloc[0].date()) + ' to ' + str(df['Date'].iloc[-1].date()) + ': ')
    df.plot(x = 'Date', y = 'GoogleIndex', figsize = (10, 4), grid = True)
    plt.title(studioName + ' from ' + str(df['Date'].iloc[0].date()) + ' to ' + str(df['Date'].iloc[-1].date()))
    plt.ylabel('Google Index')
    fig1 = plt.gcf()
    plt.show()
    figName = studioName + '_' + str(df['Date'].iloc[0].date()) + '_' + str(df['Date'].iloc[-1].date())
    fig1.savefig(figName + '_GoogleIndex.png')
    
#this function is called and execuate when users chooses "Studio Statistics" option
#It allows users to select a studio of interest from the major studios list and outputs the basic statistics of the studio's parent company
#informations includes stock prices, google index, metascore, imdbscore, followers count and tweets count
def studioStatistics():
    print('\nPlease enter 1-7 to choose from the major studios:')
    choice = int(input('1-21st Century Fox (20th Century Fox)\n2-Comcast Corporation (Universal Pictures)\n3-The Walt Disney Company (Walt Disney Pictures)\n4-Lions Gate Entertainment Corp\n5-Sony (Columbia Pictures)\n6-AT&T (Warner Bros.)\n7-Viacom (Paramount Pictures)\n'))
    infoDF,stockDF, movieDF = dfStudioStat(choice)
    print('\nPlease find the info for ' + infoDF[0] + ' on ' + str(infoDF[1].date()) + ' as follows:')
    print(infoDF.iloc[2:7]) if choice == 4  else print(infoDF.iloc[2:])
    print('\nPlease find the stock price for ' + infoDF[0] + ' from ' + str(stockDF['Date'].iloc[0].date()) + ' to ' + str(stockDF['Date'].iloc[-1].date()) + ': ')
    plot_stockPrice(stockDF,infoDF[0])
    if(infoDF[0] != 'LGF'):
        print('\nPlease find the movies on show for ' + infoDF[0] + ': ')
        movieDF = movieDF.replace(np.nan, '', regex=True)
        movieDF = movieDF.set_index('Movie')
        print(movieDF.iloc[:,2:])
        plot_googleIndex(infoDF[0])

#this function is called and execuate when users chooses "Studio Comparison" option
#It allows users to select one of the 7 criteria and outputs the information of the studio which has the maximum value of the selected criteria
def studioComparison(df1):
    df1 = df1.set_index('Parent Company')
    print('\nPlease enter criteria to find the maximum of each category: ')
    choice = int(input('1-In Theater Movies\n2-Weekend Gross\n3-Google Index\n4-Metascore\n5-IMDB score\n6-Twitter Followers Count\n7-Tweets Count\n'))
    dict = {1: 'In Theater Movies', 2: 'Weekend Gross', 3: 'GoogleIndex', 4: 'metascore', 5: 'imdbscore', 6: ' followers count', 7: ' tweets count'}
    print('\nStudio with Maximum ' + dict[choice] + ': ')
    print(df1[df1[dict[choice]] == df1[dict[choice]].max()].iloc[:, 7:].replace(np.nan, '', regex=True))

#this function is called and execuate when users chooses "Recent Movies Comparison" option
#It allows users to select one of the 7 criteria and outputs the information of the movie which has the maximum value of the selected criteria
def MovieComparison(df3):
    df3 = df3.set_index('Movie')
    print('\nPlease enter criteria to find the maximum of each category: ')
    choice = int(input('1-Total Gross\n2-Avg Google Index\n3-Metascore\n4-IMDB score\n5-Twitter Followers Count\n6-Tweets Count\n'))
    dict = {1: 'Total Gross', 2: 'AveGoogleIndex', 3: 'metascore', 4: 'imdbscore', 5: ' followers count', 6: ' tweets count'}
    print('\nMovie with Maximum ' + dict[choice] + ': ')
    print(df3[df3[dict[choice]] == df3[dict[choice]].max()].iloc[:, 2:].replace(np.nan, '', regex=True))
    
#program execution
print('------Hollywood Major Studio Analysis------')
continuing = 1

while(continuing):
    print('\n------------------------------------------------------\nPlease enter 1-4 to choose from the following options:')
    choice = int(input('1-Studio Statistics\n2-Studio Comparison\n3-Recent Movies Comparison\n4-Quit\n'))
    
    if(choice == 1):
        print('\n---------------------------------Studio Statistics---------------------------------')
        studioStatistics()
        
    if(choice == 2):
        print('\n---------------------------------Studio Comparison---------------------------------')
        studioComparison(df1)
        
    if(choice == 3):
        print('\n---------------------------------Recent Movies Comparison---------------------------------')
        MovieComparison(df3)
    
    if(choice == 4):
        print('\nThank you!\nHave a nice day!')
        continuing = 0