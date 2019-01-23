from urllib.request import urlopen 
from bs4 import BeautifulSoup
import pandas as pd

# This py is used to find all 'metascore' for ecach current movie, notice that there are some movie have no metascore
# the result will update according to the current movie and movie score!
def getMovieRate():
    html = urlopen('https://www.imdb.com/movies-in-theaters/?ref_=nv_mv_inth')

    # create the BeautifulSoup object (BeautifulSoup Yield Curve)
    bsyc = BeautifulSoup(html.read(), "html.parser")

    # so get a list of all table tags
    table_list = bsyc.findAll('table')


    # find all the 'span' with name of 'metascore', which is the movie score we want
    tc_table_list = bsyc.findAll('span', {"class": "metascore"})
    tc_table_list_0 = bsyc.findAll('h4')

    # find all 'metascore' for ecach current movie, notice that there are some movie have no metascore

     #this is the list to store the movie(key)-score(value) pair!

    movie_score_list = []

    for c in table_list:
        score = -1
        imdbscore = -1
        if c.findAll('div', {"class":"rating rating-list"}):
            imdb = c.findAll('div', {"class":"rating rating-list"})[0].getText() # clean the data
            s = imdb.split("\n")
            imdbscore = s[18].replace("/10","")
        if c.findAll('span', {"class": "metascore"}):
            score = c.findAll('span', {"class":"metascore"})[0].getText().strip()#clean the data
        if c.findAll('h4'):
            movie = c.findAll('h4')[0].getText().strip().replace("(2018)", "").replace("(2017)", "").replace(" - [Limited]", "").strip()#clean the data
        if (score != -1) & (imdbscore == -1) :#to exclude movie with no score
            movie_score_list.append([movie, int(score),])
        if (score != -1) & (imdbscore != -1):
            movie_score_list.append([movie, int(score) , float(imdbscore)])


    frame = pd.DataFrame(movie_score_list, columns = ['movie','metascore', 'imdbscore'])
    #save the moviescore to the csv file
    frame.to_csv("moviescore.csv", index=False)