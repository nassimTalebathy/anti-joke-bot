import streamlit as st
from src.utils import get_punchline, MAX_PROMPT_CHARS

# Title
st.title("""Anti-joke bot
For when you're sick of normal jokes... Powered by ChatGPT3 https://openai.com/blog/chatgpt/""")

# Inputs
st.header('Inputs: ')
is_dev = st.radio('Dev mode', options=['dev', 'prod'], index=1, key='is_dev')
api_key = st.text_input('Enter your API_KEY here:', max_chars=100, key="api_key")
prompt = st.text_input('Enter your prompt here:', max_chars=MAX_PROMPT_CHARS)

# Submit button
clicked = st.button('Get the punchline', key='clicked')

# Run if clicked submit
if clicked:
    st.header('Punchline')
    try:
        punchline = get_punchline(prompt=prompt, api_key=api_key, mode=is_dev)
        st.write(punchline)
    except Exception as e:
        st.write({'error': e, 'str': str(e)})
