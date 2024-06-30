import streamlit as st
from transformers import pipeline

# Initialize the pipeline with Gemma-2-9B model for text generation
pipe = pipeline("text-generation", model="google/gemma-2-9b")

# Streamlit configuration
st.set_page_config(page_title="Generate Text",
                   page_icon='🤖',
                   layout='centered',
                   initial_sidebar_state='collapsed')

st.header("Generate Text 🤖")

# Input field for user prompt
input_text = st.text_input("Enter the text prompt")

# Submit button
submit = st.button("Generate")

# Handle submission
if submit:
    if input_text:
        # Generate text using the Gemma-2-9B model
        response = pipe(input_text, max_length=50, num_return_sequences=1)
        generated_text = response[0]['generated_text']
        st.write("Generated Text:")
        st.write(generated_text)
    else:
        st.warning("Please enter a text prompt.")
