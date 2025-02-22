import pandas as pd
from app.spotify_api import get_spotify_client, get_top_tracks

def create_songs_feature_df(df, sp):

    if 'id' not in df.columns:
        raise ValueError("The dataframe must contain an 'id' column.")

    # Gets the id from the tracks in the dataframe df
    tracks_ids = [track['id'] for track in df[['id']].to_dict('records')]
    # Fetches the audio_features from the track_ids
    audio_features = sp.audio_features(tracks_ids)
    # Converts the audio_feature into a dataframe
    df_2 = pd.DataFrame(audio_features)
    # These are the audio features we are going to be displaying in Streamlit
    df_2 = df_2[['danceability', 'energy', 'loudness', 'liveness','duration_ms']]
    df_2.reset_index(drop=True, inplace=True)

    return df_2

def recently_played_songs(tracks):
    # Convert to data frame
    df = pd.DataFrame(tracks['items'])[['artists', 'name']]

    # Extract the artists name from the nested dictionary
    df['artists'] = df['artists'].apply(lambda x: x[0]['name'])
    # Filtering the Data for more readability (remove spaces and convert to lowercase)
    df[['artists', 'name']] = df[['artists', 'name']].applymap(lambda x: x.lower().replace(' ', ''))

    return df

def create_songs_df(tracks):
    # Convert to data frame
    df = pd.DataFrame(tracks['items'])[['id', 'artists', 'name', 'popularity']]
    # Extract the artists name from the nested dictionary
    df['artists'] = df['artists'].apply(lambda x: x[0]['name'])
    # Filtering the Data for more readability (remove spaces and convert to lowercase)
    df[['artists', 'name']] = df[['artists', 'name']].applymap(lambda x: x.lower().replace(' ', ''))
    # Remove duplicates, sort by the popularity and reset index
    df = df.drop_duplicates().sort_values(by='popularity', ascending=False).reset_index(drop=True)
    return df
















