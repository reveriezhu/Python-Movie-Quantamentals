# -*- coding: UTF-8 -*-
import tweepy

def getStudioData():
# Keys, tokens and secrets
  consumer_key = "h9yhiJ6F45gK0q0tJ6EU2I1Vx"
  consumer_secret = "jAI01X3RRsHCSLkuSm2ptujm70GnPFaAe3CNtFtIWxQUFknCau"
  access_token = "1064633226520604674-1zXfPzCZ1fYIvpc4C9kvISjHXcSi7K"
  access_token_secret = "UvrwWkrRU19QsoMkp9mu2BfDby3zmqjlELIdFtlxQwqRs"

  # Tweepy OAuthHandler
  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_token_secret)
  api = tweepy.API(auth)

  # Six major Hollywood Studios
  studios = ['DisneyStudios','ParamountPics','UniversalPics','wbpictures','20thcenturyfox','ColumbiaStudios']

  # Output file
  f = open("twitterStudios.csv","w")
  f.write('studio name,account name, followers count, tweets count\n')

  #print('----------Studios----------')
  for studio in studios:
      user = api.get_user(studio)
      #print(user.name, "(", studio, "):", user.followers_count, user.statuses_count)
      f.write(user.name + "," + studio + "," + str(user.followers_count) + "," + str(user.statuses_count) + "\n")

  f.close()

   #only include the ones found on Twitter & have weekend gross over $10,000
  movies = ['grinchmovie','BoRhapMovie','OverlordMovie','thenutcracker','starisborn2018','DragonTattoo',\
            'nobodysfool','VenomMovie','halloweenmovie','TheHateUGive','SMALLFOOTMovie','beautifulboymov',\
            'cyefm','TOHTheFilm','NightSchool','FirstManMovie','GoosebumpsMovie','BoyErased','HunterKiller',\
            'OldManAndTheGun','mid90smovie','suspiriamovie','johnnyenglish','housewithaclock','CrazyRichMovie',\
            'aprivatewar','indivisiblemov','WildlifeTheFilm','TheIncredibles','mariabycallas','ElRoyaleMovie',\
            'ColetteMovie','ASimpleFavor','DisneyCRobin','thenunmovie','TheFrontRunner','BorderMovie','whattheyhadmov',\
            'HotelT','BodiedMovie','SistersBrosFilm','AlphaTheMovie','predatormovie','Searchingmovie','GosnellMovie']

  # Output file
  f = open("twitterMoviess.csv","w",encoding='utf-8')
  f.write('movie name,account name, followers count, tweets count\n')

  #print('\n----------Movies----------')
  for movie in movies:
      user = api.get_user(movie)
      #print(user.name, "(", movie, "):", user.followers_count, user.statuses_count)
      f.write(user.name + "," + movie + "," + str(user.followers_count) + "," + str(user.statuses_count) + "\n")

  f.close()