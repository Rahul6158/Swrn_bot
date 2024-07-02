import requests
from bs4 import BeautifulSoup
import streamlit as st
import pyttsx3
from tempfile import NamedTemporaryFile

def fetch_blog_content(url):
    # Fetch the HTML content of the blog post
    response = requests.get(url)
    html_content = response.text
    return html_content

def parse_html_content(html_content):
    # Parse HTML and extract text content
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all paragraphs and concatenate their text
    paragraphs = soup.find_all('p')
    blog_text = '\n'.join([para.get_text() for para in paragraphs])
    
    return blog_text

def text_to_speech(text):
    # Initialize the pyttsx3 engine
    engine = pyttsx3.init()
    
    # Convert text to speech
    engine.save_to_file(text, 'temp.mp3')  # Save speech to a temporary file
    engine.runAndWait()

# Streamlit app
st.title("Blog Content Extractor & Text-to-Speech")

blog_url = st.text_input("Enter Blog URL:")
if st.button("Extract Content"):
    if blog_url:
        try:
            html_content = fetch_blog_content(blog_url)
            blog_text = parse_html_content(html_content)
            st.text_area("Extracted Content", blog_text, height=400)

            if st.button("Convert to Speech & Download"):
                text_to_speech(blog_text)
                st.success("Speech generated successfully!")

                # Offer the file download
                with open('temp.mp3', 'rb') as f:
                    audio_bytes = f.read()
                st.audio(audio_bytes, format='audio/mp3', start_time=0)
                st.markdown(get_binary_file_downloader_html('temp.mp3', 'Download Audio'), unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error: {e}")

def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{bin_file}">{file_label}</a>'
    return href

