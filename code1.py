import streamlit as st
import requests

API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-hf"
HEADERS = {
    "Authorization": "Bearer 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"
}

def query(payload):
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    return response.json()

# Streamlit configuration
st.set_page_config(page_title="Generate Blogs",
                   page_icon='🤖',
                   layout='centered',
                   initial_sidebar_state='collapsed')

st.header("Generate Blogs 🤖")

# Input fields
input_text = st.text_input("Enter the Blog Topic")

# Additional fields
col1, col2 = st.columns([5, 5])
with col1:
    no_words = st.text_input('No of Words')
with col2:
    blog_style = st.selectbox('Writing the blog for',
                              ('Researchers', 'Data Scientist', 'Common People'), index=0)

# Submit button
submit = st.button("Generate")

# Handle submission
if submit and input_text:
    payload = {
        "inputs": f"Write a blog for {blog_style} for a topic {input_text} within {no_words} words."
    }
    response = query(payload)
    st.write(response)
