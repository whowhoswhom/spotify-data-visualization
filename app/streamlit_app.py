# app/streamlit_app.py

import streamlit as st
from app.spotify_api import get_spotify_client, get_top_tracks

def run_app():
    st.write("My Spotify Wrapped Clone")
    
    # Get the query parameters from the URL (needed for the OAuth callback)
    query_params = st.experimental_get_query_params()
    
    # Attempt to retrieve a Spotify client.
    # If no token is cached and no "code" is provided in the URL, get_spotify_client returns a dict with auth_url.
    spotify_client = get_spotify_client(auth_response=query_params)
    
    if isinstance(spotify_client, dict) and "auth_url" in spotify_client:
        # No valid token yet – show the sign-in button.
        if st.button("Sign in with Spotify"):
            st.write("Click the link below to sign in to your Spotify Account:")
            st.markdown(f"[Authorize Spotify]({spotify_client['auth_url']})", unsafe_allow_html=True)
        else:
            st.write("Please click the button above to sign in with Spotify.")
    else:
        # A Spotify client with a valid access token was returned.
        st.write("Fetching your Spotify data...")
        try:
            top_tracks = get_top_tracks(spotify_client)
            
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
