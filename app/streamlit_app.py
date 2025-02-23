# streamlitapp.py
import os
import streamlit as st
from app.spotify_api import get_spotify_client, get_spotify_auth_url, get_top_tracks, CACHE_FILE
from app.plotting import create_songs_df  # no longer using recently_played_songs here
import pandas as pd

def get_top_albums_from_tracks(top_tracks, limit=25):
    """
    Process the top_tracks data to extract unique albums.
    The 'count' represents the number of times an album appears.
    """
    album_dict = {}
    for track in top_tracks.get("items", []):
        album = track.get("album", {})
        album_id = album.get("id")
        if album_id:
            if album_id not in album_dict:
                images = album.get("images", [])
                image_url = images[0]["url"] if images else ""
                album_dict[album_id] = {
                    "name": album.get("name", "Unknown Album"),
                    "image_url": image_url,
                    "count": 1
                }
            else:
                album_dict[album_id]["count"] += 1
    album_list = list(album_dict.values())
    album_list.sort(key=lambda x: x["count"], reverse=True)
    return album_list[:limit]

def run_app():
    st.write("My Spotify Wrapped Clone")
    
    if st.button("Sign in with Spotify"):
        st.session_state.clear()
        if os.path.exists(CACHE_FILE):
            os.remove(CACHE_FILE)
        st.write("Click the link below to sign in to your Spotify Account:")
        auth_url = get_spotify_auth_url()
        st.markdown(f"[Authorize Spotify]({auth_url})", unsafe_allow_html=True)
    else:
        query_params = st.query_params
        spotify_client = get_spotify_client(auth_response=query_params)
        
        if isinstance(spotify_client, dict) and "auth_url" in spotify_client:
            st.write("Please click the button above to sign in with Spotify.")
        else:
            st.write("Fetching your Spotify data...")
            try:
                user_info = spotify_client.current_user()
                user_name = user_info['display_name']
                profile_image_url = user_info['images'][0]['url'] if user_info['images'] else None
                if profile_image_url:
                    st.markdown(
                        f"""
                        <style>
                        .profile-image {{
                            width: 100px;
                            height: 100px;
                            border-radius: 50%;
                            object-fit: cover;
                        }}
                        </style>
                        """,
                        unsafe_allow_html=True
                    )
                    st.image(profile_image_url, width=100, caption="Profile Picture")
                else:
                    st.write("No profile picture available.")

                st.subheader(f"Welcome to your Wrap, {user_name}")

                # Fetch top tracks with an increased limit to gather more album data.
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
                    
                # --- Recently Played Songs Feature with Image in Place of Index ---
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
                        # Get the album image URL; use the first image if available.
                        images = album.get("images", [])
                        image_url = images[0]["url"] if images else ""
                        # Create an HTML <img> tag for the album cover. Adjust the height as needed.
                        img_tag = f'<img src="{image_url}" height="50">'
                        rp_data.append({
                            "Image": img_tag,
                            "Song": song_name,
                            "Artist": artists,
                            "Album": album_name,
                        })
                    rp_df = pd.DataFrame(rp_data)
                    # Render the DataFrame as HTML with no index and allow HTML rendering.
                    st.markdown(rp_df.to_html(escape=False, index=False), unsafe_allow_html=True)
                else:
                    st.write("No recently played songs found.")
                    
                st.markdown("<br><br>", unsafe_allow_html=True)
                st.header("Your Top Tracks and Their Popularity Worldwide")
                track_df = create_songs_df(top_tracks)
                st.bar_chart(track_df.set_index('name')['popularity'])

                # --- Display Top Albums using only Streamlit ---
                st.markdown("<br><br>", unsafe_allow_html=True)
                st.header("Your Top 25 Albums of the Last Year")
                top_albums = get_top_albums_from_tracks(top_tracks)
                if top_albums:
                    album_images = [album["image_url"] for album in top_albums]
                    album_names = [album["name"] for album in top_albums]
                    st.image(album_images, width=150, caption=album_names)
                else:
                    st.write("No album data available.")

            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    run_app()
