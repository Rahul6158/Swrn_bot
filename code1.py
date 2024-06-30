import streamlit as st
import requests

API_URL = "https://api-inference.huggingface.co/models/distilbert/distilgpt2"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        if "generated_text" in data:
            return data["generated_text"]
        else:
            st.error("Unexpected response format from the API.")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching response: {str(e)}")
        return None

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
    if response is not None:
        st.write(response)
