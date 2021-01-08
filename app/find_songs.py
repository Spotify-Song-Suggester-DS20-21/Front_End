import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
import copy


def make_prediction(song, n=10):
  #Read in data
  data = pd.read_csv("https://raw.githubusercontent.com/Spotify-Song-Suggester-DS20-21/DS_model/main/data.csv")
  #TODO change to file name app/data.csv
  df = data.copy()

  #Cleaning the Artist Column
  def FixArtist(artist):
    artist=artist.replace("'","").replace("'","").replace('[','').replace(']','')
    return artist

  df['artists'] = df['artists'].apply(FixArtist)
  data['artists'] = data['artists'].apply(FixArtist)

  #creating dictionary for lookup after predictions
  dictionary = df[["artists",
                  "name", 
                  "key", 
                  "id",
                  "valence",
                  "acousticness",
                  "danceability",
                  "energy",
                  "instrumentalness",
                  "liveness",
                  "speechiness"]]

  #Dropping columns not suited for a Standard Scaler fit which is neccesary for NearestNeighbors
  df = df.drop(['artists','id','name','release_date'], axis = 1)

  #Transforming dataset to standard scaler
  scaler = StandardScaler()
  df_s = scaler.fit_transform(df)

  #The NN Model
  nn = NearestNeighbors(n_neighbors=10, algorithm='kd_tree')
  nn.fit(df_s)

  #Used for the autocomplete drop down box when submitting your song
  def find_word(word,df,number=10):
      df.drop_duplicates(inplace=True)
      words=df['name'].values
      artists=df['artists'].values
      t=[]
      count=0
      if word[-1]==' ':
          word=word[:-1]
      for i in words:
          if word.lower() in i.lower():
              t.append([len(word)/len(i),count])
          else:
              t.append([0,count])
          count+=1
      t.sort(reverse=True)
      s=[[words[t[i][1]],artists[t[i][1]].strip('][').split(', ')] for i in range(number)]   
      songs=[words[t[i][1]] for i in range(number)]
      artist=[artists[t[i][1]] for i in range(number)]
      x=[]
      for i in s:
          l=''
          by=''
          for j in i[1]:
              by+=j
          l+=i[0]+' by '+by
          x.append(l)
      tup=[]
      for i in range(number):
          tup.append((x[i],i))

      
      return tup,songs,artist

  #Method for importing elsewhere
  def PredictNSimilarSongs(song_name, artist, n):
      
      n = n-1
      #Matches Song with the artist
      index = 0
      indices = []
      
      for i, item in enumerate(data['artists']):
          if(item == artist):
              indices.append(i)
      
      for item in indices:
          if(data['name'][item] == song_name):
              index = item
      
      #Gets Predictions with NN
      neighbor_predictions = nn.kneighbors([df_s[index]])
      
      #Finds the prediction's names and who its by in the dictionary
      list_of_predictions = neighbor_predictions[1][0].tolist()

      ten_similar_tracks_title = []
      for item in list_of_predictions:
          track_hash = dictionary['name'].iloc[item]
          ten_similar_tracks_title.append(track_hash)
      
      ten_similar_tracks_artists = []
      for item in list_of_predictions:
          track_hash = dictionary['artists'].iloc[item]
          ten_similar_tracks_artists.append(track_hash)

      ten_suggestions = []
      for i in range(0,n+1):
          ten_suggestions.append(ten_similar_tracks_title[i] + ' by ' + ten_similar_tracks_artists[i])
          
      
      return ten_suggestions

    #Gets Predictions with NN
    #neighbor_predictions = nn.kneighbors([df_s[index]])

  tup,s,ar=find_word(song,data)

  prediction = PredictNSimilarSongs(s[0], ar[0], n)

  return prediction

#make_prediction('piano man', n=10)