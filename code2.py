import requests
from bs4 import BeautifulSoup
import telebot
from gtts import gTTS
from googletrans import Translator
import os

# Replace with your own Telegram bot token
TELEGRAM_BOT_TOKEN = '6521994935:AAF9qvs1h4X-ybf2fVa5FKuy7Q-RDhef0Iw'

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
translator = Translator()

# Language mapping
LANGUAGE_MAPPING = {
    '1': 'te',  # Telugu
    '2': 'hi',  # Hindi
    '3': 'en'   # English (as an example, add more as needed)
}

def fetch_blog_content(url):
    response = requests.get(url)
    html_content = response.text
    return html_content

def parse_html_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    paragraphs = soup.find_all('p')
    blog_text = '\n'.join([para.get_text() for para in paragraphs])
    return blog_text

def text_to_speech(text, filename="output.mp3", lang='en'):
    tts = gTTS(text, lang=lang)
    tts.save(filename)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Send me a blog URL and I will fetch the content and convert it to speech.")

@bot.message_handler(commands=['translateto'])
def translate_blog(message):
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "Please specify a number for the language. Example: /translateto 1\n\nAvailable languages:\n1. Telugu\n2. Hindi\n3. English")
            return

        lang_number = parts[1]
        lang_code = LANGUAGE_MAPPING.get(lang_number)

        if not lang_code:
            bot.reply_to(message, "Invalid language number. Please use one of the following:\n1. Telugu\n2. Hindi\n3. English")
            return

        if 'blog_text' not in st.session_state or not st.session_state['blog_text']:
            bot.reply_to(message, "Please first send a blog URL to extract content.")
            return

        original_text = st.session_state['blog_text']
        translated = translator.translate(original_text, dest=lang_code)
        translated_text = translated.text
        st.session_state['translated_text'] = translated_text

        bot.reply_to(message, "Translating text and converting to speech. Please wait...")
        text_to_speech(translated_text, "translated_output.mp3", lang=lang_code)

        with open("translated_output.mp3", "rb") as audio_file:
            bot.send_audio(message.chat.id, audio_file)
        os.remove("translated_output.mp3")
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {e}")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        blog_url = message.text
        bot.reply_to(message, "Fetching blog content...")
        html_content = fetch_blog_content(blog_url)
        blog_text = parse_html_content(html_content)
        st.session_state['blog_text'] = blog_text

        if not blog_text:
            bot.reply_to(message, "No content found at the provided URL.")
            return

        bot.reply_to(message, "Converting text to speech. Please wait...")
        text_to_speech(blog_text)

        with open("output.mp3", "rb") as audio_file:
            bot.send_audio(message.chat.id, audio_file)
        os.remove("output.mp3")
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {e}")

bot.polling()
