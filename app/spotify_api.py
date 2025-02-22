# app/spotify_api.py

import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def get_spotify_client():
    """
    Authenticate the user with Spotify and return a Spotify client instance.
    Make sure you have the following environment variables set:
    - SPOTIPY_CLIENT_ID
    - SPOTIPY_CLIENT_SECRET
    - SPOTIPY_REDIRECT_URI
    """
    scope = "user-top-read"  # Adjust scope based on the data you need
    sp_oauth = SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope=scope
    )

    # Attempt to retrieve a cached token
    token_info = sp_oauth.get_cached_token()
    if not token_info:
        # If there's no cached token, prompt user to authenticate
        auth_url = sp_oauth.get_authorize_url()
        print("Please navigate here to authorize your application:")
        print(auth_url)
        # For a hackathon setup, you might manually copy-paste the URL redirect response
        redirect_response = input("Paste the URL you were redirected to: ")
        token_info = sp_oauth.get_access_token(redirect_response)

    access_token = token_info["access_token"]
    sp = spotipy.Spotify(auth=access_token)
    return sp

def get_top_tracks(sp, limit=10):
    """
    Retrieve and return the user's top tracks.
    
    Args:
        sp: Authenticated Spotify client instance.
        limit (int): Number of top tracks to fetch.
        
    Returns:
        dict: A dictionary containing the user's top tracks.
    """
    results = sp.current_user_top_tracks(limit=limit)
    return results
