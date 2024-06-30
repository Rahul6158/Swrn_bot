import streamlit as st
import requests

API_URL = "https://api-inference.huggingface.co/models/distilbert/distilgpt2"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()["generated_text"]

# Streamlit configuration
st.set_page_config(page_title="Generate Blogs",
                   page_icon='🤖',
                   layout='centered',
                   initial_sidebar_state='collapsed')

st.header("Generate Blogs 🤖")

# Input fields
input_text = st.text_input("Enter the Blog Topic")

# Submit button
submit = st.button("Generate")

# Handle submission
if submit:
    payload = {
        "inputs": input_text
    }
    response = query(payload)
    st.write(response)
