# app/streamlit_app.py

import os
import streamlit as st
from app.spotify_api import get_spotify_client, get_top_tracks

def run_app():
    st.write("My Spotify Wrapped Clone")
    st.write("This is rendered on the root page of the app.")
    
    # Retrieve Spotify credentials from environment variables if they're set.
    # Otherwise, display Streamlit text inputs.
    client_id = os.getenv("SPOTIPY_CLIENT_ID") or st.text_input("Enter your Spotify Client ID", key="client_id")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET") or st.text_input("Enter your Spotify Client Secret", type="password", key="client_secret")
    redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI") or st.text_input("Enter your Spotify Redirect URI", key="redirect_uri")
    
    if st.button("Get my Spotify Info"):
        # Validate that all credentials have been provided
        if not client_id or not client_secret or not redirect_uri:
            st.error("Please provide all Spotify credentials.")
            return
        
        st.write("Fetching your Spotify data...")
        try:
            # Pass the credentials to get the Spotify client instance.
            sp = get_spotify_client(client_id, client_secret, redirect_uri)
            top_tracks = get_top_tracks(sp)
            
            if top_tracks and top_tracks.get("items"):
                st.write("### Your Top Tracks:")
                for idx, track in enumerate(top_tracks["items"]):
                    track_name = track.get("name", "Unknown")
                    artists = ", ".join([artist.get("name", "Unknown") for artist in track.get("artists", [])])
                    st.write(f"{idx + 1}. **{track_name}** by {artists}")
            else:
                st.write("No top tracks found or unable to fetch data.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
