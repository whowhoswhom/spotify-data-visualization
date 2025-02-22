# app/spotify_api.py

import spotipy
from spotipy.oauth2 import SpotifyOAuth

def get_spotify_client(auth_response=None):
    """
    Authenticate the user with Spotify and return a Spotify client instance.
    The credentials are defined in this module so that the user doesn't need to
    provide them in the UI. If an OAuth callback has occurred, pass the query parameters
    in `auth_response`. Otherwise, if no token is cached, return a dict with the auth URL.
    """
    scope = "user-top-read"  # Adjust this scope based on your needs.
    sp_oauth = SpotifyOAuth(
        client_id="eb144adf5bdc40679ef5144f9fedc271",       # Replace with your actual Client ID.
        client_secret="34a058f0ede0405fb3ae5ff42d8c8e4e",     # Replace with your actual Client Secret.
        redirect_uri="http://localhost:8501",                 # Must match your Streamlit app's redirect URI.
        scope=scope
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
    results = sp.current_user_top_tracks(limit=limit)
    return results
