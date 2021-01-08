from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
#from joblib import load
from app.find_songs import make_prediction
import pandas as pd

app = FastAPI(
    title='Spotify Song Suggestor',
    description='Find and visualize songs that fits your personal taste!', 
    docs_url='/'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*']
)

#model = load('app/model.joblib')

class Song(BaseModel):
    song: str = Field(..., example="Piano Man")
    number: int = Field(..., example =10)
    def to_df(self):
        """Convert to pandas dataframe with 1 row."""
        return pd.DataFrame([dict(self)])

@app.post('/predict')
def find_related_songs(song: Song):
    """
    Add which song you want to search up and the number of related songs.
    """

    songs = make_prediction(song.song, song.number)

    return songs
