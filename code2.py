import streamlit as st
import requests
import time

# Define the API endpoint and headers
API_URL = "https://api-inference.huggingface.co/models/bartowski/gemma-2-27b-it-GGUF"
headers = {"Authorization": "Bearer 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"}

# Function to query the model
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Streamlit app configuration
st.set_page_config(page_title="Text Generation App", page_icon='🤖', layout='centered')

st.header("Text Generation App 🤖")

# Input field for user query
input_text = st.text_input("Enter your prompt here")

# Submit button
if st.button("Generate Text"):
    if input_text:
        with st.spinner("Generating text..."):
            # Initialize progress bar
            progress_bar = st.progress(0)
            progress = 0

            while True:
                output = query({"inputs": input_text})
                
                if 'error' in output and "loading" in output['error']:
                    estimated_time = output.get("estimated_time", 20)
                    st.write(f"Model is loading. Estimated time: {estimated_time} seconds.")
                    
                    for _ in range(estimated_time):
                        time.sleep(1)
                        progress += 1 / estimated_time
                        progress_bar.progress(min(progress, 1.0))
                else:
                    if 'generated_text' in output:
                        # Display the generated text
                        st.write("Generated Text:")
                        st.write(output['generated_text'])
                    else:
                        st.write("Error in generating text:")
                        st.write(output)
                    break
    else:
        st.write("Please enter a valid prompt")

