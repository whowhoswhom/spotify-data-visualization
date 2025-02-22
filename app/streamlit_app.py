# app/streamlit_app.py

import streamlit as st
from app.spotify_api import get_spotify_client, get_top_tracks

def run_app():
    st.write("My Spotify Wrapped Clone")
    st.write("This is rendered on the root page of the app.")
    
    # Create a button to fetch Spotify info
    if st.button("Get my Spotify Info"):
        st.write("Fetching your Spotify data...")
        try:
            # Authenticate and get a Spotify client instance
            sp = get_spotify_client()
            # Fetch user's top tracks
            top_tracks = get_top_tracks(sp)
            
            if top_tracks and top_tracks.get('items'):
                st.write("### Your Top Tracks:")
                for idx, track in enumerate(top_tracks['items']):
                    track_name = track.get('name', 'Unknown')
                    artists = ", ".join([artist.get('name', 'Unknown') for artist in track.get('artists', [])])
                    st.write(f"{idx + 1}. **{track_name}** by {artists}")
            else:
                st.write("No top tracks found or unable to fetch data.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
