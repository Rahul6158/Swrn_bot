import requests
from bs4 import BeautifulSoup
import streamlit as st

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

# Streamlit app
st.title("Blog Content Extractor")

blog_url = st.text_input("Enter Blog URL:")

if st.button("Extract Content"):
    if blog_url:
        try:
            html_content = fetch_blog_content(blog_url)
            blog_text = parse_html_content(html_content)
            st.text_area("Extracted Content", blog_text, height=400)
        except Exception as e:
            st.error(f"Error extracting content: {e}")
