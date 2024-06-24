import streamlit as st
from translate import Translator
import google.generativeai as genai
from gtts import gTTS
import base64
import os
import speech_recognition as sr
import requests
from PIL import Image
import io

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
HUGGING_FACE_TOKEN = "####"
GENAI_API_KEY = "####"

# Configure the Gemini AI with the provided API key
genai.configure(api_key=GENAI_API_KEY)

# Initialize the Gemini AI model
model = genai.GenerativeModel('gemini-1.5-flash')

# Function to query Stable Diffusion API
def query_stabilitydiff(payload, headers):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

# Function to translate text
def translate_text(text, dest_language):
    translator = Translator(to_lang=dest_language)
    translation = translator.translate(text)
    return translation

# Function to generate a response using Gemini AI
def generate_gemini_response(prompt):
    response = model.generate_content(prompt)
    return response.text

# Function to convert text to speech and generate a download link
def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    tts.save("response.mp3")

    # Read the audio file and encode it to base64
    audio_file = open("response.mp3", "rb")
    audio_bytes = audio_file.read()
    audio_b64 = base64.b64encode(audio_bytes).decode()
    audio_file.close()
    os.remove("response.mp3")

    return f'<audio controls autoplay><source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3"></audio>'

# Function to recognize speech input
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            st.success(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            st.error("Sorry, I did not understand that.")
        except sr.RequestError:
            st.error("Sorry, there was an issue with the speech recognition service.")
        return None

# Map language to ISO 639-1 code
languages_map = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Bengali": "bn",
    "Gujarati": "gu",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Punjabi": "pa",
    "Odia": "or",
    "Urdu": "ur",
    "Chinese": "zh-CN",
    "Korean": "ko",
    "Japanese": "ja",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Italian": "it",
    "Russian": "ru",
    "Arabic": "ar",
    "Dutch": "nl",
    "Portuguese": "pt",
    "Turkish": "tr",
    "Polish": "pl",
    "Swedish": "sv",
    "Vietnamese": "vi",
    "Greek": "el",
    "Thai": "th",
    "Indonesian": "id"
}

# Sidebar for language selection
selected_language = st.sidebar.selectbox("Select Language", list(languages_map.keys()))
dest_language = languages_map[selected_language]

# Sidebar details
st.sidebar.markdown("""
<div style="font-size: 20px;">NeoChat Features:</div>
Multilingual support
Text-based chat
Speech-to-text interaction
Text-to-speech response
Image generation
""", unsafe_allow_html=True)

st.title("NeoChat")
st.write("\n")

col2 = st.columns([2, 4])

with col2:
    st.markdown("""
    Welcome to NeoChat! Here's what you can do: \n
    1. **Type your messages**: Interact with our chatbot by typing in the chat input box.
    2. **Speak to chat**: Click the microphone button to speak and let the chatbot respond.
    3. **Hear the response**: After typing or speaking, click the speaker button to hear the response.
    4. **Multilingual support**: Communicate in various languages like Telugu, Hindi, and more!
    5. **Generate images**: Start your prompt with 'I' to generate images related to your prompt.
    """)

st.write("\n")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "response_text" not in st.session_state:
    st.session_state.response_text = ""
    st.session_state.is_image_response = False

# Display existing chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.chat_message(message["content"])
    elif message["role"] == "assistant":
        if "image" in message:
            st.image(message["image"], caption=message["content"], use_column_width=True)
        else:
            st.markdown(message["content"])

# Handle new user input
prompt = st.text_input("What's on your mind?")
if st.button("Speak"):
    prompt = recognize_speech()

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    if prompt.startswith('I') or prompt.startswith('generate'):
        # Query Stable Diffusion
        headers = {"Authorization": f"Bearer {HUGGING_FACE_TOKEN}"}
        image_bytes = query_stabilitydiff({"inputs": prompt}, headers)
        image = Image.open(io.BytesIO(image_bytes))

        # Show Result
        msg = f'Here is your image related to "{prompt}"'
        st.session_state.messages.append({"role": "assistant", "content": msg, "image": image})
        st.chat_message("assistant").image(image, caption=prompt, use_column_width=True)
    else:
        st.session_state.response_text = generate_gemini_response(prompt)
        # Translate the response
        if dest_language != 'en':
            translated_response = translate_text(st.session_state.response_text[:400], dest_language)
        else:
            translated_response = st.session_state.response_text
        st.markdown(translated_response)
        st.session_state.messages.append({"role": "assistant", "content": translated_response})

        st.session_state.is_image_response = False

    # Add a "Hear response" button to play the response
    if st.session_state.response_text and not st.session_state.is_image_response:
        if st.button("Hear response"):
            st.markdown(text_to_speech(translated_response), unsafe_allow_html=True)
