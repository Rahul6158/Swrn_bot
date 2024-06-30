import streamlit as st
import requests

# Function to query OpenAI GPT-2 model
def query_openai_gpt2(payload):
    API_URL = "https://api-inference.huggingface.co/models/openai-community/gpt2"
    headers = {"Authorization": "Bearer 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"}

    response = requests.post(API_URL, headers=headers, json=payload)
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
if submit:
    prompt = f"Write a blog for {blog_style} for a topic {input_text} within {no_words} words."
    response = query_openai_gpt2({"inputs": prompt})
    st.write(response)  # Print the entire response object for inspection
