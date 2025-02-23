# streamlitapp.py
import os
import streamlit as st
from app.spotify_api import (
    get_spotify_client,
    get_spotify_auth_url,
    get_top_tracks,
    get_top_albums_from_tracks,
    CACHE_FILE,
)
from app.plotting import create_songs_df
import pandas as pd


def run_app():
    # Check query parameters for the Spotify auth code.
    query_params = st.query_params

    # If a valid auth code is present, assume the user has logged in.
    if query_params and "code" in query_params:
        spotify_client = get_spotify_client(auth_response=query_params)
        if isinstance(spotify_client, dict) and "auth_url" in spotify_client:
            st.write("Please click the authorize link to complete sign in to your Spotify account.")
        else:
            try:
                user_info = spotify_client.current_user()
                user_name = user_info.get("display_name", "User")
                profile_images = user_info.get("images", [])
                profile_image_url = profile_images[0]["url"] if profile_images else None
                
                if profile_image_url:
                    # Create a two-column layout: text on the left (3 units) and image on the right (1 unit)
                    col_text, col_image = st.columns([3, 1])
                    with col_text:
                        st.subheader(f"Welcome to your Wrap, {user_name}")
                    with col_image:
                        st.image(profile_image_url, width=125)
                else:
                    st.subheader(f"Welcome to your Wrap, {user_name}")

                # Fetch top tracks with an increased limit.
                top_tracks = get_top_tracks(spotify_client, limit=50)
                if top_tracks and top_tracks.get("items"):
                    st.write("### Your Top Tracks:")
                    for idx, track in enumerate(top_tracks["items"][:10]):
                        track_name = track.get("name", "Unknown")
                        artists = ", ".join([artist.get("name", "Unknown") for artist in track.get("artists", [])])
                        st.write(f"{idx + 1}. **{track_name}** by {artists}")
                else:
                    st.write("No top tracks found or unable to fetch data.")

                st.markdown("<br><br>", unsafe_allow_html=True)
                    
                # Recently Played Songs Section.
                recently_played = spotify_client.current_user_recently_played(limit=10)
                if recently_played and recently_played.get("items"):
                    st.write("### Your Recently Played Songs:")
                    rp_data = []
                    for item in recently_played.get("items", []):
                        track = item.get("track", {})
                        song_name = track.get("name", "Unknown")
                        artists = ", ".join([artist.get("name", "Unknown") for artist in track.get("artists", [])])
                        album = track.get("album", {})
                        album_name = album.get("name", "Unknown Album")
                        images = album.get("images", [])
                        image_url = images[0]["url"] if images else ""
                        img_tag = f'<img src="{image_url}" height="50">'
                        rp_data.append({
                            "Image": img_tag,
                            "Song": song_name,
                            "Artist": artists,
                            "Album": album_name,
                        })
                    rp_df = pd.DataFrame(rp_data)
                    st.markdown(rp_df.to_html(escape=False, index=False), unsafe_allow_html=True)
                else:
                    st.write("No recently played songs found.")
                    
                st.markdown("<br><br>", unsafe_allow_html=True)
                st.header("Your Top Tracks and Their Popularity Worldwide")
                track_df = create_songs_df(top_tracks)
                st.bar_chart(track_df.set_index('name')['popularity'])
                
                # Display Top Albums.
                st.markdown("<br><br>", unsafe_allow_html=True)
                st.header("Your Top 25 Albums of the Last Year")
                top_albums = get_top_albums_from_tracks(top_tracks)
                if top_albums:
                    album_images = [album["image_url"] for album in top_albums]
                    album_names = [album["name"] for album in top_albums]
                    st.image(album_images, width=150, caption=album_names)
                else:
                    st.write("No album data available.")
                
                # Trigger balloons after successfully logging in and displaying your information
                st.balloons()

            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        # If not logged in, show the header and sign-in button.
        st.write("My Spotify Wrapped Clone")
        if st.button("Sign in with Spotify"):
            st.session_state.clear()
            if os.path.exists(CACHE_FILE):
                os.remove(CACHE_FILE)
            st.write("Click the link below to sign in to your Spotify Account:")
            auth_url = get_spotify_auth_url()
            st.markdown(f"[Authorize Spotify]({auth_url})", unsafe_allow_html=True)
        else:
            st.write("Please click the button above to sign in with Spotify.")

if __name__ == "__main__":
    run_app()
