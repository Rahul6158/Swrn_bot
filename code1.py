import streamlit as st
import requests

# Hugging Face API endpoint and token
API_URL = "https://api-inference.huggingface.co/models/openai-community/gpt2-large"
headers = {"Authorization": "Bearer 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"}

# Function to query the GPT-2 large model
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Streamlit configuration
st.set_page_config(page_title="GPT-2 Large Demo",
                   page_icon='🤖',
                   layout='centered',
                   initial_sidebar_state='collapsed')

st.header("GPT-2 Large Model Demo 🤖")

# Input field
input_text = st.text_input("Enter your query")

# Submit button
submit = st.button("Ask")

# Handle submission
if submit and input_text:
    # Query the GPT-2 model
    output = query({
        "inputs": input_text
    })
    
    # Display the response
    if 'error' in output:
        st.error("Failed to get a response. Please try again later.")
    elif 'generated_text' in output:
        st.write(output['generated_text'])
    else:
        st.error("Unexpected response format from the model.")
