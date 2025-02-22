import os
import streamlit as st
from app.spotify_api import get_spotify_client, get_spotify_auth_url, get_top_tracks, CACHE_FILE
#from plotting import create_songs_df, create_songs_feature_df
import pandas as pd

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

def run_app():
    st.write("My Spotify Wrapped Clone")
    
    # When the user clicks the "Sign in with Spotify" button:
    if st.button("Sign in with Spotify"):
        # Clear session state and cached token file to allow signing in with a different account.
        st.session_state.clear()
        if os.path.exists(CACHE_FILE):
            os.remove(CACHE_FILE)
        st.write("Click the link below to sign in to your Spotify Account:")
        # Always generate a fresh auth URL for a new OAuth flow.
        auth_url = get_spotify_auth_url()
        st.markdown(f"[Authorize Spotify]({auth_url})", unsafe_allow_html=True)
    else:
        # Handle the OAuth callback or cached token scenario.
        query_params = st.query_params  # Get query parameters from the URL.
        spotify_client = get_spotify_client(auth_response=query_params)
        
        if isinstance(spotify_client, dict) and "auth_url" in spotify_client:
            st.write("Please click the button above to sign in with Spotify.")
        else:
            # A Spotify client with a valid access token was returned.
            st.write("Fetching your Spotify data...")
            try:
                top_tracks = get_top_tracks(spotify_client)
                # recent_song = get_recently_played_songs(spotify_client)

                # Prints Top Tracks
                if top_tracks and top_tracks.get("items"):
                    st.write("### Your Top Tracks:")
                    for idx, track in enumerate(top_tracks["items"]):
                        track_name = track.get("name", "Unknown")
                        artists = ", ".join([artist.get("name", "Unknown") for artist in track.get("artists", [])])
                        st.write(f"{idx + 1}. **{track_name}** by {artists}")
                else:
                    st.write("No top tracks found or unable to fetch data.")

                """
                # Prints Recent Listened Tracks
                if recent_song and recent_song.get("items"):
                    st.write("### Recent Tracks Tracks:")
                    for idx, track in enumerate(recent_song["items"]):
                        track_info = track['track']
                        track_name = track_info.get("name", "Unknown")
                        artists = ", ".join([artist.get("name", "Unknown") for artist in track.get("artists", [])])
                        st.write(f"{idx + 1}. **{track_name}** by {artists}")
                    else:
                        st.write("No recently played tracks found or unable to fetch data.")
                """

                # Break Line
                st.markdown("<br><br>", unsafe_allow_html=True)
                # Header
                st.header("Your Top Tracks and Their Popularity Worldwide")
                # Bar-Graph displaying the Top 10 Songs and their popularity ranks
                track_df = create_songs_df(top_tracks)
                st.bar_chart(track_df.set_index('name')['popularity'])

            except Exception as e:
                st.error(f"An error occurred: {e}")
