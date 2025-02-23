import streamlit as st
from openai import OpenAI
from app.spotify_api import get_spotify_client, get_top_tracks

client = OpenAI(api_key="dummy")

def get_spotify_context():
    """
    Fetch the user's top tracks and generate a summary for the system prompt.
    """
    query_params = st.query_params
    spotify_client = get_spotify_client(auth_response=query_params)
    if isinstance(spotify_client, dict) and "auth_url" in spotify_client:
        return "User is not authenticated with Spotify; no music data available."
    else:
        top_tracks = get_top_tracks(spotify_client, limit=5)
        if not top_tracks or not top_tracks.get("items"):
            return "No top track data available."
        summary = "User's Top Songs:\n"
        for track in top_tracks["items"]:
            track_name = track.get("name", "Unknown")
            artists = ", ".join([artist.get("name", "Unknown") for artist in track.get("artists", [])])
            summary += f"- {track_name} by {artists}\n"
        return summary

def run_chat():
    st.header("Your Listening Friend")
    
    # Initialize conversation history if not already present.
    if "messages" not in st.session_state:
        spotify_context = get_spotify_context()
        system_msg = (
            "You are a helpful assistant. Below is some context about the user's music taste:\n\n"
            + spotify_context
        )
        st.session_state["messages"] = [
            {"role": "system", "content": system_msg}
        ]
    else:
        # Update the system message with the latest Spotify context.
        spotify_context = get_spotify_context()
        system_msg = (
            "You are a helpful assistant. Below is some context about the user's music taste:\n\n"
            + spotify_context
        )
        st.session_state["messages"][0] = {"role": "system", "content": system_msg}
    
    # Display conversation history.
    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        elif msg["role"] == "assistant":
            st.markdown(f"**Bot:** {msg['content']}")
    
    # Use a form to capture user input.
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("Your message:")
        submit = st.form_submit_button("Send")
    
    if submit and user_input:
        st.session_state["messages"].append({"role": "user", "content": user_input})
        with st.spinner("ListenBot is thinking..."):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state["messages"]
            )
        bot_reply = response.choices[0].message.content
        st.session_state["messages"].append({"role": "assistant", "content": bot_reply})
        st.experimental_rerun()