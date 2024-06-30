import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set environment variables
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

# Initialize OpenAI model
llm_openai = ChatOpenAI(model="gpt-3.5-turbo")
output_parser = StrOutputParser()

# Initialize LLama 2 model
llm_llama = CTransformers(
    model='llama-2-7b-chat',
    model_type='llama',
    config={'max_new_tokens': 256, 'temperature': 0.01}
)

# Langchain prompt for OpenAI
prompt_openai = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Please respond to user queries"),
    ("user", "Question: {question}")
])

# Langchain prompt for LLama 2
template_llama = """
    Write a blog for {blog_style} job profile for a topic {input_text}
    within {no_words} words.
"""
prompt_llama = PromptTemplate(input_variables=["blog_style", "input_text", "no_words"], template=template_llama)

# Streamlit configuration
st.set_page_config(page_title="Language Models Demo",
                   page_icon='🤖',
                   layout='centered',
                   initial_sidebar_state='collapsed')

# Streamlit app title
st.title('Language Models Demo')

# Choose model type
model_choice = st.radio("Select Model", ("OpenAI GPT-3.5 Turbo", "LLama 2"))

# If OpenAI GPT-3.5 Turbo is selected
if model_choice == "OpenAI GPT-3.5 Turbo":
    input_text_openai = st.text_input("Ask a question")
    if input_text_openai:
        chain_openai = prompt_openai | llm_openai | output_parser
        st.write(chain_openai.invoke({'question': input_text_openai}))

# If LLama 2 is selected
elif model_choice == "LLama 2":
    st.header("Generate Blogs 🤖")
    input_text_llama = st.text_input("Enter the Blog Topic")

    # Additional fields for LLama 2
    col1, col2 = st.columns([5, 5])
    with col1:
        no_words_llama = st.text_input('No of Words')
    with col2:
        blog_style_llama = st.selectbox('Writing the blog for', ('Researchers', 'Data Scientist', 'Common People'), index=0)

    # Submit button for LLama 2
    submit_llama = st.button("Generate")

    # Handle submission for LLama 2
    if submit_llama:
        response_llama = llm_llama(prompt_llama.format(blog_style=blog_style_llama, input_text=input_text_llama, no_words=no_words_llama))
        st.write(response_llama)
