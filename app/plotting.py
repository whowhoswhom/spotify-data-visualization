import pandas as pd
from spotify_api import get_spotify_client, get_top_tracks

def create_songs_df(sp):

    top_tracks = get_top_tracks(sp, limit=10)

    df = pd.DataFrame(top_tracks)
    df = df[['artists', 'name']]
    df['artists'] = df['artists'].apply(lambda x: x[0]['name'])
    df['artists'] = df['artists'].apply(lambda x: x.replace(' ', ''))
    df['artists'] = df['artists'].apply(lambda x: x.lower())
    df['name'] = df['name'].apply(lambda x: x.replace(' ', ''))
    df['name'] = df['name'].apply(lambda x: x.lower())
    df = df.drop_duplicates()
    df = df.sort_values(by='popularity', ascending=False)
    df = df.reset_index(drop=True)

    return df

def create_songs_feature_df(df, sp):
    tracks_ids = [track['id'] for track in df['items']]
    audio_features = sp.audio_features(tracks_ids)

    df_2 = pd.DataFrame(audio_features)
    df_2 = df_2[['track_name','danceability', 'energy', 'loudness', 'liveness','duration_ms']]
    df_2.reset_index('track_name', inplace=True)

    return df_2














