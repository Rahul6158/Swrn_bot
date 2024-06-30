import streamlit as st
import requests
from langchain.prompts import PromptTemplate
from transformers import pipeline

# Function to get response from Gemma-2-27B model via Hugging Face API
def getGemmaResponse(prompt_text):
    API_URL = "https://api-inference.huggingface.co/models/google/gemma-2-27b-it"
    headers = {"Authorization": "Bearer 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"}
    
    payload = {"inputs": prompt_text}
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["generated_text"]
    else:
        return f"Error: {response.status_code} - {response.reason}"

# Streamlit configuration
st.set_page_config(page_title="Generate Text",
                   page_icon='🤖',
                   layout='centered',
                   initial_sidebar_state='collapsed')

st.header("Generate Text 🤖")

# Input field for user prompt
input_text = st.text_input("Enter the Text Prompt")

# Submit button
submit = st.button("Generate")

# Handle submission
if submit:
    if input_text:
        # Generate text using Gemma-2-27B model
        response = getGemmaResponse(input_text)
        st.write("Generated Text:")
        st.write(response)
    else:
        st.warning("Please enter a text prompt.")
