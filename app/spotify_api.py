# spotifyapi.py
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CACHE_FILE = ".cache-eb144adf5bdc40679ef5144f9fedc271"

# Update the scope to include user-read-recently-played.
SCOPE = "user-top-read user-read-recently-played"

def get_spotify_auth_url():
    sp_oauth = SpotifyOAuth(
        client_id="eb144adf5bdc40679ef5144f9fedc271",       # Replace with your Client ID.
        client_secret="34a058f0ede0405fb3ae5ff42d8c8e4e",     # Replace with your Client Secret.
        redirect_uri="http://localhost:8501",                 # Must match your Streamlit app's redirect URI.
        scope=SCOPE,
        cache_path=CACHE_FILE
    )
    return sp_oauth.get_authorize_url()

def get_spotify_client(auth_response=None):
    sp_oauth = SpotifyOAuth(
        client_id="eb144adf5bdc40679ef5144f9fedc271",
        client_secret="34a058f0ede0405fb3ae5ff42d8c8e4e",
        redirect_uri="http://localhost:8501",
        scope=SCOPE,
        cache_path=CACHE_FILE
    )
    token_info = sp_oauth.get_cached_token()
    if not token_info:
        if auth_response is None or "code" not in auth_response:
            auth_url = sp_oauth.get_authorize_url()
            return {"auth_url": auth_url}
        else:
            code = auth_response["code"][0] if isinstance(auth_response["code"], list) else auth_response["code"]
            token_info = sp_oauth.get_access_token(code)
    access_token = token_info["access_token"]
    sp = spotipy.Spotify(auth=access_token)
    return sp

def get_top_tracks(sp, limit=10):
    results = sp.current_user_top_tracks(limit=limit, time_range="long_term")
    return results
