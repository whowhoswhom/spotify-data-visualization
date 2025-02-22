# plotting.py
import pandas as pd
from app.spotify_api import get_spotify_client, get_top_tracks

def create_songs_feature_df(df, sp):
    if 'id' not in df.columns:
        raise ValueError("The dataframe must contain an 'id' column.")
    tracks_ids = [track['id'] for track in df[['id']].to_dict('records')]
    audio_features = sp.audio_features(tracks_ids)
    df_2 = pd.DataFrame(audio_features)
    df_2 = df_2[['danceability', 'energy', 'loudness', 'liveness','duration_ms']]
    df_2.reset_index(drop=True, inplace=True)
    return df_2

# Updated to extract the actual track info from the 'track' key.
def recently_played_songs(tracks):
    # Each item in tracks['items'] is a dict with a 'track' key.
    df = pd.DataFrame([item['track'] for item in tracks['items']])
    df = df[['artists', 'name']]
    # Extract the first artist's name from the list of artists.
    df['artists'] = df['artists'].apply(lambda artists: artists[0]['name'] if artists else "unknown")
    df[['artists', 'name']] = df[['artists', 'name']].applymap(lambda x: x.lower().replace(' ', ''))
    return df

def create_songs_df(tracks):
    df = pd.DataFrame(tracks['items'])[['id', 'artists', 'name', 'popularity']]
    df['artists'] = df['artists'].apply(lambda x: x[0]['name'])
    df[['artists', 'name']] = df[['artists', 'name']].applymap(lambda x: x.lower().replace(' ', ''))
    df = df.drop_duplicates().sort_values(by='popularity', ascending=False).reset_index(drop=True)
    return df
