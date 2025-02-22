import pandas as pd
from spotify_api import get_spotify_client, get_top_tracks

def create_songs_df(sp):

    top_tracks = get_top_tracks(sp, limit=10)

    # Convert to data frame
    df = pd.DataFrame(top_tracks['items'])[['artists', 'name', 'popularity']]

    # Extract the artists name from the nested dictionary
    df['artists'] = df['artists'].apply(lambda x: x[0]['name'])
    # Filtering the Data for more readability (remove spaces and convert to lowercase)
    df[['artists', 'name']] = df[['artists', 'name']].applymap(lambda x: x.lower().replace(' ', ''))
    # Remove duplicates, sort by the popularity and reset index
    df = df.drop_duplicates().sort_values(by='popularity', ascending=False).reset_index(drop=True)

    return df

def create_songs_feature_df(df, sp):
    # Gets the id from the tracks in the dataframe df
    tracks_ids = [track['id'] for track in df['items']]
    # Fetches the audio_features from the track_ids
    audio_features = sp.audio_features(tracks_ids)
    # Converts the audio_feature into a dataframe
    df_2 = pd.DataFrame(audio_features)
    # These are the audio features we are going to be displaying in Streamlit
    df_2 = df_2[['danceability', 'energy', 'loudness', 'liveness','duration_ms']]
    df_2.reset_index('track_name', inplace=True)

    return df_2














