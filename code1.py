import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers

# Function to get response from LLama 2 model
def getLLamaresponse(input_text, no_words, blog_style):
    # LLama 2 model setup
    llm = CTransformers(
        model='llama-2-7b-chat',
        model_type='llama',
        config={'max_new_tokens': 256, 'temperature': 0.01}
    )
    
    # Prompt template
    template = """
        Write a blog for {blog_style} for a topic {input_text}
        within {no_words} words.
    """
    
    prompt = PromptTemplate(input_variables=["blog_style", "input_text", "no_words"],
                            template=template)
    
    # Generate response from LLama 2 model
    response = llm(prompt.format(blog_style=blog_style, input_text=input_text, no_words=no_words))
    return response

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
    response = getLLamaresponse(input_text, no_words, blog_style)
    st.write(response)
