import openai
import streamlit as st

logo_path = '/Users/copa/Desktop/CHATBOT API/8593225.png'
lily_img = '/Users/copa/Desktop/CHATBOT API/lily_TM_color_RGB.png'

# Set your OpenAI API key
openai.api_key = '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'

# Initialize session state for storing messages
if 'messages' not in st.session_state:
    st.session_state.messages = [{'role': 'system', 'content': 'You are a helpful chat assistant named Lily'}]

# Function to send a message
def send_message():
    """
    Sends a user message to OpenAI's GPT-3.5 model for processing and stores the response.

    Parameters
    ----------
    None

    Returns
    -------
    None

    Raises
    ------
    KeyError
        If `st.session_state.user_input` or `st.session_state.messages` is not found.

    Notes
    -----
    This function assumes the use of Streamlit's `st.session_state` for managing user input
    (`st.session_state.user_input`) and accumulated messages (`st.session_state.messages`).

    - If `st.session_state.user_input` contains user input, it appends the user's message
      to `st.session_state.messages` with 'role' as 'user' and 'content' as the user's input.
    
    - It sends the accumulated messages to OpenAI's GPT-3.5 model (`model='gpt-3.5-turbo'`)
      for generating a response. The response is appended to `st.session_state.messages` with
      'role' as 'assistant' and 'content' as the generated reply.
    
    - Finally, it clears `st.session_state.user_input` to reset the input field.

    """
    if st.session_state.user_input:
        st.session_state.messages.append({'role': 'user', 'content': st.session_state.user_input})
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=st.session_state.messages
        )
        reply = response['choices'][0]['message']['content']
        st.session_state.messages.append({'role': 'assistant', 'content': reply})
        st.session_state.user_input = ""  # Clear input field

# Streamlit app layout and styling
st.set_page_config(
    page_title="Lily",
    page_icon=':cherry_blossom:',
    layout="centered",  
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stTextInput>div>div>input {
        background-color: #ffeaf7;
        color: #333;
        font-size: 18px;
    }
    .stButton>button {
        background-color: #ffb6c1;
        color: white;
        border-radius: 12px;
    }
    .stButton>button:hover {
        background-color: #ff91a4;
    }
    .message {
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .user {
        background-color: #ffcce6;
        text-align: right;
    }
    .assistant {
        background-color: #ccf2ff;
    }
    .logo-img {
        width: 200px;  /* Adjust width as needed */
        margin-bottom: 20px;  /* Optional: add margin for spacing */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🌸 Lily Chatbot")
a = ("Ask me anything and I'll try my best to help!")
st.markdown(f"<div class='message assistant'>{a}</div>", unsafe_allow_html=True)


# Display messages (excluding system message)
for message in st.session_state.messages:
    if message['role'] == 'user':
        st.markdown(f"<div class='message user'>{message['content']}</div>", unsafe_allow_html=True)
    elif message['role'] == 'assistant':
        st.markdown(f"<div class='message assistant'>{message['content']}</div>", unsafe_allow_html=True)

# User input
user_input = st.text_input("You: ", key="user_input", on_change=send_message)

# Handle pressing Enter to send message
if user_input and user_input.endswith('\n'):
    send_message()

if st.button("Send"):
    send_message()
