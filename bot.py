import openai
import streamlit as st

logo_path = "/Users/copa/Desktop/CHATBOT API/8593225.png"
lily_img = "/Users/copa/Desktop/CHATBOT API/lily_TM_color_RGB.png"
# Streamlit app layout and styling
st.set_page_config(
    page_title="Bot",
    page_icon=":robot_face:",
    layout="centered",
    initial_sidebar_state="expanded",
)
# Set your OpenAI API key
openai.api_key = "sk-aqCLkscjEfzjIk0IDqoyWeIWh8APj7b8DVrVVjLipbT3BlbkFJ7x6NfaVAp16kUJFr9FDJdpAj5tcs_45yZwIfVGflMA"

options = [
    "AI",
    "Marlon Brando",
    "Meryl Streep",
    "Robert De Niro",
    "Harrison Ford",
    "Al Pacino",
    "Tom Hanks",
    "Audrey Hepburn",
    "Viola Davis",
    "Morgan Freeman",
    "Johnny Depp",
]
actor = st.sidebar.selectbox("Select the actor", options=options)

# Initialize session state for storing messages
# Initialize session state variables if they are not already set
if "messages" not in st.session_state:
    st.session_state.messages = []
if "actor" not in st.session_state:
    st.session_state.actor = actor
if st.session_state.actor != actor:
    st.session_state.actor = actor
    st.session_state.messages = [
        {
            "role": "system",
            "content": f"You are {actor}, mimic their talk and answear the way the would do.",
        }
    ]


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

st.title(f"	💬 {actor} Bot")
a = "Ask me anything and I'll try my best to help!"
st.markdown(f"<div class='message assistant'>{a}</div>", unsafe_allow_html=True)


# Display messages (excluding system message)
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

# User input
user_input = st.text_input("You: ", key="user_input", on_change=send_message)

# Handle pressing Enter to send message
if user_input and user_input.endswith("\n"):
    send_message()

if st.button("Send"):
    send_message()
