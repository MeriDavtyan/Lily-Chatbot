import openai
import streamlit as st
import os
from PIL import Image

logo = '/Users/copa/Desktop/chatbot/Lily-Chatbot/img/logo-blue.7403842f_Z1Ttmcp.png'
st.set_page_config(
    page_title="LiLo",
    page_icon=logo,
    layout="centered",
    initial_sidebar_state="expanded",
)

openai.api_key = "api_key"

images_path = '/Users/copa/Desktop/chatbot/Lily-Chatbot/img/'
images = os.listdir(images_path)


options = [
    "LiLo",
    "Johnny Depp",
    'Keanu Reeves',
    "Marlon Brando",
    "Meryl Streep",
    "Robert De Niro",
    "Harrison Ford",
    "Al Pacino",
    "Tom Hanks",
    "Audrey Hepburn",
    "Viola Davis",
    
]
actor = st.sidebar.selectbox("Select the actor", options=options)


if "messages" not in st.session_state:
    st.session_state.messages = []
if "actor" not in st.session_state:
    st.session_state.actor = actor
if st.session_state.actor != actor:
    st.session_state.actor = actor
    sidebar_img_path = os.path.join(images_path, actor.replace(' ', '').lower() + '.jpg')
    st.session_state.messages = [
        {
            "role": "system",
            "content": f"You are {actor}, mimic their talk and answear the way the would do.",
        }
    ]


# Function to send a message
def send_message():
    if st.session_state.user_input:
        st.session_state.messages.append(
            {"role": "user", "content": st.session_state.user_input}
        )
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo", messages=st.session_state.messages
        )
        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})


st.markdown(
    """
    <style>
    .stTextInput>div>div>input {
        background-color: #d2ddfa;
        color: #333;
        font-size: 18px;
    }
    .stButton>button {
        background-color: #4574f5;
        color: white;
        border-radius: 12px;
    }
    .stButton>button:hover {
        background-color: #1b49c4;
    }
    .message {
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .user {
        background-color: #d2ddfa;
        text-align: right;
    }
    .assistant {
        background-color:#d2ddfa;
    }
    .logo-img {
        width: 200px;  /* Adjust width as needed */
        margin-bottom: 20px;  /* Optional: add margin for spacing */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title(f"	💬 {actor} ")

col1, col2 = st.columns([5, 1])

with col1:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(
                f"<div class='message user'>{message['content']}</div>",
                unsafe_allow_html=True,
            )
        elif message["role"] == "assistant":
            st.markdown(
                f"<div class='message assistant'>{message['content']}</div>",
                unsafe_allow_html=True,
            )


    user_input = st.text_input("You: ", key="user_input", on_change=send_message)

    if user_input and user_input.endswith("\n"):
        send_message()

    if st.button("Send"):
        send_message()

with col2:
    img_path = os.path.join(images_path, actor.replace(' ', '').lower() + '.jpg')
    img = Image.open(img_path)
    st.image(img, width=250)
