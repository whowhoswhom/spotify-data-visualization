import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Define a cache file name based on your client_id (adjust if needed)
CACHE_FILE = ".cache-eb144adf5bdc40679ef5144f9fedc271"

def get_spotify_auth_url():
    """
    Generate and return the Spotify authorization URL.
    """
    scope = "user-top-read"  # Adjust this scope as needed.
    sp_oauth = SpotifyOAuth(
        client_id="eb144adf5bdc40679ef5144f9fedc271",       # Replace with your actual Client ID.
        client_secret="34a058f0ede0405fb3ae5ff42d8c8e4e",     # Replace with your actual Client Secret.
        redirect_uri="http://localhost:8501",                 # Must match your Streamlit app's redirect URI.
        scope=scope,
        cache_path=CACHE_FILE
    )
    return sp_oauth.get_authorize_url()

def get_spotify_client(auth_response=None):
    """
    Authenticate the user with Spotify and return a Spotify client instance.
    If an OAuth callback has occurred (provided via auth_response), it exchanges the code for an access token.
    If no token is cached and no OAuth callback is available, it returns a dict with the auth URL.
    """
    scope = "user-top-read"  # Adjust this scope based on your needs.
    sp_oauth = SpotifyOAuth(
        client_id="eb144adf5bdc40679ef5144f9fedc271",
        client_secret="34a058f0ede0405fb3ae5ff42d8c8e4e",
        redirect_uri="http://localhost:8501",
        scope=scope,
        cache_path=CACHE_FILE
    )

    # Try to retrieve a cached token.
    token_info = sp_oauth.get_cached_token()
    if not token_info:
        # If no token is cached, check for an OAuth callback (via auth_response).
        if auth_response is None or "code" not in auth_response:
            # No OAuth info yet – return the auth URL so the app can instruct the user.
            auth_url = sp_oauth.get_authorize_url()
            return {"auth_url": auth_url}
        else:
            # Extract the authorization code from the query parameters.
            code = auth_response["code"][0] if isinstance(auth_response["code"], list) else auth_response["code"]
            token_info = sp_oauth.get_access_token(code)

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
    """
    Over what time frame the affinities are computed. Valid values: long_term (calculated from ~1 year of data 
    and including all new data as it becomes available), medium_term (approximately last 6 months), 
    short_term (approximately last 4 weeks). Default: medium_term
    """

    results = sp.current_user_top_tracks(limit=limit, time_range="long_term")
    return results

