import streamlit as st
from pytube import YouTube
from pydub import AudioSegment
import requests
import os

# Set up Hugging Face API details
API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v2"
headers = {"Authorization": "Bearer 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"}

# Function to query the Hugging Face model
def query_audio(audio_path):
    with open(audio_path, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

# Function to download audio from YouTube
def download_youtube_audio(url):
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    stream.download(filename="audio.mp4")
    audio = AudioSegment.from_file("audio.mp4")
    audio.export("audio.wav", format="wav")
    return "audio.wav"

# Streamlit app configuration
st.set_page_config(page_title="YouTube Audio Transcription", page_icon='🎧', layout='centered')

st.header("YouTube Audio Transcription 🎧")

# Input field for YouTube URL
youtube_url = st.text_input("Enter YouTube video URL")

# Submit button
if st.button("Transcribe"):
    if youtube_url:
        with st.spinner("Downloading audio and transcribing, please wait..."):
            # Download and convert audio
            audio_path = download_youtube_audio(youtube_url)
            
            # Show audio file
            audio_file = open(audio_path, 'rb')
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/wav')

            # Query the Hugging Face model
            transcription = query_audio(audio_path)
            
            if 'text' in transcription:
                transcription_text = transcription['text']
                st.write("Transcription:")
                st.write(transcription_text)
                
                # Make transcription available for download
                st.download_button(label="Download Transcription", 
                                   data=transcription_text, 
                                   file_name="transcription.txt", 
                                   mime="text/plain")
            else:
                st.write("Error in transcription:")
                st.write(transcription)
    else:
        st.write("Please enter a valid YouTube URL")
